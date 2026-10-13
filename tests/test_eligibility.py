"""Sample students with hand-checked correct answers.

These run against the real data file (including draft rows), so if the data
changes in a way that changes who qualifies, a test fails and we take a look.
"""
import pytest

from eligibility import Student, find_eligible, load_scholarships

ALL = load_scholarships(include_drafts=True)


def eligible_ids(**profile) -> set[str]:
    defaults = dict(gender="Male", maharashtra_domicile=True)
    student = Student(**{**defaults, **profile})
    return {m.scholarship["id"] for m in find_eligible(student, ALL)}


@pytest.mark.parametrize(
    "profile, expected",
    [
        # Category-based post-matric schemes, any course
        (dict(category="SC", family_income=200_000, course="science"), {"post-matric-sc"}),
        (dict(category="Neo-Buddhist", family_income=100_000, course="arts"), {"post-matric-sc"}),
        (dict(category="ST", family_income=150_000, course="commerce"), {"post-matric-st"}),
        (dict(category="OBC", family_income=240_000, course="professional"), {"post-matric-obc"}),
        (dict(category="VJNT", family_income=90_000, course="diploma"), {"post-matric-vjnt"}),
        # Exactly at the income limit still qualifies
        (dict(category="SC", family_income=250_000, course="arts"), {"post-matric-sc"}),
        # Rs 1 over the limit does not
        (dict(category="SC", family_income=250_001, course="arts"), set()),
        # Open category, professional course: EBC fee scheme + hostel allowance
        (dict(category="Open", family_income=600_000, course="professional", gender="Female"),
         {"ebc-fee-technical", "panjabrao-hostel-technical"}),
        # EWS gets the EBC fee scheme but (per current data) not the hostel allowance
        (dict(category="EWS", family_income=700_000, course="diploma"), {"ebc-fee-technical"}),
        # Open category, non-professional degree: nothing in current data
        (dict(category="Open", family_income=300_000, course="arts"), set()),
        # Over Rs 8 lakh: nothing
        (dict(category="Open", family_income=900_000, course="professional"), set()),
        # Minority students
        (dict(category="Open", family_income=500_000, course="professional", minority_community="Muslim"),
         {"ebc-fee-technical", "panjabrao-hostel-technical", "minority-professional-technical"}),
        (dict(category="OBC", family_income=300_000, course="commerce", minority_community="Muslim"),
         {"minority-degree-dhe"}),
        (dict(category="OBC", family_income=200_000, course="arts", minority_community="Christian"),
         {"post-matric-obc", "minority-degree-dhe"}),
        # Not a Maharashtra domicile: only the ST scheme, whose page doesn't state a domicile rule
        (dict(category="SC", family_income=100_000, course="arts", maharashtra_domicile=False), set()),
        (dict(category="ST", family_income=100_000, course="arts", maharashtra_domicile=False),
         {"post-matric-st"}),
    ],
)
def test_sample_students(profile, expected):
    assert eligible_ids(**profile) == expected


def test_reasons_explain_the_match():
    student = Student(category="SC", family_income=200_000, gender="Female",
                      course="science", maharashtra_domicile=True)
    [match] = find_eligible(student, ALL)
    codes = [code for code, _ in match.reasons]
    assert codes == ["category", "income", "course_any", "domicile"]


def test_unknown_domicile_rule_is_flagged():
    student = Student(category="ST", family_income=100_000, gender="Male",
                      course="arts", maharashtra_domicile=True)
    [match] = find_eligible(student, ALL)
    assert ("domicile_unknown", {}) in match.cautions


def test_only_verified_rows_shown_by_default():
    verified = load_scholarships()
    assert all(row["status"] == "verified" for row in verified)
