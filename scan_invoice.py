import os
from dotenv import load_dotenv
from google import genai
import json

# Load environment variables
load_dotenv()

def scan_invoice(pdf_path):
    print(f"👀 Reading {pdf_path} with Gemini 2.5 Flash...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found.")
        return None

    # 1. Initialize Client
    client = genai.Client(api_key=api_key)

    try:
        # 2. Upload File (FIX: Use 'file=' instead of 'path=')
        # The new SDK automatically handles the file reading when you pass the path string.
        file_ref = client.files.upload(file=pdf_path)
        print(f"   ✅ Uploaded as: {file_ref.name}")

        # 3. The Prompt
        prompt = """
        You are a CSRD Compliance Officer. Analyze this invoice.
        Task: Extract ONLY the packaging materials (boxes, mailers, tape). 
        Ignore any actual products (like T-Shirts, Electronics, etc.).
        
        For each packaging item, extract or estimate:
        1. Name
        2. Dimensions (L, W, H) in inches. If not explicit, look for standard codes.
        3. Quantity.
        4. Material Category (options: Corrugated, Poly, Paper, Tape).

        Return the result as a raw JSON list. Do not use Markdown formatting.
        Example: [{"name": "Box", "dims": "12x12x12", "qty": 500, "category": "Corrugated"}]
        """

        # 4. Generate Content
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=[file_ref, prompt]
        )
        
        # 5. Parse
        if response.text:
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            return data
        else:
            print("❌ Empty response from model.")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    # Test locally
    result = scan_invoice("sample_invoice.pdf")
    if result:
        print(json.dumps(result, indent=2))