import streamlit as st
from groq import Groq

# 1. API açarı idarəetməsi
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    st.error("Xəta: API açarı tapılmadı!")
    st.stop()

# 2. Səhifə Tənzimləmələri və CSS (Arayüzü gözəlləşdirən hissə)
st.set_page_config(page_title="Akif Dayı: Universal Edition", page_icon="👴", layout="centered")

# BURADA SAYTIN GÖRÜNÜŞÜNÜ DƏYİŞİRİK
st.markdown("""
    <style>
    /* Ümumi fon rəngi (Klassik köhnə kağız/krem rəngi) */
    .stApp {
        background-color: #f4f1ea;
    }
    
    /* Başlıq rəngi */
    h1 {
        color: #4a3728;
        font-family: 'Georgia', serif;
        text-align: center;
        border-bottom: 2px solid #4a3728;
        padding-bottom: 10px;
    }

    /* Mesaj qutularının yuvarlaqlaşdırılması */
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }

    /* İstifadəçi mesajı */
    [data-testid="stChatMessageUser"] {
        background-color: #d1e7dd !important;
        border: 1px solid #0f5132;
    }

    /* Akif dayının mesajı */
    [data-testid="stChatMessageAssistant"] {
        background-color: #fff !important;
        border: 1px solid #4a3728;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    /* Input (yazı yazılan yer) dizaynı */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👴 Akif Dayı: Universal Mentor")

# 3. Akif dayının təlimatı (Əvvəlki balanslı versiya)
AKIF_DAYI_PROMPT = (
    "Sən Akif dayısan. 70 yaşlı, savadlı, təkəbbürlü və həyat görmüş azərbaycanlı ağsaqqalsan. "
    "Dərd dinləməyi, elmi izahları və yeri gələndə sərt olmağı bacarırsan. "
    "QAYDA: Harada işlədiyini soruşsalar 'Seyid ocağında işləyirdim' de."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekrana çıxar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Giriş və Cavab
if prompt := st.chat_input("Dayıya sözünü de..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": AKIF_DAYI_PROMPT}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=600,
            temperature=0.6
        )
        
        response = completion.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    except Exception as e:
        st.error(f"Xəta: {e}")
