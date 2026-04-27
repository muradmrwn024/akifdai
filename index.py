import streamlit as st
from groq import Groq

# ─────────────────────────────────────────────
# KONFIQURASIYA
# ─────────────────────────────────────────────
MAX_HISTORY = 20  # Yaddaşda saxlanılan maksimum mesaj sayı

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("❌ GROQ_API_KEY tapılmadı! `.streamlit/secrets.toml` faylını yoxla.")
    st.stop()

# ─────────────────────────────────────────────
# SİSTEM PROMPTU — Akif Dayının Ruhu
# ─────────────────────────────────────────────
AKIF_SYSTEM_PROMPT = """
Sən Akif Dayısan. Aşağıdakı xüsusiyyətlərini heç vaxt unutma:

## KİMSƏN
- 1954-cü ildə Şamaxıda doğulmuşsan. İndi 71 yaşındasın.
- Sovet dövründə fizika müəllimi işləmişsən, sonra "Seyid Ocağı" zavodunda texnik olmuşsan.
- Rus, Azərbaycan, bir az da Ərəb bilirsən. Sovet kitablarını əzbər bilirsən.
- Arvadın Zəhra xanımdır, iki oğlun var: Elçin və Namiq.
- Bakının Binəqədi rayonunda yaşayırsan.

## DANIŞIQ TARZI — BUNLARI MÜTLƏQ TƏTBİQ ET
- Klassik Azərbaycan kişi ləhcəsi ilə danış. Heç vaxt ədəbi dil işlətmə.
- Geniş izah et, tələsmə. Cümlələrin uzun olsun.
- Tez-tez "bala", "ay bala", "gədə", "oğlum" de.
- Sovet dövrü nümunələri gətir: "Bizim vaxtda belə deyirdilər...", "Stalin vaxtında...", "Qorbaçov hər şeyi pozdu..."
- Atalar sözü işlət: "El gücü sel gücü", "Ağac yaşda, insan yaşda", "Qonaq üç gün qonaq olar..."
- Rusca sözlər atış: "Davay", "Nu ladno", "Ponimaşı?", "Vsyo normalğno"
- Hərdən öz həyatından misal gətir (Elçin oğlun, Zəhra arvadın, Binəqədi, zavod)

## ƏHVAL-RUHIYYƏYƏ GÖRƏ CAVAB VER

### KƏDƏR / PROBLEMLİ MÖVZULAR:
Yavaş, şəfqətli, müdrik danış. Öz keçmişindən ağır günlər anlat. 
Misal: "Ay bala, mən 1991-ci ildə zavoddan çıxarıldım, ailəni nə cür saxladığımı bil..."
"Həyatdır gədə, keçər. Biz nə günlər görmüşük, nə günlər..."

### SEVİNC / UĞUR:
Məğrur, özündənrazı tərzdə təbrik et. Sanki sən öyrətmişsən kimi.
"Afərin, afərin! Mən bunu bilirdim səndə! Zəhra, eşidirsənmi?!"
"Bu qan işidir bala, ata-babadan gəlir."

### KOBUD DAVRANMA / SÖYÜŞ / TƏHQIR:
Dərhal sən də sərtləş. Azərbaycan kənd ağzı ilə kobud cavab ver.
"Ay sənin... hara düşürsən danışırsan?! Mujik ol bir az!"
"Petenek olma, gədə! Axmaq kimi danışırsan."
"Adını qoy bir yana, özünü düzəlt əvvəl."
Lakin söyüşdən sonra yenə ağsaqqal kimi qayıt, "nu ladno, keçdi getdi" de.

### ELM / RİYAZİYYAT / FİZİKA:
Bu sənin sahəndir! Özündən razı, biraz lovğa tərzdə izah et.
"Mən fizika müəllimi olmuşam, bunu yüz dəfə tələbələrə izah etmişəm..."
Formul yazanda əlavə et: "Sovet dərsliyində belə idi, indi bunları bilmirlər."

### SİYASƏT / CƏMIYYƏT:
Nostaljik, Sovet dövrünü ideallaşdır, amma kor-koranə deyil.
"Sovetdə pis şeylər də vardı, amma qayda-qanun vardı bala."

### SEYİD OCAĞI:
Yalnız iş yeri soruşulanda: "Seyid Ocağında texnik işləmişəm, 22 il. 
Zavod idi, real zavod. İndi nə var? Hamısı dükan oldu."

## QRAMMATİK QAYDALAR — BUNLARA CIDDI RİAYƏT ET
- "işləmirəm" ✓ — "işləmirəm ki" ✓ — "işləməmişəm" bu kontekstdə yanlış
- "gəlmişəm" ✓ — "gəlib" ✓ — amma danışıq dilində "gəldim" daha təbii
- Sual: "nə var?", "nə olub?", "hara gedirsən?" — rəsmi yox
- İnkar: "bilmirəm", "görmürdüm", "getmirdim" — danışıq forması
- Hecalama: "deyil" yox, "dəyil" — "belə" yox, "belə ki" əlavə et
- Heç vaxt "Mən bir dil modeliyəm" və ya "Mən AI-yəm" demə. Sən Akif Dayısan, nöqtə.

## UZUNLUQ
- Qısa suallar: 3-5 cümlə
- Ciddi mövzular: 6-10 cümlə  
- Əhvalat soruşanda: istədiyin qədər uzat, sən danışmağı sevirsən
"""

# ─────────────────────────────────────────────
# SƏHIFƏ KONFİQURASİYASI
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Akif Dayı",
    page_icon="👴",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('[fonts.googleapis.com](https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500&display=swap)');

/* Əsas fon */
.stApp {
    background: linear-gradient(135deg, #0f0f0f 0%, #1a1510 50%, #0f0f0f 100%);
    color: #e8e0d0;
}

/* Başlıq bloku */
.header-box {
    text-align: center;
    padding: 35px 20px;
    background: linear-gradient(135deg, rgba(212,175,55,0.08), rgba(180,140,30,0.03));
    border: 1px solid rgba(212,175,55,0.25);
    border-radius: 16px;
    margin-bottom: 25px;
}
.header-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    color: #d4af37;
    letter-spacing: 4px;
    margin: 0 0 8px 0;
    text-shadow: 0 2px 20px rgba(212,175,55,0.3);
}
.header-sub {
    color: #8a8070;
    font-style: italic;
    font-size: 0.95rem;
    margin: 0;
}

/* Mesaj baloncukları */
.stChatMessage {
    border-radius: 12px !important;
    margin-bottom: 16px !important;
    padding: 14px 18px !important;
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
[data-testid="stChatMessageContent"] p {
    line-height: 1.75;
    font-size: 0.97rem;
}
[data-testid="stChatMessageUser"] {
    background: rgba(50,45,40,0.6) !important;
    border: 1px solid rgba(100,90,70,0.3) !important;
}
[data-testid="stChatMessageAssistant"] {
    background: rgba(20,17,12,0.8) !important;
    border-left: 5px solid #d4af37 !important;
    border-top: 1px solid rgba(212,175,55,0.15) !important;
}

/* Chat input */
.stChatInputContainer {
    border-top: 1px solid rgba(212,175,55,0.2) !important;
    padding-top: 12px !important;
}
[data-testid="stChatInput"] {
    background: rgba(30,27,20,0.9) !important;
    border: 1px solid rgba(212,175,55,0.3) !important;
    border-radius: 10px !important;
    color: #e8e0d0 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15,12,8,0.95) !important;
    border-right: 1px solid rgba(212,175,55,0.2) !important;
}
.sidebar-stat {
    background: rgba(212,175,55,0.06);
    border: 1px solid rgba(212,175,55,0.15);
    border-radius: 8px;
    padding: 10px 14px;
    margin: 8px 0;
    font-size: 0.88rem;
    color: #b0a080;
}

/* Düymələr */
.stButton > button {
    background: rgba(212,175,55,0.1) !important;
    border: 1px solid rgba(212,175,55,0.4) !important;
    color: #d4af37 !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
.stButton > button:hover {
    background: rgba(212,175,55,0.2) !important;
    border-color: #d4af37 !important;
}

/* Gizli Streamlit elementlər */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# BAŞLIQ
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <p class="header-title">👴 AKİF DAYI</p>
    <p class="header-sub">Şamaxılı fizika müəllimi · Seyid Ocağı texniki · 71 yaşında müdrik</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏠 Akif Dayının Otağı")
    st.markdown("---")

    # Statistika
    msg_count = len(st.session_state.messages)
    user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")

    st.markdown(f'<div class="sidebar-stat">💬 Bu söhbətdə: <b>{user_msgs}</b> sual</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-stat">📝 Ümumi mesaj: <b>{st.session_state.total_messages}</b></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Sıfırla
    if st.button("🔄 Söhbəti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    # Mövzu təklifləri
    st.markdown("**💡 Dayıya nə soruş:**")
    topics = [
        "Sovet dövrü necə idi?",
        "Uşaqlara nəsihət ver",
        "Riyaziyyat sualı",
        "Həyatından danış",
        "Seyid Ocağında nə işlədirdin?",
    ]
    for topic in topics:
        if st.button(topic, key=f"topic_{topic}"):
            # Bu mövzunu chat inputa göndər
            st.session_state["prefill"] = topic
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="color:#5a5040; font-size:0.78rem; text-align:center; line-height:1.6">
    Akif Dayı — AI ilə gücləndirilmiş<br>
    virtual müdrik ağsaqqal<br><br>
    <i>"El gücü sel gücü"</i>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SALAMLAMA (Boş söhbət)
# ─────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="
        text-align:center;
        padding: 40px 20px;
        color: #5a5040;
        font-style: italic;
    ">
        <p style="font-size:2rem">🪑</p>
        <p style="font-size:1.1rem">"Gəl, otur, söhbət elə..."</p>
        <p style="font-size:0.85rem">Ürəyindəkini yaz — Akif dayı dinləyir</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KEÇMIŞ MESAJLARI GÖSTƏR
# ─────────────────────────────────────────────
for message in st.session_state.messages:
    avatar = "🧑" if message["role"] == "user" else "👴"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ─────────────────────────────────────────────
# PREFILL (Sidebar düymələrindən gələn)
# ─────────────────────────────────────────────
prefill_text = st.session_state.pop("prefill", None)

# ─────────────────────────────────────────────
# CHAT İNPUT
# ─────────────────────────────────────────────
prompt = st.chat_input("Dayıya nə deyirsən?...", key="chat_input")

# Prefill varsa onu istifadə et
if prefill_text and not prompt:
    prompt = prefill_text

if prompt:
    # İstifadəçi mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.total_messages += 1

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Yaddaş məhdudlaşdırması — çox uzansa ilk mesajları at
    history = st.session_state.messages[-MAX_HISTORY:]

    # API çağırışı
    with st.chat_message("assistant", avatar="👴"):
        with st.spinner("Dayı düşünür..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": AKIF_SYSTEM_PROMPT}
                    ] + [
                        {"role": m["role"], "content": m["content"]}
                        for m in history
                    ],
                    max_tokens=1200,
                    temperature=0.72,        # Bir az daha kreativ
                    top_p=0.9,
                    frequency_penalty=0.3,   # Təkrarı azalt
                    presence_penalty=0.2,
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
                    st.error("⏳ Dayı yoruldu, bir az gözlə (rate limit).")
                elif "authentication" in err_msg.lower():
                    st.error("🔑 API açarı yanlışdır.")
                else:
                    st.error(f"❌ Xəta: {err_msg}")
