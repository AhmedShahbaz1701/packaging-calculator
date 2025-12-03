import streamlit as st
import tempfile
import os
import csv
import datetime
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

# --- 5. SESSION STATE INITIALIZATION ---
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

# --- 6. MAIN APP ---
uploaded_file = st.file_uploader("Upload Invoice (PDF)", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    # We'll cache the extraction to avoid re-scanning on every rerun (like form submission)
    @st.cache_data(show_spinner=False)
    def cached_scan(path):
        return scan_invoice(path, api_key=api_key)

    with st.status("Analyzing document with AI...", expanded=True) as status:
        st.write("📤 Uploading to secure sandbox...")
        st.write("🤖 Extracting packaging dimensions...")
        
        extracted_data = cached_scan(tmp_path)
        
        status.update(label="Extraction Complete!", state="complete", expanded=False)

    # --- 7. SUMMARY RESULTS (Visible to All) ---
    if extracted_data:
        total_items = sum(item.get('qty', 0) for item in extracted_data)
        col1, col2 = st.columns(2)
        col1.metric("Packaging Line Items", len(extracted_data))
        col2.metric("Total Units", total_items)

        st.divider()

        # --- 8. LEAD GEN GATE ---
        if not st.session_state.unlocked:
            st.info("🔒 **Unlock Full Report**")
            st.markdown("Enter your email to view the detailed line-item breakdown and download the JSON data.")
            
            with st.form("lead_form"):
                email_input = st.text_input("Email Address", placeholder="you@company.com")
                submit_btn = st.form_submit_button("Unlock Report 🔓")
                
                if submit_btn:
                    if email_input and "@" in email_input:
                        # Save Lead
                        try:
                            with open("leads.csv", "a", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow([datetime.datetime.now().isoformat(), email_input])
                        except Exception as e:
                            st.error(f"Error saving lead: {e}")

                        st.session_state.unlocked = True
                        st.rerun() # Rerun to show unlocked content
                    else:
                        st.warning("Please enter a valid email address.")
        
        # --- 9. PREMIUM CONTENT (Unlocked) ---
        if st.session_state.unlocked:
            st.success("Report Unlocked! ✅")
            
            st.subheader("Detailed Breakdown")
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
            
            # Reset button to test again (Optional, helpful for dev)
            if st.button("Start New Scan"):
                st.session_state.unlocked = False
                st.rerun()

    else:
        st.warning("No packaging items found in this document.")
