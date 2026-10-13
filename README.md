# Disha (दिशा)

**Helping students in Maharashtra find the scholarships and career paths open to them after 12th, in English and Marathi.**

Many students, especially from SC, ST, OBC, VJNT, minority and low-income families, miss scholarships they qualify for because the information is scattered, complicated or only in English. Disha asks a few simple questions and shows:

- every scholarship the student is eligible for, with documents needed, steps to apply and the official link
- 2–3 career paths that suit them, explained simply
- an assistant that answers follow-up questions **only from verified information**

It's built for students and for the teachers and NGO workers who guide them.

> **Status:** early development (milestone M0: setup). See the [product plan](docs/product-plan.md).

## Principles
1. **Accurate before clever.** Eligibility is checked by rules against verified data. The AI explains; it never guesses facts.
2. **Always point to the official source.** Every scholarship links to its official portal with a "last verified" date.
3. **Private by default.** No accounts, and student answers are not stored.

## Run it locally
Requires Python 3.11+.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
| Path | What it is |
|---|---|
| `app.py` | The web app (Streamlit) |
| `data/scholarships.csv` | Verified scholarship data (see `data/README.md`) |
| `docs/product-plan.md` | Problem, users, scope, metrics, risks, milestones |
