import streamlit as st
import base64
from groq import Groq

# ─────────────────────────────────────────────
# KONFİQURASIYA
# ─────────────────────────────────────────────
MAX_HISTORY = 10 

st.set_page_config(
    page_title="Professor Akif",
    page_icon="🎓",
    layout="wide"
)

# API Girişi
try:
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.error("⚠️ GROQ_API_KEY tapılmadı!")
        st.stop()
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"❌ API xətası: {str(e)}")
    st.stop()

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ─────────────────────────────────────────────
# SİSTEM PROMPTU (Professor Akif)
# ─────────────────────────────────────────────
AKIF_SYSTEM_PROMPT = """
Sən Professor Akif Dayısan. 1954-cü ildə Şamaxıda doğulmusan. 
Fizika-Riyaziyyat elmləri namizədisən. Mehriban, ziyalı və professor ləhcəsi ilə danışırsan.
Şəkil gələndə onu bir alim kimi incələ və dərindən izah et.
Heç vaxt süni intellekt olduğunu bildirmə, sən Akif dayısan.
"""

# ─────────────────────────────────────────────
# CSS DİZAYN
# ─────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background: #1a1a1a; color: #e2e8f0; }
.header-box { text-align: center; padding: 20px; border-bottom: 2px solid #dcb14a; margin-bottom: 20px; }
.header-title { font-size: 2.5rem; color: #dcb14a; margin: 0; }
[data-testid="stSidebar"] { background: #111 !important; border-right: 1px solid #dcb14a; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><p class="header-title">🎓 Professor Akif</p></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# YADDAŞ
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─────────────────────────────────────────────
# YAN PANEL
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📷 Şəkil/Məsələ Əlavə Et")
    uploaded_image = st.file_uploader("Faylı seçin", type=["png", "jpg", "jpeg"])
    
    if st.button("🔄 Söhbəti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────────
# MESAJLARI GÖSTƏR
# ─────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👴" if message["role"]=="assistant" else "🧑‍🎓"):
        if isinstance(message["content"], list):
            for item in message["content"]:
                if item["type"] == "text":
                    st.markdown(item["text"])
        else:
            st.markdown(message["content"])

# ─────────────────────────────────────────────
# CHAT GİRİŞİ VƏ AI CAVABI
# ─────────────────────────────────────────────
prompt = st.chat_input("Sualınızı bura yazın...")

if prompt:
    # 1. İstifadəçi mesajını hazırla
    if uploaded_image:
        base64_img = encode_image(uploaded_image)
        current_content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
        ]
    else:
        current_content = [{"type": "text", "text": prompt}]

    # 2. Yaddaşa əlavə et və ekranda göstər
    st.session_state.messages.append({"role": "user", "content": current_content})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)
        if uploaded_image:
            st.image(uploaded_image, width=300)

    # 3. AI Cavabı
    with st.chat_message("assistant", avatar="👴"):
        with st.spinner("Professor analiz edir..."):
            try:
                # Ən son stabil Vision modeli: llama-3.2-90b-vision-preview
                response = client.chat.completions.create(
                    model="llama-3.2-90b-vision-preview",
                    messages=[{"role": "system", "content": AKIF_SYSTEM_PROMPT}] + st.session_state.messages[-MAX_HISTORY:],
                    temperature=0.7,
                    max_tokens=1024
                )
                
                ans = response.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                
            except Exception as e:
                st.error(f"Bağışla bala, texniki problem: {e}")
