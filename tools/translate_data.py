"""Draft Marathi versions of scholarship details with Claude.

Fills the *_mr columns in data/scholarships.csv for rows where they are empty.
Translations are drafts: a Marathi speaker should review each row and set
mr_reviewed to Yes.

Run from the project folder:
    .\\.venv\\Scripts\\python.exe tools\\translate_data.py
"""
import csv
import json
import sys
import tomllib
from pathlib import Path

import anthropic

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "data" / "scholarships.csv"
SECRETS_FILE = ROOT / ".streamlit" / "secrets.toml"
FIELDS = ["benefit", "documents", "how_to_apply", "notes"]

PROMPT = """Translate these scholarship details from English into simple, clear Marathi (Devanagari) for students who have just finished 12th in Maharashtra.

- Keep every fact exactly: amounts, percentages, limits, names of schemes, portals, departments and documents. Don't add or drop information.
- Keep the ";" separators in documents and how_to_apply: they split list items. Keep the same number of items.
- Keep URLs, "MahaDBT 2.0", "CAP", "GR", "Aadhaar" and course names like B.Ed as they are.
- Use "रु." for Rs.

<details>
{details}
</details>"""

SCHEMA = {
    "type": "object",
    "properties": {f: {"type": "string"} for f in FIELDS},
    "required": FIELDS,
    "additionalProperties": False,
}


def main():
    if not SECRETS_FILE.exists():
        sys.exit(f"Add your API key to {SECRETS_FILE} first (see .streamlit/secrets.toml.example).")
    api_key = tomllib.loads(SECRETS_FILE.read_text(encoding="utf-8"))["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)

    with open(DATA_FILE, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        rows = list(reader)

    for row in rows:
        if all(row[f"{f}_mr"].strip() for f in FIELDS if row[f].strip()):
            continue
        print(f"Translating {row['id']}...")
        details = json.dumps({f: row[f] for f in FIELDS}, ensure_ascii=False, indent=1)
        response = client.beta.messages.create(
            model="claude-opus-5-5",
            max_tokens=16000,
            messages=[{"role": "user", "content": PROMPT.format(details=details)}],
            output_config={"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
        if response.stop_reason != "end_turn":
            print(f"  Skipped ({response.stop_reason})")
            continue
        text = next(b.text for b in response.content if b.type == "text")
        translated = json.loads(text)
        for f in FIELDS:
            row[f"{f}_mr"] = translated[f] if row[f].strip() else ""
        row["mr_reviewed"] = ""

    with open(DATA_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    print("Done. Please review the Marathi columns and set mr_reviewed to Yes for each checked row.")


if __name__ == "__main__":
    main()
