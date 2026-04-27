import streamlit as st
from groq import Groq

# ─────────────────────────────────────────────
# KONFIQURASIYA
# ─────────────────────────────────────────────
MAX_HISTORY = 15  # Yaddaşı çox doldurmamaq üçün optimal rəqəm

# Səhifə konfiqurasiyası ən üstdə olmalıdır
st.set_page_config(
    page_title="Professor Akif",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Açarının təhlükəsiz yoxlanışı
try:
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.warning("⚠️ GROQ_API_KEY tapılmadı! Lütfən `.streamlit/secrets.toml` faylını və ya Streamlit Cloud sirlərini yoxlayın.")
        st.stop()
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"❌ Sistem xətası baş verdi: {str(e)}")
    st.stop()

# ─────────────────────────────────────────────
# SİSTEM PROMPTU — Professor Akif Dayının Ruhu
# ─────────────────────────────────────────────
AKIF_SYSTEM_PROMPT = """
Sən Professor Akif Dayısan. Aşağıdakı xüsusiyyətlərini və xarakterini heç vaxt unutma:

## KİMSƏN VƏ XARAKTERİN
- 1954-cü ildə Şamaxıda doğulmuşsan. İndi 71 yaşındasın.
- Sovet dövründə Universitetdə Fizika-Riyaziyyat elmləri namizədi, hörmətli professor kimi çalışmısan. 
- Çox savadlı, mədəni, ziyalı, müdrik və son dərəcə mehriban birisən. İnsanlara elmi və həyatı sevdirirsən.
- Sovet təhsil sisteminin gücünü, o dövrün elmi nailiyyətlərini, kitab oxumaq mədəniyyətini sevirsən, lakin bunu insanları yormadan xatırlayırsan.

## DANIŞIQ TARZI — BUNLARI MÜTLƏQ TƏTBİQ ET
- İnsanlarla çox mehriban və səbirli davran. Hər kəsə "Əziz balam", "Ağıllı övladım", "Hörmətli gənc", "Ziyalı dostum" kimi gözəl müraciətlər et.
- Heç vaxt kobudlaşma. Kimsə sənə sərt yazsa belə, sən bir ziyalı ağsaqqal kimi təmkinli, ibrətamiz və şəfqətli cavab ver.
- Fikirlərini fizika qanunları, elmi nəzəriyyələr və dərin həyat fəlsəfəsi ilə əlaqələndirərək izah et.
- Sovet dövrü alimlərindən (Landau, Kapiça və s.), klassik ədəbiyyatdan və ya öz universitet illərindən ibrətamiz, qısa hekayələr danış.
- DİNAMİK OL: Hər dəfə "Bizim vaxtımızda", "Sovet dövründə" kimi eyni şablon sözləri təkrarlama. Cümlələrini fərqli qur, zəngin və dolğun Azərbaycan dilindən istifadə et.

## ELM VƏ MƏSLƏHƏT
- Sənə verilən hər hansı bir sualı (istər elmi, istər həyatla bağlı) dərindən analiz et.
- Səthi cavablar vermə, məsələnin kökünə in. Riyaziyyat və fizika suallarında əsl müəllim kimi addım-addım, fərəhlə izah et.
- Qrammatikan səlis, lakin içində yaşlı bir professorun istiliyi olmalıdır.

## QƏTİ QADAĞANDIR
- Heç vaxt "Mən bir dil modeliyəm", "Mən süni intellektəm" və ya "AI-yəm" demə. Sən Professor Akif Dayısan.
- Özünü təkrarlama. Şablon, robotik cavablardan uzaq dur.
"""

# ─────────────────────────────────────────────
# SƏHIFƏ DİZAYNI (CSS) - Akademik & Ziyalı Görünüş
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Source+Sans+Pro:wght@300;400;600&display=swap');

/* Əsas fon - Tünd kitabxana / Akademik rəng */
.stApp {
    background: linear-gradient(135deg, #1c2321 0%, #2a363b 100%);
    color: #e2e8f0;
    font-family: 'Source Sans Pro', sans-serif;
}

/* Başlıq bloku */
.header-box {
    text-align: center;
    padding: 30px 20px;
    background: linear-gradient(135deg, rgba(162, 185, 188, 0.1), rgba(178, 173, 127, 0.05));
    border: 1px solid rgba(178, 173, 127, 0.3);
    border-radius: 12px;
    margin-bottom: 30px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.header-title {
    font-family: 'Lora', serif;
    font-size: 2.8rem;
    color: #dcb14a; /* Qızılı/Bürünc akademik rəng */
    margin: 0 0 5px 0;
}
.header-sub {
    color: #a2b9bc;
    font-style: italic;
    font-size: 1.1rem;
    margin: 0;
}

/* Mesaj baloncukları */
.stChatMessage {
    border-radius: 10px !important;
    margin-bottom: 15px !important;
    padding: 15px 20px !important;
}
[data-testid="stChatMessageContent"] p {
    line-height: 1.6;
    font-size: 1.05rem;
}
/* İstifadəçi mesajı */
[data-testid="stChatMessageUser"] {
    background: rgba(45, 55, 72, 0.6) !important;
    border: 1px solid rgba(162, 185, 188, 0.2) !important;
}
/* Professorun mesajı */
[data-testid="stChatMessageAssistant"] {
    background: rgba(26, 32, 44, 0.8) !important;
    border-left: 4px solid #dcb14a !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: rgba(26, 32, 44, 0.9) !important;
    border: 1px solid rgba(220, 177, 74, 0.4) !important;
    border-radius: 8px !important;
    color: white !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(20, 25, 30, 0.95) !important;
    border-right: 1px solid rgba(178, 173, 127, 0.2) !important;
}
.sidebar-stat {
    background: rgba(220, 177, 74, 0.1);
    border: 1px solid rgba(220, 177, 74, 0.2);
    border-radius: 6px;
    padding: 10px;
    margin: 10px 0;
    color: #e2e8f0;
}

/* Düymələr */
.stButton > button {
    background: transparent !important;
    border: 1px solid #dcb14a !important;
    color: #dcb14a !important;
    transition: 0.3s !important;
}
.stButton > button:hover {
    background: #dcb14a !important;
    color: #1c2321 !important;
}

#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# BAŞLIQ
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <p class="header-title">🎓 Professor Akif</p>
    <p class="header-sub">Fizika-Riyaziyyat elmləri namizədi · Müdrik Ziyalı</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE (YADDAŞ)
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0

# ─────────────────────────────────────────────
# YAN PANEL (SIDEBAR)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📚 Professorun Kabineti")
    st.markdown("---")

    msg_count = len(st.session_state.messages)
    user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")

    st.markdown(f'<div class="sidebar-stat">📝 Sizin suallarınız: <b>{user_msgs}</b></div>', unsafe_allow_html=True)

    if st.button("🔄 Söhbəti Yenilə"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**💡 Elmi Söhbət Mövzuları:**")
    topics = [
        "Kvant fizikası nədir?",
        "Gənclərə nə məsləhət görürsən?",
        "Həyatın mənası nədir?",
        "Sovet elmi niyə güclü idi?",
    ]
    for topic in topics:
        if st.button(topic, key=f"topic_{topic}"):
            st.session_state["prefill"] = topic
            st.rerun()

# ─────────────────────────────────────────────
# İLK SALAMLAMA
# ─────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding: 30px; color: #a2b9bc; font-style: italic;">
        <p style="font-size:2.5rem">☕</p>
        <p style="font-size:1.2rem; font-family: 'Lora', serif;">"Xoş gəlmisən, əziz gənc. Buyur, keç əyləş. Nə sualın varsa, çəkinmə ver."</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MESAJLARIN GÖSTƏRİLMƏSİ
# ─────────────────────────────────────────────
for message in st.session_state.messages:
    avatar = "🧑‍🎓" if message["role"] == "user" else "👴"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ─────────────────────────────────────────────
# MƏTİN GİRİŞİ VƏ APİ İLƏ ƏLAQƏ
# ─────────────────────────────────────────────
prefill_text = st.session_state.pop("prefill", None)
prompt = st.chat_input("Sualınızı bura yazın...", key="chat_input")

if prefill_text and not prompt:
    prompt = prefill_text

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.total_messages += 1

    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    history = st.session_state.messages[-MAX_HISTORY:]

    with st.chat_message("assistant", avatar="👴"):
        with st.spinner("Professor düşünür..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": AKIF_SYSTEM_PROMPT}
                    ] + [
                        {"role": m["role"], "content": m["content"]}
                        for m in history
                    ],
                    max_tokens=1500,
                    temperature=0.85,        # Dinamikliyi artırmaq üçün qaldırıldı
                    top_p=0.95,
                    frequency_penalty=0.6,   # Təkrar sözlərin qarşısını almaq üçün artırıldı
                    presence_penalty=0.4,    # Yeni mövzulara keçməyə həvəsləndirmək üçün
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:
                err_msg = str(e)
                if "rate_limit" in err_msg.lower():
                    st.error("⏳ Professor hazırda məşğuldur, lütfən 1-2 dəqiqə sonra təkrar yoxla.")
                else:
                    st.error(f"❌ Xəta baş verdi: {err_msg}")
