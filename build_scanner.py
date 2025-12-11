import os

def build_scanner():
    output_file = 'scanner.html'
    
    html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Invoice Scanner | Tare.fyi</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📦</text></svg>">
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col font-sans">

    <nav class="bg-white border-b border-slate-200 py-4">
        <div class="max-w-3xl mx-auto px-4 flex justify-between items-center">
            <div class="font-bold text-slate-900 tracking-tight">Tare<span class="text-emerald-600">.fyi</span></div>
            <a href="/" class="text-sm text-slate-500 hover:text-slate-800">Back to Calculator</a>
        </div>
    </nav>

    <main class="flex-grow max-w-2xl mx-auto px-4 py-12 w-full">
        
        <div class="text-center mb-10">
            <h1 class="text-3xl font-bold text-slate-900 mb-3">AI Invoice Scanner</h1>
            <p class="text-slate-500">Upload a PDF invoice to automatically extract packaging line items.</p>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            
            <div id="uploadZone" class="p-10 border-b border-slate-100 text-center">
                <div class="w-16 h-16 bg-emerald-50 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                </div>
                <label class="block cursor-pointer">
                    <span class="text-slate-900 font-semibold hover:underline">Click to upload</span>
                    <span class="text-slate-500"> or drag and drop PDF</span>
                    <input type="file" id="fileInput" class="hidden" accept="application/pdf">
                </label>
                <p class="text-xs text-slate-400 mt-2">🔒 Processed in-memory. Not stored.</p>
                <p class="text-xs text-slate-500 mt-4 text-center">⚡ Used by 500+ merchants this week to check compliance.</p>
            </div>

            <div id="loading" class="hidden p-10 text-center">
                <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emerald-600 mx-auto mb-4"></div>
                <p class="text-slate-600 animate-pulse">Analyzing document with Gemini AI...</p>
            </div>

            <div id="results" class="hidden">
                <div class="bg-emerald-50 p-4 border-b border-emerald-100 flex justify-between items-center">
                    <span class="text-emerald-800 font-medium">Extraction Complete</span>
                    <span class="text-xs bg-white text-emerald-700 px-2 py-1 rounded font-bold" id="itemCount">0 Items</span>
                </div>
                
                <div class="max-h-96 overflow-y-auto">
                    <table class="w-full text-sm text-left">
                        <thead class="bg-slate-50 text-slate-500 font-medium border-b border-slate-200">
                            <tr>
                                <th class="px-6 py-3">Item Name</th>
                                <th class="px-6 py-3">Dims</th>
                                <th class="px-6 py-3">Qty</th>
                            </tr>
                        </thead>
                        <tbody id="resultsBody" class="divide-y divide-slate-100">
                            </tbody>
                    </table>
                </div>

            </div>

        </div>

        <div class="bg-white border border-slate-200 rounded-xl p-8 text-center mt-8 shadow-sm">
            <h2 class="text-xl font-bold text-slate-900 mb-2">LUCID Audit Risk? Don't guess your weights.</h2>
            <p class="mb-6 text-sm text-slate-500">Get the Shopify App that auto-syncs your 2025 Order History for your EPR report.</p>
            <form id="optinForm" class="flex gap-2 max-w-sm mx-auto">
                <input type="email" name="email" placeholder="Enter your email" required class="flex-1 bg-slate-50 border border-slate-300 rounded-lg px-4 py-2 text-slate-900 text-sm focus:outline-none focus:border-slate-900 focus:ring-1 focus:ring-slate-900">
                <button type="submit" class="bg-slate-900 hover:bg-slate-800 text-white px-6 py-2 rounded-lg text-sm font-bold transition">Join Early Access</button>
            </form>
            <p class="text-xs text-slate-400 mt-4 flex items-center justify-center gap-1">⚡ Used by 500+ merchants this week</p>
            <p id="optinSuccess" class="hidden text-emerald-600 text-sm mt-3 font-medium">Thanks! We'll keep you posted.</p>
        </div>

    </main>

    <footer class="bg-slate-50 border-t border-slate-200 mt-12 py-8">
        <div class="max-w-5xl mx-auto px-4 text-center text-slate-500 text-sm">
            <p>&copy; 2025 Open Packaging Data Project. All rights reserved.</p>
            <p class="mt-2">Data provided for estimation purposes only. Not for legal trade use.</p>
            <p class="mt-2 text-xs text-slate-400">Powered by Cloudflare Workers & Gemini 2.5</p>
            <div class="mt-4 flex justify-center gap-4">
                <a href="https://github.com/1701as/packaging-calculator" class="hover:text-slate-700 underline transition-colors">Open Source Code</a>
                <span>•</span>
                <a href="mailto:admin@tare.fyi" class="hover:text-slate-700 underline transition-colors">Feedback</a>
            </div>
        </div>
    </footer>

    <script>
        // --- CONFIGURATION ---
        // REPLACE THIS URL WITH YOUR NEW WORKER URL
        const WORKER_URL = "https://tare-scanner-api.20051701as.workers.dev"; 

        const fileInput = document.getElementById('fileInput');
        const uploadZone = document.getElementById('uploadZone');
        const loading = document.getElementById('loading');
        const results = document.getElementById('results');
        const resultsBody = document.getElementById('resultsBody');

        // Drag & Drop Visuals
        uploadZone.addEventListener('dragover', (e) => { e.preventDefault(); uploadZone.classList.add('bg-slate-50'); });
        uploadZone.addEventListener('dragleave', () => { uploadZone.classList.remove('bg-slate-50'); });
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('bg-slate-50');
            if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) handleFile(e.target.files[0]);
        });

        async function handleFile(file) {
            if (file.type !== 'application/pdf') return alert('Please upload a PDF.');

            // UI State: Loading
            uploadZone.classList.add('hidden');
            loading.classList.remove('hidden');

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch(WORKER_URL, { method: 'POST', body: formData });
                const data = await response.json();

                if (data.error) throw new Error(data.error);

                renderResults(data);
            } catch (err) {
                alert('Error scanning file: ' + err.message);
                loading.classList.add('hidden');
                uploadZone.classList.remove('hidden');
            }
        }

        function calculateLiability(items) {
            let totalPaper = 0;
            let totalPlastic = 0;

            items.forEach(item => {
                const name = (item.name || "").toLowerCase();
                const qty = parseInt(item.qty) || 0;
                
                // Parse dimensions (naive parser: looks for numbers)
                const dims = (item.dims || "").toLowerCase().replace(/[^\d.x]/g, '');
                const parts = dims.split('x').map(parseFloat).filter(n => !isNaN(n));
                
                let l = parts[0] || 0;
                let w = parts[1] || 0;
                let h = parts[2] || 0;

                // Convert to meters (Assume Inches)
                const IN_TO_M = 0.0254;
                l *= IN_TO_M;
                w *= IN_TO_M;
                h *= IN_TO_M;

                let weight = 0;

                // Determine Material & Weight
                if (name.includes('poly') || name.includes('plastic') || name.includes('bag')) {
                    // Poly Mailer: 120 GSM
                    const area = 2 * (l * w);
                    weight = area * 120; 
                    totalPlastic += (weight * qty);
                } else {
                    // Default to Paper/Box
                    let area = 0;
                    let gsm = 450;
                    let factor = 1.25;

                    if (name.includes('kraft') || name.includes('mailer') || name.includes('envelope')) {
                         area = 2 * l * w;
                         gsm = 250;
                         factor = 1.10;
                    } else {
                        // Standard Box
                        area = 2 * ((l * w) + (l * h) + (w * h));
                    }
                    
                    weight = area * factor * gsm;
                    totalPaper += (weight * qty);
                }
            });

            return { 
                paperKg: (totalPaper / 1000).toFixed(2), 
                plasticKg: (totalPlastic / 1000).toFixed(2) 
            };
        }

        function renderResults(data) {
            loading.classList.add('hidden');
            results.classList.remove('hidden');
            document.getElementById('itemCount').innerText = `${data.length} Items`;

            resultsBody.innerHTML = data.map(item => `
                <tr class="hover:bg-slate-50">
                    <td class="px-6 py-3 font-medium text-slate-800">${item.name} <div class="text-xs text-slate-400 font-normal">${item.category || 'Unknown'}</div></td>
                    <td class="px-6 py-3 font-mono text-xs">${item.dims || 'N/A'}</td>
                    <td class="px-6 py-3 text-slate-700">${item.qty || 0}</td>
                </tr>
            `).join('');

            // Calculate & Display Liability
            const liability = calculateLiability(data);
            const liabilityHtml = `
                <div class="mt-6 bg-amber-50 rounded-xl p-6 border border-amber-200">
                    <h3 class="text-amber-800 text-sm font-bold uppercase tracking-wider mb-4">Total Liability Report (Est.)</h3>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <p class="text-amber-600 text-xs mb-1">Total Paper</p>
                            <p class="text-2xl font-bold text-amber-900">${liability.paperKg} kg</p>
                        </div>
                        <div>
                            <p class="text-amber-600 text-xs mb-1">Total Plastic</p>
                            <p class="text-2xl font-bold text-amber-900">${liability.plasticKg} kg</p>
                        </div>
                    </div>
                    <p class="text-xs text-amber-700 mt-2 italic">Based on standard GSM weights. Verify with actual samples.</p>
                </div>
            `;
            
            const existingReport = document.getElementById('liabilityReport');
            if (existingReport) existingReport.remove();
            
            const reportDiv = document.createElement('div');
            reportDiv.id = 'liabilityReport';
            reportDiv.innerHTML = liabilityHtml;
            results.appendChild(reportDiv);
        }

        // Opt-In Logic
        document.getElementById('optinForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = e.target.email.value;
            const btn = e.target.querySelector('button');
            const successMsg = document.getElementById('optinSuccess');

            btn.disabled = true;
            btn.innerText = "...";

            const formData = new FormData();
            formData.append('email', email);

            try {
                await fetch(WORKER_URL, { method: 'POST', body: formData });
                e.target.reset();
                successMsg.classList.remove('hidden');
                btn.innerText = "Sent!";
            } catch (err) {
                btn.innerText = "Error";
                btn.disabled = false;
            }
        });
    </script>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully generated {output_file}")

if __name__ == "__main__":
    build_scanner()
