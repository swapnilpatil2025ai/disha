"""Checks on the scholarship data file itself."""
import re

import pytest

from eligibility import load_scholarships, split

ALL = load_scholarships(include_drafts=True)
TRANSLATED = ["benefit", "documents", "how_to_apply", "notes"]


def numbers(text: str) -> list[str]:
    return sorted(re.findall(r"\d[\d,.]*\d|\d", text.replace(",", "")))


@pytest.mark.parametrize("row", ALL, ids=[r["id"] for r in ALL])
def test_marathi_keeps_every_number(row):
    for field in TRANSLATED:
        if row[f"{field}_mr"].strip():
            assert numbers(row[f"{field}_mr"]) == numbers(row[field]), field


@pytest.mark.parametrize("row", ALL, ids=[r["id"] for r in ALL])
def test_marathi_keeps_list_items(row):
    for field in ["documents", "how_to_apply"]:
        if row[f"{field}_mr"].strip():
            assert len(split(row[f"{field}_mr"])) == len(split(row[field])), field


@pytest.mark.parametrize("row", ALL, ids=[r["id"] for r in ALL])
def test_official_links_are_government_sites(row):
    assert row["official_url"].startswith("https://mahadbt.maharashtra.gov.in/")
