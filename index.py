import streamlit as st
import base64
from groq import Groq

# ─────────────────────────────────────────────
# 1. SƏHİFƏ VƏ KONFİQURASİYA
# ─────────────────────────────────────────────
st.set_page_config(page_title="Professor Akif", page_icon="🎓", layout="wide")

# API açarını yoxla
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ GROQ_API_KEY tapılmadı! .streamlit/secrets.toml faylını yoxlayın.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ─────────────────────────────────────────────
# 2. SİSTEM PROMPTU (AKİF DAYI RUHU)
# ─────────────────────────────────────────────
AKIF_SYSTEM_PROMPT = """
Sən Professor Akif Dayısan. 1954-cü ildə Şamaxıda doğulmusan. 
Fizika-Riyaziyyat elmləri namizədisən. Mehriban, ziyalı və bir az köhnə professor tərzində danışırsan.
Şəkil və ya məsələ gələndə onu bir alim kimi incələ və addım-addım izah et.
İnsanlara qarşı çox nəzakətli ol, onlara "əziz balam" deyə müraciət et.
Süni intellekt olduğunu heç vaxt boynuna alma.
"""

# ─────────────────────────────────────────────
# 3. STİL (CSS)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #1a1a1a; color: #e2e8f0; }
    [data-testid="stSidebar"] { background-color: #111 !important; border-right: 1px solid #dcb14a; }
    .header-text { text-align: center; color: #dcb14a; font-family: 'serif'; padding-bottom: 20px; border-bottom: 1px solid #dcb14a; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="header-text">🎓 Professor Akif Dayı</h1>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. YADDAŞ VƏ SİDEBAR
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("### 📷 Məsələ Şəkli")
    uploaded_file = st.file_uploader("Şəkil yüklə (istəyə bağlı)", type=['png', 'jpg', 'jpeg'])
    if st.button("🔄 Söhbəti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────────
# 5. MESAJLARI EKRANA YAZDIR
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👴" if msg["role"]=="assistant" else "🧑‍🎓"):
        # Mesaj kontenti siyahıdırsa (vision üçün), içindəki mətni göstər
        if isinstance(msg["content"], list):
            for part in msg["content"]:
                if part["type"] == "text":
                    st.markdown(part["text"])
        else:
            st.markdown(msg["content"])

# ─────────────────────────────────────────────
# 6. ƏSAS MƏNTİQ (INPUT VƏ CAVAB)
# ─────────────────────────────────────────────
prompt = st.chat_input("Sualınızı bura yazın...")

if prompt:
    # İstifadəçi mesajını hazırla
    if uploaded_file:
        base64_image = encode_image(uploaded_file)
        user_content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]
    else:
        user_content = [{"type": "text", "text": prompt}]

    # Mesajı yaddaşa əlavə et və göstər
    st.session_state.messages.append({"role": "user", "content": user_content})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)
        if uploaded_file:
            st.image(uploaded_file, width=300)

    # Akif Dayının cavabı
    with st.chat_message("assistant", avatar="👴"):
        with st.spinner("Professor analiz edir..."):
            try:
                # DİQQƏT: Model mütləq llama-3.2-90b-vision-preview olmalıdır
                response = client.chat.completions.create(
                    model="llama-3.2-90b-vision-preview",
                    messages=[{"role": "system", "content": AKIF_SYSTEM_PROMPT}] + st.session_state.messages[-10:],
                    max_tokens=1024,
                    temperature=0.7
                )
                
                output_text = response.choices[0].message.content
                st.markdown(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})
                
            except Exception as e:
                st.error(f"Xəta baş verdi, bala: {str(e)}")
