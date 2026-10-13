import anthropic
import streamlit as st

from assistant import MAX_QUESTIONS, build_system_prompt, stream_reply
from eligibility import (
    CATEGORIES, COURSES, GENDERS, MINORITY_COMMUNITIES,
    Student, find_eligible, load_scholarships, split,
)

TEXT = {
    "English": {
        "tagline": "Find the scholarships open to you after 12th.",
        "intro": "Answer a few questions. We'll show every scholarship you qualify for, the documents you need and how to apply.",
        "privacy": "Your answers are not saved anywhere. Checking eligibility happens without AI.",
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
        "machine_translated": "",
        "ask_title": "Have a question? Ask Disha",
        "ask_intro": "Answers use only the scholarship information shown above. Your questions and the answers you gave are sent to our AI provider to write a reply; they're not saved.",
        "ask_unavailable": "The assistant isn't set up yet.",
        "ask_placeholder": "Ask about documents, steps or rules…",
        "ask_limit": "You've reached the question limit for this session. Check another student to start again.",
        "ask_error": "Sorry, the assistant isn't available right now. Please try again in a moment.",
        "suggestions": ["Which documents should I get first?", "What is CAP?", "What happens if I fail a year?"],
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
        "privacy": "तुमची उत्तरे कुठेही जतन केली जात नाहीत. पात्रता तपासणी AI शिवाय होते.",
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
        "machine_translated": "मराठी माहिती AI ने भाषांतरित केली आहे आणि तिची तपासणी सुरू आहे. शंका असल्यास अधिकृत पान पाहा.",
        "ask_title": "काही प्रश्न आहे? दिशाला विचारा",
        "ask_intro": "उत्तरे फक्त वर दाखवलेल्या शिष्यवृत्ती माहितीवर आधारित असतात. उत्तर तयार करण्यासाठी तुमचे प्रश्न आणि तुम्ही दिलेली माहिती आमच्या AI सेवेकडे पाठवली जाते; ती जतन केली जात नाही.",
        "ask_unavailable": "सहाय्यक अजून सुरू केलेला नाही.",
        "ask_placeholder": "कागदपत्रे, अर्ज प्रक्रिया किंवा नियमांबद्दल विचारा…",
        "ask_limit": "या सत्रातील प्रश्नांची मर्यादा पूर्ण झाली. पुन्हा सुरू करण्यासाठी दुसऱ्या विद्यार्थ्याची माहिती तपासा.",
        "ask_error": "माफ करा, सहाय्यक सध्या उपलब्ध नाही. कृपया थोड्या वेळाने पुन्हा प्रयत्न करा.",
        "suggestions": ["आधी कोणती कागदपत्रे मिळवू?", "CAP म्हणजे काय?", "एखाद्या वर्षी नापास झालो तर काय?"],
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


def detail(s: dict, name: str) -> str:
    """A scholarship field in the chosen language, falling back to English."""
    if language == "मराठी" and s.get(f"{name}_mr", "").strip():
        return s[f"{name}_mr"]
    return s[name]


def show_results(student: Student) -> list:
    if not scholarships:
        st.warning(t["no_verified"])
        return []
    matches = find_eligible(student, scholarships)
    if not matches:
        st.info(t["none"])
        return []

    st.subheader(t["found"].format(n=len(matches)))
    st.info(t["portal_note"])
    if language == "मराठी":
        rows = [m.scholarship for m in matches]
        if any(not s["benefit_mr"].strip() for s in rows):
            st.caption(t["details_lang"])
        elif any(s["mr_reviewed"].strip() != "Yes" for s in rows):
            st.caption(t["machine_translated"])

    for m in matches:
        s = m.scholarship
        with st.container(border=True):
            if s["status"] != "verified":
                st.warning(t["draft"])
            name = s["name_mr"] if language == "मराठी" and s["name_mr"] else s["name_en"]
            st.markdown(f"### {name}")
            st.caption(f"{t['provider']}: {s['provider']}")
            st.markdown(f"**{t['benefit']}:** {detail(s, 'benefit')}")

            st.markdown(f"**{t['why']}:**")
            for code, params in m.reasons:
                st.markdown(f"- ✅ {t['reasons'][code].format(**localize(params))}")
            for code, params in m.cautions:
                st.markdown(f"- ⚠️ {t['careful']}: {t['cautions'][code].format(**localize(params))}")

            with st.expander(t["documents"]):
                for doc in split(detail(s, "documents")):
                    st.markdown(f"- {doc}")
            with st.expander(t["steps"]):
                for i, step in enumerate(split(detail(s, "how_to_apply")), 1):
                    st.markdown(f"{i}. {step}")
            if s["notes"]:
                with st.expander(t["rules"]):
                    st.write(detail(s, "notes"))
            st.link_button(t["official"], s["official_url"])

    st.download_button(t["download"], checklist_text(student, matches),
                       file_name="disha-checklist.txt")
    return matches


def get_client() -> anthropic.Anthropic | None:
    try:
        key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:  # no secrets file, or key missing
        return None
    return anthropic.Anthropic(api_key=key)


def show_assistant(student: Student, matches: list):
    st.divider()
    st.subheader(t["ask_title"])
    client = get_client()
    if client is None:
        st.caption(t["ask_unavailable"])
        return
    st.caption(t["ask_intro"])

    chat = st.session_state.setdefault("chat", [])
    for message in chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    asked = sum(1 for message in chat if message["role"] == "user")
    if asked >= MAX_QUESTIONS:
        st.info(t["ask_limit"])
        return

    question = None
    if not chat:
        cols = st.columns(len(t["suggestions"]))
        for col, suggestion in zip(cols, t["suggestions"]):
            if col.button(suggestion, use_container_width=True):
                question = suggestion
    question = st.chat_input(t["ask_placeholder"]) or question
    if not question:
        return

    chat.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    system = build_system_prompt(student, matches, language)
    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(stream_reply(client, system, chat, language))
        except anthropic.APIError:
            chat.pop()
            st.error(t["ask_error"])
            return
    chat.append({"role": "assistant", "content": reply})


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
    matches = show_results(st.session_state.student)
    if st.button(t["another"]):
        st.session_state.student = None
        st.session_state.chat = []
        st.rerun()
    if matches:
        show_assistant(st.session_state.student, matches)

st.divider()
st.caption(t["confirm"])
with st.expander(t["reviewers"]):
    st.toggle(t["reviewer"], key="reviewer_mode", help=t["reviewer_help"])
