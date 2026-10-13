import streamlit as st

from eligibility import (
    CATEGORIES, COURSES, GENDERS, MINORITY_COMMUNITIES,
    Student, find_eligible, load_scholarships, split,
)

TEXT = {
    "English": {
        "tagline": "Find the scholarships open to you after 12th.",
        "intro": "Answer a few questions. We'll show every scholarship you qualify for, the documents you need and how to apply.",
        "privacy": "Your answers are not saved anywhere.",
        "category": "Your category (as on your caste certificate)",
        "minority": "Are you from a minority community?",
        "no_minority": "No",
        "income": "Annual family income (₹), as on your income certificate",
        "gender": "You are a",
        "course": "What will you study after 12th?",
        "domicile": "Are you a domicile (permanent resident) of Maharashtra?",
        "yes": "Yes", "no": "No",
        "submit": "Show my scholarships",
        "found": "You may be eligible for {n} scholarship(s)",
        "none": "We didn't find a scholarship for this profile in our list yet. We're adding more. You can also use **Find Eligible Schemes** on the MahaDBT portal.",
        "benefit": "What you get",
        "why": "Why you qualify",
        "careful": "Please check",
        "documents": "Documents to keep ready",
        "steps": "How to apply",
        "rules": "Important rules",
        "official": "Official page",
        "provider": "Run by",
        "draft": "DRAFT: not yet verified",
        "portal_note": "For 2026-27, apply on the new **MahaDBT 2.0** portal: mahadbt2.maharashtra.gov.in",
        "confirm": "Always confirm details on the official portal before applying.",
        "another": "Check another student",
        "download": "Download checklist",
        "details_lang": "",
        "reviewers": "For reviewers",
        "reviewer": "Reviewer mode: include draft (unverified) data",
        "reviewer_help": "Only for checking the data. Students should see verified data only.",
        "no_verified": "No scholarships are verified yet. To test with draft data, turn on reviewer mode under **For reviewers** at the bottom of the page.",
        "reasons": {
            "category": "Your category ({value}) is eligible",
            "minority": "Open to {value} students",
            "income": "Family income is within the ₹{limit} limit",
            "marks": "12th marks meet the {min:g}% minimum",
            "course_any": "Covers any course after 12th",
            "course_professional": "Covers professional / technical courses",
            "course": "Covers your course",
            "gender": "Only for {value} students",
            "domicile": "You are a Maharashtra domicile",
        },
        "cautions": {
            "marks_unknown": "Needs at least {min:g}% in 12th",
            "domicile_unknown": "The official page doesn't say whether Maharashtra domicile is required",
        },
        "categories": {"Open": "Open", "EWS": "EWS", "SEBC": "SEBC", "OBC": "OBC", "SBC": "SBC",
                       "VJNT": "VJNT", "SC": "SC", "Neo-Buddhist": "Neo-Buddhist (Navbauddha)", "ST": "ST"},
        "minorities": {"Muslim": "Muslim", "Buddhist": "Buddhist", "Christian": "Christian", "Sikh": "Sikh",
                       "Parsi": "Parsi", "Jain": "Jain", "Jewish": "Jewish"},
        "genders": {"Female": "Girl", "Male": "Boy", "Other": "Other"},
        "courses": {
            "professional": "Professional degree through CAP (Engineering, Medical, Pharmacy, Architecture…)",
            "diploma": "Polytechnic diploma",
            "arts": "Arts (BA)",
            "commerce": "Commerce (B.Com)",
            "science": "Science (B.Sc)",
            "law": "Law",
            "education": "Education (D.Ed / B.Ed)",
            "other": "Other / not decided yet",
        },
    },
    "मराठी": {
        "tagline": "१२वी नंतर तुमच्यासाठी उपलब्ध शिष्यवृत्ती जाणून घ्या.",
        "intro": "काही प्रश्नांची उत्तरे द्या. तुम्ही पात्र असलेल्या सर्व शिष्यवृत्ती, आवश्यक कागदपत्रे आणि अर्ज कसा करायचा ते आम्ही दाखवू.",
        "privacy": "तुमची उत्तरे कुठेही जतन केली जात नाहीत.",
        "category": "तुमचा प्रवर्ग (जात प्रमाणपत्रानुसार)",
        "minority": "तुम्ही अल्पसंख्याक समुदायातील आहात का?",
        "no_minority": "नाही",
        "income": "कुटुंबाचे वार्षिक उत्पन्न (₹), उत्पन्न दाखल्यानुसार",
        "gender": "तुम्ही",
        "course": "१२वी नंतर तुम्ही काय शिकणार आहात?",
        "domicile": "तुम्ही महाराष्ट्राचे अधिवासी (कायमचे रहिवासी) आहात का?",
        "yes": "होय", "no": "नाही",
        "submit": "माझ्या शिष्यवृत्ती दाखवा",
        "found": "तुम्ही {n} शिष्यवृत्तींसाठी पात्र असू शकता",
        "none": "या माहितीसाठी आमच्या यादीत अजून शिष्यवृत्ती सापडली नाही. आम्ही आणखी योजना जोडत आहोत. तुम्ही MahaDBT पोर्टलवरील **Find Eligible Schemes** देखील वापरू शकता.",
        "benefit": "तुम्हाला काय मिळेल",
        "why": "तुम्ही पात्र का आहात",
        "careful": "कृपया तपासा",
        "documents": "तयार ठेवायची कागदपत्रे",
        "steps": "अर्ज कसा करायचा",
        "rules": "महत्त्वाचे नियम",
        "official": "अधिकृत पान",
        "provider": "योजना राबवणारा विभाग",
        "draft": "मसुदा: अजून पडताळणी झालेली नाही",
        "portal_note": "२०२६-२७ साठी नवीन **MahaDBT 2.0** पोर्टलवर अर्ज करा: mahadbt2.maharashtra.gov.in",
        "confirm": "अर्ज करण्यापूर्वी अधिकृत पोर्टलवर माहिती नक्की तपासा.",
        "another": "दुसऱ्या विद्यार्थ्याची माहिती तपासा",
        "download": "यादी डाउनलोड करा",
        "details_lang": "योजनेची सविस्तर माहिती सध्या इंग्रजीत आहे. मराठी लवकरच येईल.",
        "reviewers": "पडताळणी करणाऱ्यांसाठी",
        "reviewer": "पडताळणी मोड: मसुदा (पडताळणी न झालेली) माहितीही दाखवा",
        "reviewer_help": "फक्त माहिती तपासण्यासाठी. विद्यार्थ्यांना फक्त पडताळलेली माहिती दिसावी.",
        "no_verified": "अजून एकाही शिष्यवृत्तीची पडताळणी झालेली नाही. मसुदा माहितीसह तपासण्यासाठी पानाच्या तळाशी **पडताळणी करणाऱ्यांसाठी** मध्ये पडताळणी मोड सुरू करा.",
        "reasons": {
            "category": "तुमचा प्रवर्ग ({value}) पात्र आहे",
            "minority": "{value} विद्यार्थ्यांसाठी खुली",
            "income": "कुटुंबाचे उत्पन्न ₹{limit} मर्यादेत आहे",
            "marks": "१२वीचे गुण किमान {min:g}% पेक्षा जास्त आहेत",
            "course_any": "१२वी नंतरच्या कोणत्याही अभ्यासक्रमासाठी",
            "course_professional": "व्यावसायिक / तांत्रिक अभ्यासक्रमांसाठी",
            "course": "तुमच्या अभ्यासक्रमासाठी लागू",
            "gender": "फक्त {value} विद्यार्थ्यांसाठी",
            "domicile": "तुम्ही महाराष्ट्राचे अधिवासी आहात",
        },
        "cautions": {
            "marks_unknown": "१२वीत किमान {min:g}% गुण आवश्यक",
            "domicile_unknown": "महाराष्ट्र अधिवास आवश्यक आहे का, हे अधिकृत पानावर नमूद नाही",
        },
        "categories": {"Open": "खुला", "EWS": "EWS (आर्थिकदृष्ट्या दुर्बल घटक)", "SEBC": "SEBC",
                       "OBC": "OBC (इतर मागास वर्ग)", "SBC": "SBC (विशेष मागास प्रवर्ग)",
                       "VJNT": "VJNT (विमुक्त जाती व भटक्या जमाती)", "SC": "SC (अनुसूचित जाती)",
                       "Neo-Buddhist": "नवबौद्ध", "ST": "ST (अनुसूचित जमाती)"},
        "minorities": {"Muslim": "मुस्लिम", "Buddhist": "बौद्ध", "Christian": "ख्रिश्चन", "Sikh": "शीख",
                       "Parsi": "पारशी", "Jain": "जैन", "Jewish": "ज्यू"},
        "genders": {"Female": "मुलगी", "Male": "मुलगा", "Other": "इतर"},
        "courses": {
            "professional": "CAP द्वारे व्यावसायिक पदवी (अभियांत्रिकी, वैद्यकीय, फार्मसी, आर्किटेक्चर…)",
            "diploma": "पॉलिटेक्निक डिप्लोमा",
            "arts": "कला (BA)",
            "commerce": "वाणिज्य (B.Com)",
            "science": "विज्ञान (B.Sc)",
            "law": "विधी (Law)",
            "education": "शिक्षणशास्त्र (D.Ed / B.Ed)",
            "other": "इतर / अजून ठरवले नाही",
        },
    },
}

st.set_page_config(page_title="Disha", page_icon="🧭")

language = st.radio("Language / भाषा", list(TEXT), horizontal=True)
t = TEXT[language]

reviewer_mode = st.session_state.get("reviewer_mode", False)
scholarships = load_scholarships(include_drafts=reviewer_mode)

st.title("Disha · दिशा")
st.write(t["tagline"])

if "student" not in st.session_state:
    st.session_state.student = None


def inr(amount: int) -> str:
    """Format rupees the Indian way: 800000 -> 8,00,000."""
    digits = str(amount)
    head, tail = digits[:-3], digits[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    if head:
        groups.insert(0, head)
    return ",".join(groups + [tail])


def localize(params: dict) -> dict:
    """Show reason values (category, community, gender, amounts) in the chosen language."""
    labels = {**t["categories"], **t["minorities"], **t["genders"], **t["courses"]}
    out = {}
    for key, value in params.items():
        if key == "limit":
            out[key] = inr(value)
        elif isinstance(value, str):
            out[key] = labels.get(value, value)
        else:
            out[key] = value
    return out


def checklist_text(student: Student, matches) -> str:
    lines = ["Disha – scholarship checklist", ""]
    for m in matches:
        s = m.scholarship
        lines += [s["name_en"], f"  Benefit: {s['benefit']}", f"  Official page: {s['official_url']}", "  Documents:"]
        lines += [f"    [ ] {d}" for d in split(s["documents"])]
        lines.append("")
    lines += ["Apply on MahaDBT 2.0: https://mahadbt2.maharashtra.gov.in",
              "Always confirm details on the official portal before applying."]
    return "\n".join(lines)


def show_results(student: Student):
    if not scholarships:
        st.warning(t["no_verified"])
        return
    matches = find_eligible(student, scholarships)
    if not matches:
        st.info(t["none"])
        return

    st.subheader(t["found"].format(n=len(matches)))
    st.info(t["portal_note"])
    if t["details_lang"]:
        st.caption(t["details_lang"])

    for m in matches:
        s = m.scholarship
        with st.container(border=True):
            if s["status"] != "verified":
                st.warning(t["draft"])
            name = s["name_mr"] if language == "मराठी" and s["name_mr"] else s["name_en"]
            st.markdown(f"### {name}")
            st.caption(f"{t['provider']}: {s['provider']}")
            st.markdown(f"**{t['benefit']}:** {s['benefit']}")

            st.markdown(f"**{t['why']}:**")
            for code, params in m.reasons:
                st.markdown(f"- ✅ {t['reasons'][code].format(**localize(params))}")
            for code, params in m.cautions:
                st.markdown(f"- ⚠️ {t['careful']}: {t['cautions'][code].format(**localize(params))}")

            with st.expander(t["documents"]):
                for doc in split(s["documents"]):
                    st.markdown(f"- {doc}")
            with st.expander(t["steps"]):
                for i, step in enumerate(split(s["how_to_apply"]), 1):
                    st.markdown(f"{i}. {step}")
            if s["notes"]:
                with st.expander(t["rules"]):
                    st.write(s["notes"])
            st.link_button(t["official"], s["official_url"])

    st.download_button(t["download"], checklist_text(student, matches),
                       file_name="disha-checklist.txt")


if st.session_state.student is None:
    st.write(t["intro"])
    st.caption(t["privacy"])
    with st.form("profile"):
        category = st.selectbox(t["category"], CATEGORIES, format_func=t["categories"].get)
        minority = st.selectbox(t["minority"], [None] + MINORITY_COMMUNITIES,
                                format_func=lambda v: t["no_minority"] if v is None else t["minorities"][v])
        income = st.number_input(t["income"], min_value=0, value=200_000, step=10_000)
        gender = st.radio(t["gender"], GENDERS, format_func=t["genders"].get, horizontal=True)
        course = st.selectbox(t["course"], COURSES, format_func=t["courses"].get)
        domicile = st.radio(t["domicile"], [True, False],
                            format_func=lambda v: t["yes"] if v else t["no"], horizontal=True)
        if st.form_submit_button(t["submit"], type="primary"):
            st.session_state.student = Student(
                category=category, family_income=int(income), gender=gender, course=course,
                maharashtra_domicile=domicile, minority_community=minority,
            )
            st.rerun()
else:
    show_results(st.session_state.student)
    if st.button(t["another"]):
        st.session_state.student = None
        st.rerun()

st.divider()
st.caption(t["confirm"])
with st.expander(t["reviewers"]):
    st.toggle(t["reviewer"], key="reviewer_mode", help=t["reviewer_help"])
