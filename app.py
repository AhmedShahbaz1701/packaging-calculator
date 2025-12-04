import streamlit as st
import tempfile
import os
import csv
import datetime
import time
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from scan_invoice import scan_invoice

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Tare.fyi Scanner", 
    page_icon="📦",
    layout="centered"
)

# --- 2. HYBRID KEY LOADER ---
def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")

api_key = get_api_key()

# --- 3. GOOGLE SHEETS INTEGRATION ---
def save_lead_to_sheets(email, retries=3):
    for i in range(retries):
        try:
            # Define Scopes
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            
            # Load Credentials from Streamlit Secrets
            if "gcp_service_account" in st.secrets:
                creds_dict = st.secrets["gcp_service_account"]
                credentials = Credentials.from_service_account_info(
                    creds_dict,
                    scopes=scopes
                )
                
                # Authenticate & Open Sheet
                client = gspread.authorize(credentials)
                sheet_url = st.secrets.get("SHEETS_URL") # Add SHEETS_URL to secrets
                
                if sheet_url:
                    sheet = client.open_by_url(sheet_url).sheet1
                    # Append Row: [Email, Timestamp, Action]
                    timestamp = datetime.datetime.now().isoformat()
                    sheet.append_row([email, timestamp, "Unlocked Report"])
                    return True
                else:
                    raise Exception("SHEETS_URL not found in secrets.")
            else:
                raise Exception("GCP Credentials not found in secrets.")

        except Exception as e:
            if i < retries - 1:
                time.sleep(2 ** i)  # Exponential backoff
                continue
            st.error(f"Error saving lead to Google Sheets after {retries} attempts: {e}")
            return False
    return False

# --- 4. UI HEADER ---
st.title("📦 Invoice Scanner")
st.markdown("""
Upload a PDF invoice (Uline, Alibaba, etc.) to extract packaging line items automatically.
**Powered by Gemini 2.5 Flash**
""")

# --- 5. API KEY CHECK ---
if not api_key:
    st.error("❌ API Key not found.")
    st.info("If running locally: Check your .env file.")
    st.info("If running on Streamlit Cloud: Go to App Settings > Secrets and add GEMINI_API_KEY.")
    st.stop()

# --- 6. SESSION STATE INITIALIZATION ---
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

# --- 7. MAIN APP ---
uploaded_file = st.file_uploader("Upload Invoice (PDF)", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    @st.cache_data(show_spinner=False)
    def cached_scan(path):
        return scan_invoice(path, api_key=api_key)

    with st.status("Analyzing document with AI...", expanded=True) as status:
        st.write("📤 Uploading to secure sandbox...")
        st.write("🤖 Extracting packaging dimensions...")
        
        extracted_data = cached_scan(tmp_path)
        
        status.update(label="Extraction Complete!", state="complete", expanded=False)

    # --- 8. SUMMARY RESULTS (Visible to All) ---
    if extracted_data:
        total_items = sum(item.get('qty', 0) for item in extracted_data)
        col1, col2 = st.columns(2)
        col1.metric("Packaging Line Items", len(extracted_data))
        col2.metric("Total Units", total_items)

        st.divider()

        # --- 9. LEAD GEN GATE ---
        if not st.session_state.unlocked:
            st.info("🔒 **Unlock Full Report**")
            st.markdown("Enter your email to view the detailed line-item breakdown and download the JSON data.")
            
            with st.form("lead_form"):
                email_input = st.text_input("Email Address", placeholder="you@company.com")
                submit_btn = st.form_submit_button("Unlock Report 🔓")
                
                if submit_btn:
                    if email_input and "@" in email_input:
                        # Call Save Function
                        if save_lead_to_sheets(email_input):
                            st.session_state.unlocked = True
                            st.rerun()
                    else:
                        st.warning("Please enter a valid email address.")
        
        # --- 10. PREMIUM CONTENT (Unlocked) ---
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
            
            if st.button("Start New Scan"):
                st.session_state.unlocked = False
                st.rerun()

    else:
        st.warning("No packaging items found in this document.")
