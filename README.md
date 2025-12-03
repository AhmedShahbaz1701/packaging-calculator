# Open Packaging Weight Calculator & AI Scanner 📦
### The Open Source CSRD & EPR Compliance Tool

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg) ![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg) ![Gemini AI](https://img.shields.io/badge/AI-Gemini%202.5-8E75B2.svg)

## The Why: Fixing the E-Commerce Data Nightmare

If you run a Shopify store or manage logistics, you know the panic. New EU regulations like **CSRD**, **LUCID (Germany)**, and **CITEO (France)** demand precise weight data for every gram of packaging you ship into their countries.

**The problem?** Most generic supplier invoices just say "100x Corrugated Boxes." They don't list the specific gram weight or material codes required by law.

**The result?** Merchants are either guessing (risking audits) or overpaying for "Enterprise Sustainability Platforms" just to access basic physics data.

**The Solution:** This project provides two open-source tools to solve this:
1.  A **Static Calculator** for instant, physics-based estimates of standard packaging.
2.  An **AI Invoice Scanner** that reads your supplier PDFs and extracts compliance data automatically.

---

## Features

### 🧮 Static Calculator (Web Tool)
*   **Instant Math:** Estimates weight based on dimensions (L x W x H) and material density (GSM).
*   **Compliance Ready:** Auto-generates Material Codes (PAP 20, PAP 21, LDPE 4).
*   **Standard Library:** Pre-loaded with **FedEx, USPS, and Amazon** sizes.
*   **Zero Latency:** Runs as a static HTML site (Cloudflare Pages/Netlify).

### 🤖 AI Invoice Scanner (Streamlit App)
*   **Powered by Gemini 2.5 Flash:** Upload a supplier PDF (e.g., Uline invoice).
*   **Smart Extraction:** Ignores products (T-shirts) and only finds packaging (Boxes, Tape, Mailers).
*   **Auto-Calculation:** Infers dimensions and quantities to calculate total plastic/paper liability.
*   **CSV Export:** Download a "Tare.fyi" compatible CSV for instant reporting.

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/packaging-calculator.git
cd packaging-calculator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
You need a **Google Gemini API Key** to use the AI Scanner.
*   Get it here: [Google AI Studio](https://aistudio.google.com/app/apikey)

**For Local Development:**
Create a `.env` file in the root directory:
```bash
GEMINI_API_KEY="your_actual_api_key_here"
```

**For Streamlit Cloud:**
Add your key to the Secrets management console as `GEMINI_API_KEY`.

### 4. Run the Tools

**Option A: Build the Static Site**
Generates the HTML pages for the calculator.
```bash
python generate.py
python build_index.py
# Output is in the /public folder
```

**Option B: Run the AI Scanner**
Launches the interactive Streamlit app.
```bash
streamlit run app.py
```

---

## How to Contribute 🤝

This is a community-driven project. We believe access to compliance data should be free.

**We need your help to expand the "Standard Industry Sizes" library.**

Do you use a specific carrier box (DHL, DPD, UPS) or a popular supplier size (Uline)?

1.  Open `generate.py`.
2.  Find the `data_sources` list.
3.  Add your box details following this format:
    ```python
    {"name": "DHL Box 2", "l": 12, "w": 10, "h": 6, "type": "box", "wall": "single"},
    ```
4.  Submit a **Pull Request**!

*Note: Please ensure dimensions are accurate. If you have physical samples, weighing them to verify our GSM assumptions is highly appreciated!*

---

## Roadmap 🗺️

*   [ ] **Add DHL & DPD Standard Sizes:** Expand coverage for European merchants.
*   [ ] **Shopify App Integration:** Pull order history directly to calculate total liability.
*   [ ] **Biodegradability Estimator:** Add logic to estimate decomposition times.
*   [ ] **Multi-Language Support:** French and German translations for local compliance officers.

---

## License

This project is open-sourced under the **MIT License**. You are free to use, modify, and distribute this software as you wish.

**Built for the Open Web.**