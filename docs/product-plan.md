# Disha: Product Plan (v0.1)

*Disha (दिशा) = "direction". Working name, easy to change.*

## 1. Problem
After 12th, many students in Maharashtra don't know what options they have or what support they can get. The information exists, but it's spread across government portals, coaching ads and word of mouth, and much of it is only in English. Students from SC, ST, OBC, VJNT, minority and low-income families are hit hardest: **many miss scholarships they qualify for because nobody told them, or because the process seemed too complicated.**

## 2. Users
| User | Situation | What they need |
|---|---|---|
| **Student** (17–19, just finished 12th) | Often the first in the family to go to college. Uses a basic smartphone with patchy internet. Prefers Marathi. | "Which scholarships can I get, and what do I do next?" in simple language |
| **Teacher / NGO worker** | Helps 20–200 students each year. Short on time. | Quickly check eligibility for each student and give them a printable or shareable checklist |

## 3. Goal of the MVP
Help a post-12th student in Maharashtra **find every scholarship they qualify for and know exactly how to apply** in under 5 minutes, in English or Marathi. Also show 2–3 suitable career paths as a starting point.

### In scope (v1)
- A short questionnaire: stream, marks, category, family income, gender, disability, district, interests
- Eligible scholarships, with amount, deadline, documents needed, step-by-step application process and the **official link**
- 2–3 suggested career paths with simple explanations (duration, cost, entrance exams)
- A chat assistant for follow-up questions, which answers **only from verified data**
- English + Marathi
- **Teacher mode:** check several students one after another, and share or print each student's result
- Works well on a cheap phone with slow internet

### Out of scope (later versions)
Studying abroad · in-depth career counseling · other states · user accounts · applying from inside the app · Hindi

## 4. Key product decisions
1. **Rules decide eligibility; AI explains it.** Eligibility is checked by plain code against verified criteria, never guessed by the AI. The AI does what it's good at: conversation, simple explanations and translation. This keeps answers accurate and testable.
2. **Verified data is the source of truth.** Every scholarship has an official source link and a "last verified" date. If the information isn't in our data, the assistant says "I don't know" and points to the official portal.
3. **No login, minimal personal data.** Profile answers are used for that session only and are not stored. Caste and income are sensitive, and many users are minors.

## 5. Data (scholarships to verify first)
Start with roughly 20 of the highest-impact schemes, each checked against its official source:
- **MahaDBT portal** schemes (post-matric scholarships for SC / ST / OBC / VJNT / SBC, tuition-fee and exam-fee reimbursement, EBC and hostel allowance schemes)
- **National Scholarship Portal** (central post-matric and minority scholarships)
- Maharashtra institutes that run student support and coaching schemes: **BARTI, TRTI, MAHAJYOTI, SARTHI**

*Each entry: name · provider · who is eligible (category, income limit, marks, course, gender) · amount · deadline · documents · how to apply · official link · last verified date.*

## 6. Success metrics
| Type | Metric | MVP target |
|---|---|---|
| **North star** | % of students who find ≥1 eligible scholarship **and open its official link** | ≥ 60% |
| Usability | Questionnaire completion rate | ≥ 70% |
| Usability | Time to first result | < 3 min |
| **Accuracy (evals)** | Precision: scholarships shown that the student really qualifies for | ≥ 95% |
| **Accuracy (evals)** | Recall: qualifying scholarships we found | ≥ 90% |
| **Trust** | Made-up scholarships, amounts or deadlines | **0** |
| **Fairness** | Career suggestions stay equally ambitious when only category or gender changes | No difference |
| Language | Marathi answers rated clear and correct by native speakers | ≥ 4 / 5 |

## 7. Evals plan
- **Eligibility test set:** 40 sample student profiles with the correct scholarship list worked out by hand. Run automatically after every change.
- **Made-up facts check:** 30 tricky questions (fake schemes, missing information). The assistant must not invent an answer.
- **Fairness check:** pairs of profiles that are identical except for category or gender. Compare the career suggestions.
- **Marathi review:** 2–3 native speakers rate a sample of answers.

## 8. Risks & mitigations
| Risk | Mitigation |
|---|---|
| Out-of-date deadlines or amounts | "Last verified" date on every item, links to the official portal, and a recurring check |
| AI makes up facts | Rules-based eligibility, answers only from verified data, and the fact-check evals |
| Bias in career suggestions | Fairness evals, and showing a range of options |
| Sensitive data | No accounts, nothing stored, collect only what's needed |
| Low connectivity | Lightweight pages, short answers |
| Students over-trust the tool | Clear note: "Always confirm on the official portal before applying" |

## 9. Tech (kept simple)
Python · Streamlit (web app that works on mobile) · Claude API (chat, explanations, Marathi) · scholarship data in a simple file/SQLite · free deployment on Streamlit Community Cloud.

## 10. Milestones
| # | Milestone | Done when |
|---|---|---|
| M0 | Setup | Repo on GitHub, app runs locally |
| M1 | Data | ~20 scholarships verified and entered |
| M2 | Eligibility + results page | Questionnaire → correct list, eligibility tests passing |
| M3 | AI assistant + Marathi | Chat answers from data only; language switch works |
| M4 | Evals | All four eval sets run; results recorded |
| M5 | Launch & learn | Live link; tested with 5–10 students and 1–2 teachers; feedback noted |

## 11. Open questions
- Can we find 1–2 teachers or NGOs to test with early?
- Which career paths should v1 cover? (e.g. engineering, medical, pharmacy, nursing, law, B.Com/CA, BA + UPSC/MPSC, ITI/diploma, design)
- Is a WhatsApp version worth exploring later, since that's where many students already are?
