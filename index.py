import streamlit as st
from groq import Groq

# API açarını bura yerləşdir
client = Groq(api_key="api_key=st.secrets["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"]")

st.set_page_config(page_title="Akif Dayı AI", page_icon="👴")
st.title("👴 Akif Dayı")
st.write("Cavanlıq əldən gedir, ay bala... Nəsə sualın var?")

# Akif dayının xarakteri
AKIF_DAYI = "Sən Akif dayısan, 65+ yaşlı, deyingən amma məlumatlı sovet adamısan. 'Bizim vaxtımızda' deyə başlayıb nəsihət verirsən."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Dayıya sözünü de..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": AKIF_DAYI}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        response = completion.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"Xəta: {e}")







