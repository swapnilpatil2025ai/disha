"""Fairness checks on the eligibility rules (no AI involved)."""
import itertools

from eligibility import CATEGORIES, COURSES, MINORITY_COMMUNITIES, Student, find_eligible, load_scholarships

ALL = load_scholarships(include_drafts=True)
INCOMES = [50_000, 250_000, 500_000, 800_000, 1_000_000]


def ids(student: Student) -> set[str]:
    return {m.scholarship["id"] for m in find_eligible(student, ALL)}


def test_gender_never_changes_eligibility_for_gender_neutral_schemes():
    """No scheme in the data is gender-specific, so girl/boy/other must get the same list."""
    assert all(row["gender"] in ("", "Any") for row in ALL), "update this test if a gender-specific scheme is added"
    for category, income, course, minority in itertools.product(
            CATEGORIES, INCOMES, COURSES, [None] + MINORITY_COMMUNITIES):
        results = {frozenset(ids(Student(category=category, family_income=income, gender=g, course=course,
                                         maharashtra_domicile=True, minority_community=minority)))
                   for g in ("Female", "Male", "Other")}
        assert len(results) == 1, (category, income, course, minority)


def test_every_minority_community_is_treated_the_same():
    for category, income, course in itertools.product(CATEGORIES, INCOMES, COURSES):
        results = {frozenset(ids(Student(category=category, family_income=income, gender="Female",
                                         course=course, maharashtra_domicile=True, minority_community=m)))
                   for m in MINORITY_COMMUNITIES}
        assert len(results) == 1, (category, income, course)
