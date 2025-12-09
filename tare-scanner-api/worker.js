export default {
  async fetch(request, env) {
    // 1. CORS Headers (Allow your site to talk to this)
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") return new Response(null, { headers: corsHeaders });

    if (request.method === "POST") {
      try {
        const url = new URL(request.url);

        // --- NEW: Log Calculation Route ---
        if (url.pathname === "/log-calculation") {
            const body = await request.json();
            const { box_name, l, w, h, unit, weight_grams, qty } = body;
            // Format dimensions string
            const dimensions = `${l}x${w}x${h} ${unit}`;
            
            if (env.tare_db) {
                await env.tare_db.prepare(
                    "INSERT INTO usage_logs (box_name, dimensions, weight_grams, qty, timestamp) VALUES (?, ?, ?, ?, ?)"
                ).bind(box_name, dimensions, weight_grams, qty, new Date().toISOString()).run();
            }
            return new Response("OK", { status: 200, headers: corsHeaders });
        }

        const formData = await request.formData();
        const file = formData.get("file");
        const email = formData.get("email");

        // SCENARIO A: Lead Opt-In (Email Only)
        // This runs when someone clicks "Notify Me" at the bottom
        if (email && !file) {
           if (env.tare_db) {
             await env.tare_db.prepare("INSERT INTO leads (email, created_at, source) VALUES (?, ?, 'opt_in')")
               .bind(email, new Date().toISOString())
               .run();
             return new Response(JSON.stringify({ success: true }), { headers: { "Content-Type": "application/json", ...corsHeaders } });
           } else {
             return new Response(JSON.stringify({ error: "DB not configured" }), { status: 500, headers: corsHeaders });
           }
        }

        // SCENARIO B: File Scan (File Only)
        // This runs when they upload a PDF
        if (file) {
            // We use the REST API directly to keep the worker lightweight (no heavy Python SDKs)
            const GEMINI_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${env.GEMINI_API_KEY}`;
            
            const arrayBuffer = await file.arrayBuffer();
            let binary = '';
            const bytes = new Uint8Array(arrayBuffer);
            const len = bytes.byteLength;
            for (let i = 0; i < len; i++) {
                binary += String.fromCharCode(bytes[i]);
            }
            const base64String = btoa(binary);

            const payload = {
              contents: [{
                parts: [
                  { text: "Analyze this invoice. Identify all packaging materials (boxes, mailers, tape, labels). Ignore the products being sold. Return a raw JSON list of objects with these keys: name, dims, qty, category. If dimensions are missing, put 'N/A'. Response must be a raw JSON array." },
                  { inline_data: { mime_type: file.type, data: base64String } }
                ]
              }],
              generationConfig: {
                response_mime_type: "application/json"
              }
            };

            const aiReq = await fetch(GEMINI_URL, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload)
            });
            const aiRes = await aiReq.json();

            if (aiRes.error) {
                return new Response(JSON.stringify({ error: "AI Error: " + aiRes.error.message }), { status: 500, headers: { "Content-Type": "application/json", ...corsHeaders } });
            }
            
            // Safe parsing of the AI response
            const text = aiRes.candidates?.[0]?.content?.parts?.[0]?.text || "";
            
            // Try to find a JSON array in the text
            const jsonMatch = text.match(/\[[\s\S]*\]/);
            let jsonStr = jsonMatch ? jsonMatch[0] : "[]";

            // If we couldn't find a JSON array, or if it's empty, we might want to know what the text was.
            // We'll try to parse it to see if it's valid.
            try {
                const parsed = JSON.parse(jsonStr);
                // Return the parsed object but WRAPPED so we can include debug info if needed.
                // Note: The frontend expects a direct array, so we might break it if we change the shape.
                // BUT the user is debugging. Let's return the raw array if valid, but if empty/invalid, 
                // we might want to return an error object or the raw text in a special way?
                
                // User said "I'm still getting [] response". 
                // Let's stick to returning the JSON but maybe we can log the raw text to the database if we had one?
                // Or, let's temporarily return an object with { data: [...], debug: "..." } if the user allows changing frontend?
                // The frontend does `data.map(...)` in `renderResults`. So it expects an Array.
                // If I return `{ debug: ... }` it will crash the frontend map.
                
                // Strategy: If the array is empty, we force a "fake" item with the debug text so it shows up in the UI table.
                if (parsed.length === 0 && text.length > 0) {
                    return new Response(JSON.stringify([{
                        name: "DEBUG: No items found", 
                        dims: "Raw AI Response:", 
                        qty: text.substring(0, 100) + "...", 
                        category: "Debug"
                    }]), { headers: { "Content-Type": "application/json", ...corsHeaders } });
                }
                
                return new Response(jsonStr, { headers: { "Content-Type": "application/json", ...corsHeaders } });

            } catch (e) {
                 // If parsing fails, return the raw text as a debug item
                 return new Response(JSON.stringify([{
                    name: "Error Parsing JSON", 
                    dims: "See Details", 
                    qty: text.substring(0, 50), 
                    category: "Error"
                }]), { headers: { "Content-Type": "application/json", ...corsHeaders } });
            }
        }

        return new Response("Invalid Request", { status: 400, headers: corsHeaders });

      } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: corsHeaders });
      }
    }
    return new Response("Method not allowed", { status: 405, headers: corsHeaders });
  }
};