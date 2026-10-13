import streamlit as st

TEXT = {
    "English": {
        "tagline": "Find the scholarships and career paths open to you after 12th.",
        "status": "Disha is being built. Soon you'll be able to answer a few questions and see every scholarship you qualify for.",
        "note": "Always confirm details on the official portal before applying.",
    },
    "मराठी": {
        "tagline": "१२वी नंतर तुमच्यासाठी उपलब्ध शिष्यवृत्ती आणि करिअरचे पर्याय जाणून घ्या.",
        "status": "दिशा सध्या तयार होत आहे. लवकरच काही प्रश्नांची उत्तरे देऊन तुम्ही पात्र असलेल्या सर्व शिष्यवृत्ती पाहू शकाल.",
        "note": "अर्ज करण्यापूर्वी अधिकृत पोर्टलवर माहिती नक्की तपासा.",
    },
}

st.set_page_config(page_title="Disha", page_icon="🧭")

language = st.radio("Language / भाषा", list(TEXT), horizontal=True)
t = TEXT[language]

st.title("Disha · दिशा")
st.write(t["tagline"])
st.info(t["status"])
st.caption(t["note"])
