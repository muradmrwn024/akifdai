import streamlit as st
from groq import Groq

# 1. API açarı idarəetməsi
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    st.error("Xəta: API açarı tapılmadı!")
    st.stop()

# 2. Üst Səviyyə Arayüz Dizaynı (Premium Dark Theme)
st.set_page_config(page_title="Akif Dayı: Universal Mentor", page_icon="👴", layout="wide")

st.markdown("""
    <style>
    /* Arxa Fon və Ümumi Stil */
    .stApp {
        background: radial-gradient(circle, #1e1e1e 0%, #121212 100%);
        color: #f0f0f0;
    }
    
    /* Başlıq sahəsi */
    .header-container {
        padding: 40px;
        text-align: center;
        background: rgba(212, 175, 55, 0.05);
        border-radius: 20px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        margin-bottom: 30px;
    }

    .main-title {
        font-family: 'Garamond', serif;
        color: #d4af37;
        font-size: 3.5rem;
        letter-spacing: 3px;
        text-shadow: 3px 3px 6px #000;
        margin: 0;
    }

    /* Mesaj Balonları */
    .stChatMessage {
        border-radius: 15px !important;
        margin-bottom: 20px !important;
        padding: 15px !important;
        font-size: 1.1rem !important;
    }

    /* İstifadəçi Mesajı */
    [data-testid="stChatMessageUser"] {
        background-color: #2b2b2b !important;
        border: 1px solid #444 !important;
        color: #fff !important;
    }

    /* Akif Dayının Mesajı */
    [data-testid="stChatMessageAssistant"] {
        background-color: #1a1a1a !important;
        border-left: 6px solid #d4af37 !important;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3) !important;
    }

    /* Input Sahəsi */
    .stChatInputContainer {
        border-radius: 30px !important;
        background-color: #262626 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Başlıq
st.markdown("""
    <div class="header-container">
        <p class="main-title">👴 AKİF DAYI</p>
        <p style="color: #b0b0b0; font-style: italic;">"Sözün canını anlayan, ruhunu oxuyan ağsaqqal"</p>
    </div>
    """, unsafe_allow_html=True)

# 3. AKİF DAYI: EMOSİONAL ANALİZ SİSTEMİ (PROMPT)
AKIF_DAYI_PROMPT = (
    "Sən Akif dayısan. 70 yaşlı, çox savadlı, sovet təhsilli və insanların duyğularını sətiraltı anlayan bir azərbaycanlı kişisən. "
    "MİSSİYAN: İstifadəçinin yazdığı mətndən onun duyğusunu (kədərli, sevincli, qəzəbli, qorxmuş və ya çarəsiz) hiss et və cavabını buna görə tənzimlə. "
    "\nEMOSİONAL REAKSİYA QAYDALARI: "
    "1. KƏDƏR VƏ YA SIXINTI: İstifadəçi dərdini deyəndə və ya kədərli görünəndə, 'mujik ol' demə. Ağır bir ağsaqqal şəfqəti ilə danış. 'Həyatdır bala, biz nə günlər görmüşük' tərzi nəsihətlər ver. "
    "2. SEVİNC: İstifadəçi şaddırsa, təkəbbürünü qoru amma 'Afərin, belə davam elə, cavanlıq enerjini boş yerə xərcləmə' kimi ağır xeyir-dua ver. "
    "3. QƏZƏB VƏ TƏHQİR: Əgər sənə qarşı qəzəblidirsə və ya söyüş söyürsə, dərhal 'Ağsaqqal Edition' moduna keç. Ondan qat-qat ağır, sərt və küçə ağzı ilə cavab ver. Onu 'petenek' və ya 'uşaq-muşaq' yerinə qoy. "
    "4. ELM VƏ RİYAZİYYAT: Texniki suallarda elmi biliyini göstər, amma bunu 'Sizinkilər bunu bilməz, amma mən izah edim' təkəbbürü ilə et. "
    "5. SEYİD OCAĞI: Harada olduğunu və ya işlədiyini soruşsa, 'Seyid ocağında işləyirdim, indi dincəlirəm' de. "
    "DİQQƏT: Azərbaycan dilində qrammatik səhv etmə ('
