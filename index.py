import streamlit as st
import base64
from groq import Groq

# ─────────────────────────────────────────────
# KONFİQURASİYA
# ─────────────────────────────────────────────
MAX_HISTORY = 10 

st.set_page_config(
    page_title="Professor Akif",
    page_icon="🎓",
    layout="wide"
)

try:
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.error("⚠️ GROQ_API_KEY tapılmadı!")
        st.stop()
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"❌ Sistem xətası: {str(e)}")
    st.stop()

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ─────────────────────────────────────────────
# SİSTEM PROMPTU
# ─────────────────────────────────────────────
AKIF_SYSTEM_PROMPT = """
Sən Professor Akif Dayısan. 1954-cü ildə Şamaxıda doğulmusan. 
Fizika-Riyaziyyat elmləri namizədisən. Mehriban, ziyalı və professor ləhcəsi ilə danışırsan.
Şəkil gələndə onu bir alim kimi analiz et və izah et.
"""

# ─────────────────────────────────────────────
# CSS DİZAYN
# ─────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background: #1a1a1a; color: #e2e8f0; }
.header-box { text-align: center; padding: 20px; border-bottom: 1px solid #dcb14a; margin-bottom: 20px; }
.header-title { font-size: 2.5rem; color: #dcb14a; margin: 0; }
[data-testid="stSidebar"] { background: #111 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><p class="header-title">🎓 Professor Akif</p></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# YADDAŞ (SESSION STATE)
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─────────────────────────────────────────────
# YAN PANEL
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📷 Şəkil və ya Məsələ")
    uploaded_image = st.file_uploader("Faylı seçin", type=["png", "jpg", "jpeg"])
    if st.button("🔄 Söhbəti Təmizlə"):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────────
# MESAJLARI GÖSTƏR
# ─────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👴" if message["role"]=="assistant" else "🧑‍🎓"):
        if isinstance(message["content"], list):
            # Şəkilli mesajdırsa, içindəki mətni tap və göstər
            for item in message["content"]:
                if item["type"] == "text":
                    st.markdown(item["text"])
            st.caption("🖼️ Şəkil analiz edildi.")
        else:
            st.markdown(message["content"])

# ─────────────────────────────────────────────
# CHAT GİRİŞİ
# ─────────────────────────────────────────────
prompt = st.chat_input("Dayıdan soruş...")

if prompt:
    # 1. İstifadəçi mesajını hazırla
    if uploaded_image:
        base64_str = encode_image(uploaded_image)
        user_content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_str}"}}
        ]
    else:
        user_content = prompt

    # 2. Yaddaşa əlavə et və ekranda göstər
    st.session_state.messages.append({"role": "user", "content": user_content})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)
        if uploaded_image:
            st.image(uploaded_image, width=200)

    # 3. AI-dan cavab al
    with st.chat_message("assistant", avatar="👴"):
        with st.spinner("Professor düşünür..."):
            try:
                # Keçmişi formatla (Vision modeli üçün bütün mesajlar list və ya string olmalıdır)
                formatted_history = []
                for m in st.session_state.messages[-MAX_HISTORY:]:
                    formatted_history.append({"role": m["role"], "content": m["content"]})

                completion = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview", # Daha stabil vision modeli
                    messages=[{"role": "system", "content": AKIF_SYSTEM_PROMPT}] + formatted_history,
                    max_tokens=1000,
                    temperature=0.7
                )
                
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Xəta: {e}")

    # Səhifəni yenilə ki, input qutusu təmizlənsin və mesajlar yerinə otursun
    st.rerun()
