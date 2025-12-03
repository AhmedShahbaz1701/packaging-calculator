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

# Force reload .env to catch key changes without restarting
if "GEMINI_API_KEY" in os.environ:
    del os.environ["GEMINI_API_KEY"]
load_dotenv(override=True)

# --- 2. UI HEADER ---
st.title("📦 Invoice Scanner")
st.markdown("""
Upload a PDF invoice (Uline, Alibaba, etc.) to extract packaging line items automatically.
**Powered by Gemini 2.5 Flash**
""")

# --- 3. API KEY CHECK ---
if not os.getenv("GEMINI_API_KEY"):
    st.error("❌ API Key not found. Please check your .env file.")
    st.stop()

# --- 4. MAIN APP ---
uploaded_file = st.file_uploader("Upload Invoice (PDF)", type="pdf")

if uploaded_file is not None:
    # Save to temp file because Gemini needs a path/file object
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    with st.status("Analyzing document with AI...", expanded=True) as status:
        st.write("📤 Uploading to secure sandbox...")
        st.write("🤖 Extracting packaging dimensions...")
        
        # Run the Scanner
        extracted_data = scan_invoice(tmp_path)
        
        status.update(label="Extraction Complete!", state="complete", expanded=False)

    # Cleanup temp file
    os.remove(tmp_path)

    # --- 5. RESULTS DISPLAY ---
    if extracted_data:
        # Summary Metrics
        total_items = sum(item.get('qty', 0) for item in extracted_data)
        col1, col2 = st.columns(2)
        col1.metric("Packaging Line Items", len(extracted_data))
        col2.metric("Total Units", total_items)

        st.divider()
        
        # Detailed Cards
        for item in extracted_data:
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.subheader(item.get('name', 'Unknown Item'))
                c1.caption(f"Material: {item.get('category', 'Unknown')}")
                
                c2.write(f"**Qty:** {item.get('qty', 0)}")
                c3.write(f"**Dims:** {item.get('dims', 'N/A')}")
                st.markdown("---")
        
        # JSON Export for "Power Users"
        with st.expander("View Raw JSON (for API)"):
            st.json(extracted_data)
            
    else:
        st.warning("No packaging items found in this document.")