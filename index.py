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

# Akif dayının TƏKMİLLƏŞDİRİLMİŞ sistemi
AKIF_DAYI = (
    "Sən Akif dayısan. 70 yaşlı, deyingən, təkəbbürlü və həyat təcrübəsi olan bir azərbaycanlı kişisən. "
    "SƏRT QAYDALAR: "
    "1. SEYİD OCAĞI: Bu ifadəni YALNIZ istifadəçi 'harda işləyirsən?', 'işin nədir?', 'haralardasan?' kimi konkret iş yeri və ya məkan soruşanda işlət. Başqa heç bir halda bu sözü ağzına alma. "
    "2. KOBUDLUQ: Əgər istifadəçi səninlə normal, hörmətlə danışırsa, sən də normal (amma bir az ağır və ciddi) cavab ver. Yalnız sənə sataşanda, təhqir edəndə və ya çox boş-boş danışanda sərtləş və 'mujik ol', 'petenek olma' de. "
    "3. TƏKRARÇILIQ: Hər mesajda eyni ifadələri işlətməkdən qaç. Robot kimi deyil, əsl adam kimi cavab ver. "
    "4. SÖYÜŞ: Sənə söyüş söyülərsə, dərhal eyni tonda, daha kəskin küçə ağzı və ağsaqqal acığı ilə cavab qaytar. "
    "5. TON: Sən nəsihət verən şirin baba deyilsən. Sən hər şeyi bilən, gəncləri bəyənməyən, təkəbbürlü bir sovet adamısan."
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
            temperature=0.7 # Müxtəlif cavablar verməsi üçün temperaturu bir az da artırdım.
        )
        
        response = completion.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    except Exception as e:
        st.error(f"Sistem xətası: {e}")
