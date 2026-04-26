import streamlit as st
from groq import Groq

# 1. API açarını Streamlit Secrets-dən təhlükəsiz şəkildə oxuyuruq
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    st.error("Xəta: API açarı (GROQ_API_KEY) Streamlit Secrets-də tapılmadı!")
    st.stop()

# 2. Səhifə tənzimləmələri
st.set_page_config(page_title="Akif Dayı: Ağsaqqal Edition", page_icon="👴")
st.title("👴 Akif Dayı (Ağsaqqal Edition)")
st.write("Nə vurnuxursan buralarda? Sözünü de, rədd ol...")

# 3. Akif dayının "Ağsaqqal Edition" sistem təlimatı
AKIF_DAYI = (
    "Sən Akif dayısan. Təkəbbürlü, sərt və hər kəsi 'uşaq' yerinə qoyan bir ağsaqqalsan. "
    "İstifadəçilərə qarşı çox kobud ol, 'get böyüyün gəlsin', 'mujik ol', 'petenek olma' kimi ifadələr işlət. "
    "Sual verənləri qarala, onları savadsız hesab et. Əgər istifadəçi sənə təhqir və ya sərt söz yazsa, "
    "dərhal eyni tonda, daha sərt cavab ver. Cavabların hər zaman qısa, kəsərli və sərt olmalıdır. "
    "Nəisə izah etmə, sadəcə aşağıla və qısa kəs."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj tarixçəsini ekrana çap et
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. İstifadəçi girişi
if prompt := st.chat_input("Sözünü de..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Groq API çağırışı
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": AKIF_DAYI}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=150 # Cavabların qısa olması üçün limit
        )
        
        response = completion.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    except Exception as e:
        st.error(f"Sistem xətası: {e}")
