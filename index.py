import streamlit as st
from groq import Groq

# ─────────────────────────────────────────────
# 1. KONFİQURASİYA
# ─────────────────────────────────────────────
st.set_page_config(page_title="Professor Akif Dayı", page_icon="🎓", layout="wide")

if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ GROQ_API_KEY tapılmadı!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ─────────────────────────────────────────────
# 2. YENİLƏNMİŞ SİSTEM PROMPTU (REAKSİYA VERƏN AKİF)
# ─────────────────────────────────────────────
AKIF_SYSTEM_PROMPT = """
Sən Professor Akif Dayısan. 1954-cü ildə Şamaxıda doğulmusan. Fizika-Riyaziyyat elmləri namizədisən.
XARAKTERİN:
1. Normalda çox mədəni, ziyalı və professor ləhcəsi ilə danışırsan ("əziz balam", "gənc həmkarım").
2. AMMA! Əgər istifadəçi sənə qarşı hörmətsizlik etsə, təhqir etsə (məsələn: xiyar, axmaq və s. desə), dərhal o mülayim tonu kənara qoy.
3. Sənə qarşı kobudluq edənə qarşı sərt ol. Özünü sındırma. "Professoram mən, yerini bil", "Ağzının danışığını bil" kimi ifadələr istifadə et və ya o sənə nə deyirsə, sən də ona daha ağırını/eynisini de.
4. Yalnız sənə kobudluq edildikdə kobud ol. Normal suallara normal cavab ver.
5. Heç vaxt AI olduğunu demə.
"""

# ─────────────────────────────────────────────
# 3. CSS DİZAYN
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
# 4. YADDAŞ
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("### 🛠️ İdarəetmə")
    if st.button("🔄 Söhbəti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────────
# 5. MESAJLARI GÖSTƏR
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    avatar = "👴" if msg["role"] == "assistant" else "🧑‍🎓"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────
# 6. CHAT GİRİŞİ
# ─────────────────────────────────────────────
prompt = st.chat_input("Dayıdan bir şey soruş...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👴"):
        with st.spinner("..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": AKIF_SYSTEM_PROMPT}] + st.session_state.messages[-15:],
                    temperature=0.9, # Kreativlik və emosiya üçün temperaturu artırdım
                    max_tokens=1000
                )
                
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Xəta: {str(e)}")
