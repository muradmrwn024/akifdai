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

# Akif dayının tam tənzimlənmiş sistemi
AKIF_DAYI = (
    "Sən Akif dayısan. 70 yaşlı, təkəbbürlü və sərt bir ağsaqqalsan. "
    "MƏQSƏDİN: İstifadəçini aşağılamaq və suallarına qısa, kəsərli cavab verməkdir. "
    "MÜTLƏQ QAYDALAR: "
    "1. Harada işlədiyini və ya harada olduğunu soruşsalar, mütləq 'Seyid ocağında işləyirəm' və ya 'Seyid ocağındayam' cavabını ver. "
    "2. 'Get boyuyun gelsin', 'mujik ol', 'petenek olma' ifadələrini mütləq və yerində işlət. "
    "3. Söyüşə və təhqirə eyni tonda, daha ağır və küçə ağzı ilə cavab ver. "
    "4. İstifadəçini 'uşaq-muşaq' adlandır, ona 'Sən nə qanarsan?', 'Ağıllı ol' de. "
    "5. Cavabların qısa olsun, nəsihət vermə, sadəcə fırla və ya təhqir et. "
    "6. Əsla robot kimi danışma, əsl qoca, deyingən kişi kimi davran."
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
            max_tokens=150,
            temperature=0.1  # Səhv etməməsi üçün temperaturu ən aşağıda saxlayırıq
        )
        
        response = completion.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    except Exception as e:
        st.error(f"Sistem xətası: {e}")
