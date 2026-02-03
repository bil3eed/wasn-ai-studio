import streamlit as st
import google.generativeai as genai

# --- 1. THE ONLY FIX FOR THE 404/REGION ERROR ---
# We use the 2026 stable alias 'gemini-2.5-flash'
# This fetches the key securely from your Streamlit Cloud settings
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key not found! Please add GOOGLE_API_KEY to your Streamlit Secrets.")

st.set_page_config(page_title="WASN STUDIO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE "NON-GARBAGE" UI (SaaS GRADE) ---
st.markdown("""
    <style>
    header, footer, .stDeployButton {display:none !important;}
    .stApp { background-color: #0a0a0a; color: #fdfdfd; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Input Box styling */
    .stTextArea textarea {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 15px !important;
    }
    
    /* Modern Card */
    .post-card {
        background: #111;
        border: 1px solid #222;
        border-radius: 16px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .fb-header { display: flex; align-items: center; margin-bottom: 15px; }
    .avatar { width: 40px; height: 40px; background: #0084ff; border-radius: 50%; display:flex; align-items:center; justify-content:center; margin-right: 12px; font-weight:bold; }
    
    .generate-btn button {
        background: linear-gradient(90deg, #0084ff, #0056b3) !important;
        border: none !important;
        padding: 20px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 12px !important;
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. APP LOGIC ---
st.title("Wasn Digital Content Studio")
st.write("Professional AI-driven social copy for high-growth brands.")

topic = st.text_area("What is your campaign goal?", placeholder="Describe your topic here...", height=120)

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("Brand Voice", ["Bold", "Professional", "Funny", "Luxury"])
with col2:
    num = st.slider("Options", 1, 3, 2)

if st.button("Generate Content", key="gen_btn"):
    if topic:
        try:
            # TRYING THE 2026 STABLE FLASH MODEL
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            with st.spinner(" "):
                response = model.generate_content(f"Create {num} Facebook posts for: {topic}. Tone: {tone}. Separate with '---'. No labels.")
                posts = response.text.split("---")

            for post in posts:
                if post.strip():
                    st.markdown(f"""
                    <div class="post-card">
                        <div class="fb-header">
                            <div class="avatar">W</div>
                            <div>
                                <div style="font-weight: 700;">Wasn AI Studio</div>
                                <div style="font-size: 12px; color: #888;">Live Preview · 🌎</div>
                            </div>
                        </div>
                        <div style="font-size: 16px; line-height: 1.6; color: #ddd;">{post.strip()}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(post.strip())
        
        except Exception as e:
            st.error(f"Region/API Error: {str(e)}")
            st.info("If this persists, your IP is likely blocked from the Free Tier. Using a VPN set to the USA or Europe usually fixes this instantly.")
    else:

        st.warning("Input required.")
