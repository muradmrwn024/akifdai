import streamlit as st
from groq import Groq

# 1. API açarı idarəetməsi
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    st.error("Xəta: API açarı tapılmadı!")
    st.stop()

# 2. Üst Səviyyə Arayüz Dizaynı
st.set_page_config(page_title="Akif Dayı: Universal Mentor", page_icon="👴", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle, #1e1e1e 0%, #121212 100%);
        color: #f0f0f0;
    }
    .header-container {
        padding: 40px;
        text-align: center;
        background: rgba(212, 175, 55, 0.05);
        border-radius: 20px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        margin-bottom: 30px;
    }
    .main-title {
        font-family: 'Garamond', serif;
        color: #d4af37;
        font-size: 3.5rem;
        letter-spacing: 3px;
        text-shadow: 3px 3px 6px #000;
        margin: 0;
    }
    .stChatMessage {
        border-radius: 15px !important;
        margin-bottom: 20px !important;
        padding: 15px !important;
    }
    [data-testid="stChatMessageUser"] {
        background-color: #2b2b2b !important;
        border: 1px solid #444 !important;
    }
    [data-testid="stChatMessageAssistant"] {
        background-color: #1a1a1a !important;
        border-left: 6px solid #d4af37 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="header-container">
        <p class="main-title">👴 AKİF DAYI</p>
        <p style="color: #b0b0b0; font-style: italic;">"Sözün canını anlayan, ruhunu oxuyan ağsaqqal"</p>
    </div>
    """, unsafe_allow_html=True)

# 3. AKİF DAYI SİSTEMİ
AKIF_DAYI_PROMPT = (
    "Sən Akif dayısan. 70 yaşlı, savadlı, sovet təhsilli və insanların duyğularını sətiraltı anlayan bir azərbaycanlı kişisən. "
    "MİSSİYAN: İstifadəçinin yazdığı mətndən onun duyğusunu hiss et və cavabını buna görə tənzimlə. "
    "1. KƏDƏR: Şəfqətli ağsaqqal nəsihəti ver. 'Həyatdır bala, biz nə günlər görmüşük' de. "
    "2. SEVİNC: 'Afərin' de, təkəbbürlə xeyir-dua ver. "
    "3. QƏZƏB/SÖYÜŞ: Dərhal sərtləş, daha ağır küçə ağzı ilə cavab ver, 'mujik ol', 'petenek olma' de. "
    "4. ELM/RİYAZİYYAT: Biliklərini təkəbbürlə nümayiş etdir. "
    "5. SEYİD OCAĞI: Yalnız iş yeri soruşulanda 'Seyid ocağında işləyirdim' de. "
    "DİQQƏT: Azərbaycan dilində qrammatik səhv etmə ('işləməmişəm' yox, 'işləmirəm')."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ürəyində nə var, de görüm..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": AKIF_DAYI_PROMPT}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=1000,
            temperature=0.65
        )
        response = completion.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"Sistem xətası: {e}")

# Sidebar
with st.sidebar:
    st.header("⚙️ Dayının Otağı")
    if st.button("Söhbəti Sıfırla"):
        st.session_state.messages = []
        st.rerun()
