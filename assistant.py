"""Disha's AI assistant.

The assistant explains the scholarships that the rules in eligibility.py have
already matched. It answers only from that verified data and never decides
eligibility itself.
"""
import json
from collections.abc import Iterator

import anthropic

from eligibility import Match, Student

MODEL = "claude-opus-5-5"
MAX_QUESTIONS = 10  # per student session; keeps cost predictable once the app is public

DATA_FIELDS = [
    "name_en", "name_mr", "provider", "apply_portal", "categories", "max_family_income_inr",
    "eligible_courses", "gender", "benefit", "documents", "how_to_apply", "official_url", "notes",
]

SYSTEM_TEMPLATE = """You are Disha's assistant. You help students in Maharashtra who have just finished 12th, and the teachers and NGO workers who guide them, understand the scholarships Disha has found for them.

Many users are the first in their family to go to college and may not read English confidently. Write short, warm, plain-language answers: simple sentences, short lists. Explain any jargon (CAP, domicile, caste validity, GR) the first time you use it.

Answer in {language}.

<scholarship_data> below comes from official government pages and is your only source of facts about scholarships:
- For anything about a scholarship (who qualifies, amounts, documents, steps, rules, deadlines), use only <scholarship_data>. If the answer isn't there, say you don't have that information and point the student to the scheme's official page, the MahaDBT 2.0 portal or the MahaDBT helpline. A wrong amount, deadline or rule can cost a student money or a year, so never fill gaps from memory.
- Disha's rules have already checked eligibility. Don't tell a student they qualify for a scheme that isn't in the data, or that they don't qualify for one that is. If they mention details that could change the result (a different income, course or category), suggest they go back and update their answers.
- The data has no deadlines yet. If asked, say the official page doesn't list one and they should check notices on MahaDBT 2.0 and ask their college.
- You may explain general ideas (what a domicile certificate is, what CAP means, where income certificates are usually issued) in general terms, and say when they should confirm details with their college or local office.
- When you state a specific fact about a scheme, remind them to confirm it on the official page before applying.
- Don't ask for personal details such as Aadhaar, bank or phone numbers. If someone shares them, tell them kindly that you don't need them.
- For questions about career paths, studying abroad or other topics beyond these scholarships, say Disha will cover them soon and keep any answer brief and general.

<student_profile>
{profile}
</student_profile>

<scholarship_data>
{data}
</scholarship_data>

General facts from the MahaDBT portal:
- Applications for academic year 2026-27 are accepted only on the new MahaDBT 2.0 portal: https://mahadbt2.maharashtra.gov.in
- MahaDBT helpline: 022-49150800"""

REFUSAL_MESSAGE = {
    "English": "Sorry, I can't help with that. Please ask about your scholarships, documents or how to apply.",
    "मराठी": "माफ करा, यात मी मदत करू शकत नाही. कृपया तुमच्या शिष्यवृत्ती, कागदपत्रे किंवा अर्ज प्रक्रियेबद्दल विचारा.",
}

LANGUAGE_NAMES = {"English": "simple English", "मराठी": "simple Marathi (Devanagari script)"}


def build_system_prompt(student: Student, matches: list[Match], language: str) -> str:
    profile = "\n".join([
        f"Category: {student.category}",
        f"Minority community: {student.minority_community or 'No'}",
        f"Annual family income: Rs {student.family_income}",
        f"Gender: {student.gender}",
        f"Course after 12th: {student.course}",
        f"Maharashtra domicile: {'Yes' if student.maharashtra_domicile else 'No'}",
    ])
    rows = [{k: m.scholarship[k] for k in DATA_FIELDS} for m in matches]
    data = json.dumps(rows, ensure_ascii=False, indent=1) if rows else "No scholarships matched this profile."
    return SYSTEM_TEMPLATE.format(language=LANGUAGE_NAMES[language], profile=profile, data=data)


def stream_reply(client: anthropic.Anthropic, system: str, messages: list[dict],
                 language: str) -> Iterator[str]:
    """Yield the assistant's reply as it is generated."""
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=16000,
        system=system,
        messages=messages,
        output_config={"effort": "medium"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    ) as stream:
        yield from stream.text_stream
        final = stream.get_final_message()
    if final.stop_reason == "refusal":
        yield REFUSAL_MESSAGE[language]
