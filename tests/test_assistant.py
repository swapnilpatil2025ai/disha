from assistant import build_system_prompt
from eligibility import Student, find_eligible, load_scholarships

ALL = load_scholarships(include_drafts=True)
STUDENT = Student(category="SC", family_income=200_000, gender="Female",
                  course="science", maharashtra_domicile=True)


def test_prompt_contains_only_matched_scholarships():
    matches = find_eligible(STUDENT, ALL)
    prompt = build_system_prompt(STUDENT, matches, "English")
    assert "Government of India Post-Matric Scholarship (SC)" in prompt
    assert "Post-Matric Scholarship to OBC Students" not in prompt


def test_prompt_asks_for_chosen_language():
    assert "simple Marathi" in build_system_prompt(STUDENT, [], "मराठी")
    assert "simple English" in build_system_prompt(STUDENT, [], "English")


def test_prompt_without_matches_says_so():
    assert "No scholarships matched this profile." in build_system_prompt(STUDENT, [], "English")


def test_prompt_keeps_marathi_text_readable():
    matches = find_eligible(STUDENT, ALL)
    assert "भारत सरकार" in build_system_prompt(STUDENT, matches, "मराठी")
