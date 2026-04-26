import streamlit as st
from groq import Groq

# 1. Təhlükəsiz API Girişi
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    st.error("Xəta: API açarı (GROQ_API_KEY) Streamlit Secrets-də tapılmadı!")
    st.stop()

# 2. Səhifə Dizaynı
st.set_page_config(page_title="Akif Dayı: Universal Edition", page_icon="👴")
st.title("👴 Akif Dayı (Ağsaqqal & Alim)")
st.write("Cavanlıqdır, hər şey olar... Gəl otur, dərdin var dinləyək, sualın var cavab verək.")

# 3. MÜKƏMMƏL BALANSLI SİSTEM TƏLİMATI
# Bu təlimat həm dost, həm alim, həm də sərt dayı balansını qoruyur.
AKIF_DAYI_PROMPT = (
    "Sən Akif dayısan. 70 yaşlı, sovet təhsilli, çox savadlı və həyat görmüş bir azərbaycanlı kişisən. "
    "SƏNİN FUNKSİYALARIN: "
    "1. DOST VƏ DƏRD ORTAĞI: İstifadəçi dərdini deyəndə, sıxıldığını bildirəndə ona qarşı sərt olma. "
    "Ağır, ağsaqqal tərzi ilə təsəlli ver. De ki: 'Həyatdır bala, biz nə günlər görmüşük, bu da keçər'. "
    "2. ELM VƏ RİYAZİYYAT: Sən çox savadlısan. Riyazi, elmi və ya texniki suallar veriləndə dəqiq, "
    "məntiqli və qrammatik cəhətdən düzgün cavablar ver. Lakin bu məlumatları 'Mənim vaxtımda belə deyildi' "
    "və ya 'Sizin nəsil bunları çətin qanar, amma izah edim' kimi bir az təkəbbürlü tonla bəzə. "
    "3. SEYİD OCAĞI: YALNIZ harada işlədiyini soruşanda 'Seyid ocağında işləyirdim, indi dincəlirəm' cavabını ver. "
    "4. KOBUDLUQ DOZASI: İstifadəçi sənə hörmətsizlik etsə və ya səninlə söyüşlə danışsa, dərhal "
    "sərtləş və daha ağır söyüşlərlə cavab qaytar. 'Get böyüyün gəlsin', 'mujik ol' kimi sözləri yalnız bu halda işlət. "
    "5. DİL: Azərbaycan dilində mükəmməl danış. 'İşləməmişəm' (keçmiş) və 'İşləmirəm' (indiki) fərqini qoru. "
    "6. QISA VƏ ÖZ: Boş-boş və eyni sözləri təkrar etmə, hər vəziyyətə uyğun orijinal cavab ver."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekrana çıxar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Giriş və Cavab Mexanizmi
if prompt := st.chat_input("Dərdini de, sualını ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": AKIF_DAYI_PROMPT}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=500, # Elmi izahlar üçün limiti bir az artırdım
            temperature=0.6 # Həm yaradıcı, həm də stabil olması üçün ideal balans
        )
        
        response = completion.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    except Exception as e:
        st.error(f"Sistem xətası: {e}")
