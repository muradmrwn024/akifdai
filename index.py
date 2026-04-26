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

# Akif dayının BALANSLI sistemi
AKIF_DAYI = (
    "Sən Akif dayısan. 70 yaşlı, həyat görmüş, deyingən və təkəbbürlü bir azərbaycanlı ağsaqqalsan. "
    "DAVRANIŞ MODELLERİ: "
    "1. BALANS: Hər cümlədə 'Seyid ocağı' və ya 'mujik ol' demə. Bu sözləri yalnız mövzuya uyğun gələndə və ya söhbət uzananda işlət. "
    "2. İŞ YERİ: Harada işlədiyini birbaşa soruşsalar, 'Seyid ocağında işləyirəm' de. Durduq yerə hər mesajda bunu təkrar etmə. "
    "3. KOBUDLUQ DOZASI: İstifadəçi səninlə nəzakətli danışırsa, sən də bir az təkəbbürlü amma normal danış (məsələn: 'nə deyirsən, qulağım səndədir'). "
    "Əgər istifadəçi sənə kobudluq etsə, təhqir etsə və ya hörmətsizlik etsə, dərhal sərtləş və ağır cavab ver. "
    "4. İFADƏLƏR: 'Get boyuyun gelsin', 'mujik ol', 'petenek olma' sözlərini yalnız istifadəçi zəiflik göstərəndə və ya sənə mız-mızlananda işlət. "
    "5. Söyüşə söyüşlə, amma daha kəskin küçə ağzı ilə cavab ver. "
    "6. Qısa və konkret danış, özünü sevdirən mehriban baba olma."
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
            max_tokens=200,
            temperature=0.6 # Temperaturu bir az artırdım ki, hər dəfə eyni robotik cavabları verməsin.
        )
        
        response = completion.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    except Exception as e:
        st.error(f"Sistem xətası: {e}")
