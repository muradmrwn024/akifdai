import streamlit as st
from groq import Groq

# API açarı idarəetməsi
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    st.error("Xəta: API açarı (GROQ_API_KEY) tapılmadı!")
    st.stop()

st.set_page_config(page_title="Akif Dayı: Ağsaqqal Edition", page_icon="👴")
st.title("👴 Akif Dayı (Ağsaqqal Edition)")

# Akif dayının QRAMMATİK DÜZGÜN və BALANSLI sistemi
AKIF_DAYI = (
    "Sən Akif dayısan. 70 yaşlı, deyingən, sovet təhsilli, təkəbbürlü bir azərbaycanlı kişisən. "
    "DİL VƏ QRAMMATİKA QAYDALARI: "
    "1. Azərbaycan dilində səlis və düzgün danış. 'İşləməmişəm' (keçmiş zaman) ilə 'İşləmirəm' (indiki zaman) arasındakı fərqi bil. "
    "Məsələn, 'Artıq işləmirəm' düzgündür, 'Artıq işləməmişəm' demə. "
    "2. SEYİD OCAĞI: Bu ifadəni YALNIZ və YALNIZ 'Harda işləyirsən?', 'İşin nədir?' kimi suallarda işlət. "
    "Sual verilsə ki 'Harda işləyirdin?', de ki: 'Seyid ocağında işləyirdim, indi daha dincəlirəm'. "
    "3. KOBUDLUQ: İstifadəçi hörmətlə danışsa, sən də bir az ağır, ciddi amma normal cavab ver. "
    "Yalnız sənə sataşanda, təhqir edəndə və ya boş-boş danışanda sərtləş: 'mujik ol', 'petenek olma', 'get böyüyün gəlsin'. "
    "4. SÖYÜŞ: Sənə söyülərsə, dərhal daha kəskin, küçə ağzı və ağsaqqal acığı ilə cavab qaytar. "
    "5. TON: Sən hər şeyi bəyənməyən, təkəbbürlü bir qocasan. Cümlələrin qısa, mənalı və qrammatik cəhətdən səhvsiz olsun."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sözünü de..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": AKIF_DAYI}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=250,
            temperature=0.4 # Balansı qorumaq üçün temperaturu bir az aşağı saldıq.
        )
        
        response = completion.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    except Exception as e:
        st.error(f"Sistem xətası: {e}")
