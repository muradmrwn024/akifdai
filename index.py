import streamlit as st
import base64
from groq import Groq

# ─────────────────────────────────────────────
# 1. KONFİQURASİYA VƏ API
# ─────────────────────────────────────────────
st.set_page_config(page_title="Professor Akif Dayı", page_icon="🎓", layout="wide")

if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ API açarı tapılmadı! Lütfən secrets bölməsini yoxlayın.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ─────────────────────────────────────────────
# 2. SİSTEM PROMPTU
# ─────────────────────────────────────────────
AKIF_SYSTEM_PROMPT = """
Sən Professor Akif Dayısan. 1954-cü ildə Şamaxıda doğulmusan. 
Fizika-Riyaziyyat elmləri namizədisən. Mehriban, ziyalı və professor ləhcəsi ilə danışırsan.
Gələn şəkilləri bir alim kimi incələ və ətraflı izah et. Heç vaxt AI olduğunu demə.
"""

# ─────────────────────────────────────────────
# 3. YADDAŞ (SESSION STATE)
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─────────────────────────────────────────────
# 4. YAN PANEL (SIDEBAR)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📷 Şəkil/Məsələ Yüklə")
    uploaded_file = st.file_uploader("Şəkil seçin...", type=['png', 'jpg', 'jpeg'])
    if st.button("🔄 Söhbəti Təmizlə"):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────────
# 5. EKRANDA GÖSTƏRMƏ
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👴" if msg["role"]=="assistant" else "🧑‍🎓"):
        if isinstance(msg["content"], list):
            for part in msg["content"]:
                if part["type"] == "text":
                    st.markdown(part["text"])
        else:
            st.markdown(msg["content"])

# ─────────────────────────────────────────────
# 6. ƏSAS MƏNTİQ
# ─────────────────────────────────────────────
prompt = st.chat_input("Sualınızı bura yazın...")

if prompt:
    # İstifadəçi mesajını hazırla
    if uploaded_file:
        img_b64 = encode_image(uploaded_file)
        user_content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
        ]
    else:
        user_content = [{"type": "text", "text": prompt}]

    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)
        if uploaded_file:
            st.image(uploaded_file, width=300)

    # Akif Dayı Cavab Verir
    with st.chat_message("assistant", avatar="👴"):
        with st.spinner("Professor düşünür..."):
            try:
                # KRİTİK DƏYİŞİKLİK: Hazırda Groq-da ən stabil vision modeli budur
                # Əgər bu da xəta versə "llama-3.2-11b-vision-preview" yazaraq yoxlayın
                model_name = "llama-3.2-90b-vision-preview" 
                
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "system", "content": AKIF_SYSTEM_PROMPT}] + st.session_state.messages[-10:],
                    max_tokens=1024
                )
                
                final_text = response.choices[0].message.content
                st.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
                
            except Exception as e:
                # Əgər 90b yenə xəta versə, avtomatik 11b-ni yoxlamaq üçün ehtiyat plan:
                try:
                    response = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[{"role": "system", "content": AKIF_SYSTEM_PROMPT}] + st.session_state.messages[-10:],
                    )
                    final_text = response.choices[0].message.content
                    st.markdown(final_text)
                    st.session_state.messages.append({"role": "assistant", "content": final_text})
                except:
                    st.error(f"Xəta: Modellər hazırda Groq tərəfindən yenilənir. Bir az sonra yoxlayın. {str(e)}")
