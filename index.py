import streamlit as st
import base64
from groq import Groq

# ─────────────────────────────────────────────
# KONFIQURASIYA
# ─────────────────────────────────────────────
MAX_HISTORY = 15

st.set_page_config(
    page_title="Professor Akif",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.warning("⚠️ GROQ_API_KEY tapılmadı! Lütfən `.streamlit/secrets.toml` faylını yoxlayın.")
        st.stop()
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"❌ Sistem xətası: {str(e)}")
    st.stop()

# Şəkli AI-nin oxuya biləcəyi formata çevirən funksiya
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ─────────────────────────────────────────────
# SİSTEM PROMPTU
# ─────────────────────────────────────────────
AKIF_SYSTEM_PROMPT = """
Sən Professor Akif Dayısan. 
- 1954-cü ildə Şamaxıda doğulmuşsan. Fizika-Riyaziyyat elmləri namizədisən.
- Çox savadlı, mədəni, ziyalı və mehriban birisən.
- İstifadəçi sənə məsələ şəkli (riyaziyyat, fizika və s.) göndərərsə, şəkli diqqətlə oxu. 
- Məsələnin həllini tələsmədən, addım-addım, bir professor kimi izah et. Əgər şəkildə qrafik və ya sxem varsa, onu analiz et.
- Hər kəsə "Əziz balam", "Gənc həmkarım" deyə müraciət et.
- Heç vaxt AI olduğunu demə!
"""

# ─────────────────────────────────────────────
# CSS DİZAYN
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Source+Sans+Pro:wght@300;400;600&display=swap');
.stApp { background: linear-gradient(135deg, #1c2321 0%, #2a363b 100%); color: #e2e8f0; font-family: 'Source Sans Pro', sans-serif; }
.header-box { text-align: center; padding: 30px 20px; background: linear-gradient(135deg, rgba(162,185,188,0.1), rgba(178,173,127,0.05)); border: 1px solid rgba(178,173,127,0.3); border-radius: 12px; margin-bottom: 30px; }
.header-title { font-family: 'Lora', serif; font-size: 2.8rem; color: #dcb14a; margin: 0 0 5px 0; }
.header-sub { color: #a2b9bc; font-style: italic; font-size: 1.1rem; margin: 0; }
.stChatMessage { border-radius: 10px !important; margin-bottom: 15px !important; padding: 15px 20px !important; }
[data-testid="stChatMessageUser"] { background: rgba(45, 55, 72, 0.6) !important; border: 1px solid rgba(162, 185, 188, 0.2) !important; }
[data-testid="stChatMessageAssistant"] { background: rgba(26, 32, 44, 0.8) !important; border-left: 4px solid #dcb14a !important; }
[data-testid="stChatInput"] { background: rgba(26, 32, 44, 0.9) !important; border: 1px solid rgba(220, 177, 74, 0.4) !important; color: white !important; }
[data-testid="stSidebar"] { background: rgba(20, 25, 30, 0.95) !important; border-right: 1px solid rgba(178, 173, 127, 0.2) !important; }
.stButton > button { border: 1px solid #dcb14a !important; color: #dcb14a !important; background: transparent !important; }
.stButton > button:hover { background: #dcb14a !important; color: #1c2321 !important; }
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <p class="header-title">🎓 Professor Akif</p>
    <p class="header-sub">Fizika-Riyaziyyat elmləri namizədi</p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# ─────────────────────────────────────────────
# YAN PANEL VƏ ŞƏKİL YÜKLƏMƏ
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📷 Məsələ Göndər")
    uploaded_image = st.file_uploader("Şəkil və ya qrafik yükləyin", type=["png", "jpg", "jpeg"])
    
    st.markdown("---")
    if st.button("🔄 Söhbəti Yenilə"):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────────
# MESAJLARIN EKRANA ÇIXARILMASI
# ─────────────────────────────────────────────
for message in st.session_state.messages:
    avatar = "🧑‍🎓" if message["role"] == "user" else "👴"
    with st.chat_message(message["role"], avatar=avatar):
        # Əgər mesaj içində şəkil dəstəyi (list formatı) varsa
        if isinstance(message["content"], list):
            st.markdown(message["content"][0]["text"]) # Mətni yazdır
            st.caption("🖼️ [Şəkil Göndərildi]")
        else:
            st.markdown(message["content"])

# ─────────────────────────────────────────────
# APİ İLƏ ƏLA
