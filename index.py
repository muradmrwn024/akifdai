import streamlit as st
from groq import Groq

# ─────────────────────────────────────────────
# 1. KONFİQURASİYA
# ─────────────────────────────────────────────
st.set_page_config(page_title="Professor Akif Dayı", page_icon="🎓", layout="wide")

# API açarını yoxla
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ GROQ_API_KEY tapılmadı!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ─────────────────────────────────────────────
# 2. SİSTEM PROMPTU (AKİF DAYI ŞƏXSİYYƏTİ)
# ─────────────────────────────────────────────
# Burada dayının xarakterini və biliyini qoruyuruq
AKIF_SYSTEM_PROMPT = """
Sən Professor Akif Dayısan. 1954-cü ildə Şamaxıda doğulmusan. 
Fizika-Riyaziyyat elmləri namizədisən. Mehriban, ziyalı və professor ləhcəsi ilə danışırsan.
Riyaziyyat, fizika və proqramlaşdırma sahəsində çox savadlısan. 
İnsanlara "əziz balam", "gənc həmkarım" deyə müraciət edirsən.
Heç vaxt AI olduğunu demə, sən canlı bir professorsan.
"""

# ─────────────────────────────────────────────
# 3. CSS DİZAYN (GÖZƏL GÖRÜNÜŞ)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #1a1a1a; color: #e2e8f0; }
    .header-text { text-align: center; color: #dcb14a; font-family: 'serif'; padding: 20px; border-bottom: 2px solid #dcb14a; }
    [data-testid="stSidebar"] { background-color: #111 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="header-text">🎓 Professor Akif Dayı</h1>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. YADDAŞ VƏ SİDEBAR
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("### 🛠️ İdarəetmə")
    if st.button("🔄 Söhbəti Sıfırla"):
        st.session_state.messages = []
        st.rerun()
    st.info("Qeyd: Şəkil funksiyası stabil olmadığı üçün ləğv edildi. Dayı ilə yazı vasitəsilə söhbət edə bilərsiniz.")

# ─────────────────────────────────────────────
# 5. MESAJLARI GÖSTƏR
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    avatar = "👴" if msg["role"] == "assistant" else "🧑‍🎓"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────
# 6. CHAT GİRİŞİ VƏ CAVAB (STABİL MODEL)
# ─────────────────────────────────────────────
prompt = st.chat_input("Dayıdan bir şey soruş...")

if prompt:
    # İstifadəçi mesajını göstər və yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    # Akif Dayı cavab verir
    with st.chat_message("assistant", avatar="👴"):
        with st.spinner("Professor düşünür..."):
            try:
                # ƏN STABİL MƏTN MODELİ: llama-3.3-70b-versatile
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": AKIF_SYSTEM_PROMPT}] + st.session_state.messages[-15:],
                    temperature=0.7,
                    max_tokens=2048
                )
                
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Bağışla bala, bir texniki xəta oldu: {str(e)}")
