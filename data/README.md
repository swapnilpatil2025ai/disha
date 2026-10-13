# Scholarship data

`scholarships.csv` is Disha's **source of truth**. The app only shows what is in this file, so every row must be checked against the official source. You can edit it in Excel or Google Sheets; save it as CSV.

## Columns
| Column | Meaning | Example format |
|---|---|---|
| `id` | Short unique ID, lowercase with dashes | `post-matric-sc` |
| `name_en` / `name_mr` | Scheme name in English / Marathi | |
| `provider` | Who runs it | `Social Justice Dept, Govt of Maharashtra` |
| `apply_portal` | Where students apply | `MahaDBT`, `NSP`, `BARTI` |
| `categories` | Eligible categories, separated by `;` (use `Any` if open to all) | `SC;Neo-Buddhist` |
| `minority_only` | `Yes` if only for minority communities (Muslim, Buddhist, Christian, Sikh, Parsi, Jain, Jewish) | `No` |
| `max_family_income_inr` | Annual family income limit in rupees; blank if none | `250000` |
| `min_12th_percent` | Minimum 12th marks; blank if none | `60` |
| `eligible_courses` | Courses covered, separated by `;` (or `Any`) | `Degree;Diploma;Professional` |
| `gender` | `Any`, `Female` or `Male` | `Any` |
| `maharashtra_domicile_required` | `Yes` or `No` | `Yes` |
| `benefit` | What the student gets, in plain words | `Full tuition fee + monthly allowance` |
| `deadline` | Usual application window | `Usually Oct–Dec; check portal` |
| `documents` | Documents needed, separated by `;` | `Caste certificate;Income certificate` |
| `how_to_apply` | Short steps, separated by `;` | |
| `official_url` | Official page (government / provider site only) | |
| `last_verified` | Date you checked it, `YYYY-MM-DD` | `2026-10-14` |
| `status` | `draft` (entered, not yet checked by a person) or `verified` | `draft` |
| `notes` | Anything unusual (e.g. can't combine with another scheme) | |

## Rules
- **Official sources only.** Don't use blogs or coaching sites as the source.
- **If you're unsure, leave it blank** and add a note. A blank is better than a wrong value.
- Update `last_verified` every time you re-check a row.
- **Only `verified` rows will be shown to students.** Draft rows are for review.

## How to verify a row
1. Open the row's `official_url`.
2. Compare categories, income limit, courses, benefit and documents with the page.
3. Check the Marathi name against the portal's मराठी version.
4. Read any **CHECK BEFORE VERIFYING** note and resolve it, for example by reading the linked Government Resolution (GR).
5. If everything matches, change `status` to `verified` and update `last_verified`.
