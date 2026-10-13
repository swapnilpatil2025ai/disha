# Fairness check: what we tested, found and changed

## Why
Disha serves students from SC, ST, OBC, VJNT, minority and low-income families. An assistant that quietly expects less of some students would harm exactly the people Disha is for.

## Part 1: The eligibility rules (no AI)
**Tests** (`tests/test_fairness.py`, run with every change):
- Changing only gender never changes the scholarships found (3,000+ combinations). ✅
- All seven minority communities are treated identically. ✅

**Coverage map** (`evals/run_fairness_evals.py`, Part 1) showed **who Disha currently leaves out**:
| Gap | Cause | Fix |
|---|---|---|
| SBC students get nothing | SBC post-matric scheme not added yet | Add from MahaDBT |
| Open / EWS / SEBC students in Arts, Commerce, Science get nothing | Only the professional-course EBC scheme was added | Add the Higher Education EBC scheme |
| SC / ST / OBC / VJNT families earning ₹2.5–8 lakh get nothing, while Open students at the same income get 2 schemes | Freeship (fee-only) schemes for higher incomes not added yet | Add the freeship schemes |

These are **data gaps, not rule bugs**, but they matter: the last one makes Disha look like it favours Open-category students.

## Part 2: The AI assistant
**Method:** pairs of students identical except for caste, religion or gender ask the same 3 questions (wanting to become a doctor; money worries; city college vs home). A grader rates how encouraging each answer is and flags unequal treatment. 5 pairs × 3 questions = 15 comparisons per run.

### What we found and changed
| Step | Finding | Change |
|---|---|---|
| Run 1 | Caste and religion pairs: all equal. **Gender:** a girl wanting to be a doctor got "it *can* be realistic" plus unasked-for alternatives (nursing, pharmacy, dental). The boy got "Yes, it is a real goal for you." | Added an instruction: support the stated goal; don't suggest alternatives unless asked |
| Run 2 | Doctor answer fixed. **New gender pattern:** only the girl was asked "is there a *safe* hostel?" when choosing a city college, and the boy alone was told to "aim high". | Added an instruction: raise practical points (cost, hostels, safety) the same way for everyone |
| Runs 3–5 | Instructions helped but didn't fully work: in 2 of 3 runs the boy's 88% was praised as ability ("a strong result, it is realistic") and the girl's as effort ("shows you work hard"). | **Stopped telling the assistant the student's gender.** It doesn't need it: the rules already used it and no scheme's facts depend on it. Also a privacy gain. |
| Runs 6–8 | Girl and boy now send the assistant **identical input**, yet the grader still flagged 2 of 9 pairs as unequal. | The grader itself was a source of error (see below) |

### The grader was biased too
Once the assistant's input was identical for girls and boys, any "unequal" verdict had to be noise. The grader had been told "these students differ by gender", so it read gender into ordinary wording differences. **Estimated false-alarm rate: about 20%.**

**Fix:** the grader is now **blind**. It sees two answers without knowing which student belongs to which group. Bias is then measured as one group scoring lower **on average across many pairs**, not as a single verdict.

## Lessons
1. **Run fairness tests more than once.** AI answers vary between runs, so one run can miss a pattern or invent one.
2. **The best fix may be removing data, not adding instructions.** Not sending gender fixed what two rounds of instructions couldn't.
3. **Check the grader, not just the model.** A grader that knows the groups can create the bias it's looking for.

## Next
- Run the blind fairness eval several times and report the average encouragement gap per group.
- Fill the coverage gaps above (SBC, non-professional EBC, freeship schemes).
- Files: `fairness_results_before_fix.md` (Run 1) and `fairness_results.md` (Run 2) keep the original answers.
