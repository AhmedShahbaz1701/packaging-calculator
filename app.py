import streamlit as st
import tempfile
import os
from dotenv import load_dotenv
from scan_invoice import scan_invoice

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Tare.fyi Scanner", 
    page_icon="📦",
    layout="centered"
)

# --- 2. HYBRID KEY LOADER (The Fix) ---
# This function checks Streamlit Secrets first (Cloud), then .env (Local)
def get_api_key():
    # 1. Try Streamlit Secrets (Cloud)
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    
    # 2. Try Local .env
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")

api_key = get_api_key()

# --- 3. UI HEADER ---
st.title("📦 Invoice Scanner")
st.markdown("""
Upload a PDF invoice (Uline, Alibaba, etc.) to extract packaging line items automatically.
**Powered by Gemini 2.5 Flash**
""")

# --- 4. API KEY CHECK ---
if not api_key:
    st.error("❌ API Key not found.")
    st.info("If running locally: Check your .env file.")
    st.info("If running on Streamlit Cloud: Go to App Settings > Secrets and add GEMINI_API_KEY.")
    st.stop()

# --- 5. MAIN APP ---
uploaded_file = st.file_uploader("Upload Invoice (PDF)", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    with st.status("Analyzing document with AI...", expanded=True) as status:
        st.write("📤 Uploading to secure sandbox...")
        st.write("🤖 Extracting packaging dimensions...")
        
        # UPDATE: Pass the API key to the function
        extracted_data = scan_invoice(tmp_path, api_key=api_key)
        
        status.update(label="Extraction Complete!", state="complete", expanded=False)

    os.remove(tmp_path)

    # --- 6. RESULTS DISPLAY ---
    if extracted_data:
        total_items = sum(item.get('qty', 0) for item in extracted_data)
        col1, col2 = st.columns(2)
        col1.metric("Packaging Line Items", len(extracted_data))
        col2.metric("Total Units", total_items)

        st.divider()
        
        for item in extracted_data:
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.subheader(item.get('name', 'Unknown Item'))
                c1.caption(f"Material: {item.get('category', 'Unknown')}")
                
                c2.write(f"**Qty:** {item.get('qty', 0)}")
                c3.write(f"**Dims:** {item.get('dims', 'N/A')}")
                st.markdown("---")
        
        with st.expander("View Raw JSON (for API)"):
            st.json(extracted_data)
            
    else:
        st.warning("No packaging items found in this document.")