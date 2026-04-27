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

# API Girişi
try:
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.error("⚠️ GROQ_API_KEY tapılmadı! Secrets hissəsini yoxla.")
        st.stop()
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"❌ API Bağlantı xətası: {str(e)}")
    st.stop()

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ─────────────────────────────────────────────
# SİSTEM PROMPTU (Professor Ruhu)
# ─────────────────────────────────────────────
AKIF_SYSTEM_PROMPT = """
Sən Professor Akif Dayısan. 1954-cü ildə Şamaxıda doğulmusan. 
Fizika-Riyaziyyat elmləri namizədisən. Mehriban, ziyalı və bir az köhnə sovet professoru tərzində danışırsan.
Şəkil gələndə onu bir alim kimi incələ və dərindən izah et. İnsanlara qarşı çox nəzakətli ol.
"""

# ─────────────────────────────────────────────
# CSS DİZAYN
# ─────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background: #1a1a1a; color: #e2e8f0; }
.header-box { text-align: center; padding: 20px; border-bottom: 2px solid #dcb14a; margin-bottom: 20px; }
.header-title { font-size: 2.5rem; color: #dcb14a; margin: 0; font-family: 'serif'; }
[data-testid="stSidebar"] { background: #111 !important; border-right: 1px solid #dcb14a; }
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
    st.markdown("### 📷 Şəkil/Məsələ Əlavə Et")
    uploaded_image = st.file_uploader("Faylı seçin (Opsional)", type=["png", "jpg", "jpeg"])
    st.info("Əgər məsələ şəkli atırsınızsa, aşağıdan 'Dayı buna bax' yazıb göndərin.")
    
    if st.button("🔄 Söhbəti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────────
# MESAJLARI EKRANDA GÖSTƏR
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
        base_4_image = encode_image(uploaded_image)
        current_user_content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base_4_image}"}}
        ]
    else:
        current_user_content = prompt

    # 2. İstifadəçi mesajını ekranda göstər və yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": current_user_content})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)
        if uploaded_image:
            st.image(uploaded_image, width=300)

    # 3. AI-dan cavab al
    with st.chat_message("assistant", avatar="👴"):
        message_placeholder = st.empty()
        with st.spinner("Professor Akif düşünür və analiz edir..."):
            try:
                # Keçmiş mesajları vision modelinə uyğun formata salırıq
                chat_history = []
                for m in st.session_state.messages[-MAX_HISTORY:]:
                    chat_history.append({"role": m["role"], "content": m["content"]})

                # Vision modeli çağırırıq
                response = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{"role": "system", "content": AKIF_SYSTEM_PROMPT}] + chat_history,
                    temperature=0.7,
                    max_tokens=1000
                )
                
                full_response = response.choices[0].message.content
                message_placeholder.markdown(full_response)
                
                # Cavabı yaddaşa əlavə et
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Bağışla bala, bir az texniki problem oldu: {e}")

    # Vacib: Kod bitəndə deyil, yalnız proses tam bitəndə rerun lazımdırsa istifadə edilə bilər.
    # Bu versiyada chat_input özü avtomatik yenilədiyi üçün rerun-a çox vaxt ehtiyac qalmır.
