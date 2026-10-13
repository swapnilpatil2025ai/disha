"""Rules-based scholarship eligibility.

Eligibility is decided here, in plain code, so results are predictable and
testable. The AI assistant (milestone M3) only explains results; it never
decides who qualifies.

Each check returns reason codes (not sentences) so the app can show them in
English or Marathi.
"""
import csv
from dataclasses import dataclass, field
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "scholarships.csv"

CATEGORIES = ["Open", "EWS", "SEBC", "OBC", "SBC", "VJNT", "SC", "Neo-Buddhist", "ST"]
MINORITY_COMMUNITIES = ["Muslim", "Buddhist", "Christian", "Sikh", "Parsi", "Jain", "Jewish"]
GENDERS = ["Female", "Male", "Other"]
COURSES = ["professional", "diploma", "arts", "commerce", "science", "law", "education", "other"]

# Courses that count as "Professional" in the data (technical/professional, usually via CAP).
PROFESSIONAL_COURSES = {"professional", "diploma"}


@dataclass
class Student:
    category: str
    family_income: int
    gender: str
    course: str
    maharashtra_domicile: bool
    minority_community: str | None = None
    marks_12th: float | None = None


@dataclass
class Match:
    scholarship: dict
    reasons: list[tuple[str, dict]] = field(default_factory=list)
    cautions: list[tuple[str, dict]] = field(default_factory=list)


def split(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def load_scholarships(path: Path = DATA_FILE, include_drafts: bool = False) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if include_drafts:
        return rows
    return [row for row in rows if row["status"].strip().lower() == "verified"]


def check(student: Student, s: dict) -> Match | None:
    """Return a Match if the student qualifies for scholarship `s`, else None."""
    match = Match(scholarship=s)

    categories = split(s["categories"])
    if "Any" not in categories:
        if student.category not in categories:
            return None
        match.reasons.append(("category", {"value": student.category}))

    if s["minority_only"].strip() == "Yes":
        if not student.minority_community:
            return None
        match.reasons.append(("minority", {"value": student.minority_community}))

    if s["max_family_income_inr"].strip():
        limit = int(s["max_family_income_inr"])
        if student.family_income > limit:
            return None
        match.reasons.append(("income", {"limit": limit}))

    if s["min_12th_percent"].strip():
        minimum = float(s["min_12th_percent"])
        if student.marks_12th is None:
            match.cautions.append(("marks_unknown", {"min": minimum}))
        elif student.marks_12th < minimum:
            return None
        else:
            match.reasons.append(("marks", {"min": minimum}))

    courses = [c.lower() for c in split(s["eligible_courses"])]
    if "any" in courses:
        match.reasons.append(("course_any", {}))
    elif "professional" in courses and student.course in PROFESSIONAL_COURSES:
        match.reasons.append(("course_professional", {}))
    elif student.course in courses:
        match.reasons.append(("course", {"value": student.course}))
    else:
        return None

    gender = s["gender"].strip() or "Any"
    if gender != "Any":
        if student.gender != gender:
            return None
        match.reasons.append(("gender", {"value": gender}))

    domicile = s["maharashtra_domicile_required"].strip()
    if domicile == "Yes":
        if not student.maharashtra_domicile:
            return None
        match.reasons.append(("domicile", {}))
    elif not domicile:
        match.cautions.append(("domicile_unknown", {}))

    return match


def find_eligible(student: Student, scholarships: list[dict]) -> list[Match]:
    return [m for s in scholarships if (m := check(student, s))]
