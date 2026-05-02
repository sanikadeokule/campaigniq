# BCG Matrix — Campaign Tier Classification

CampaignIQ classifies every campaign into one of four tiers, modeled after the Boston Consulting Group (BCG) growth-share matrix. Use this document for questions like "what does Star tier mean?", "should I keep my Question Mark campaigns?", and "how is tier decided?"

## The Four Tiers

| Tier | Icon | What It Means | Action |
|---|---|---|---|
| **Star** ⭐ | High revenue + high efficiency | Top performers — your winners | Scale aggressively. Increase budget. |
| **Core** 🟢 | Solid revenue + decent efficiency | Reliable workhorses | Maintain. Optimize at the margins. |
| **Question Mark** ❓ | Mixed signals — high spend, mediocre return OR low spend with promise | Could go either way | Test improvements; set a 30-day decision deadline. |
| **Dog** 🐶 | Low revenue + low efficiency | Underperformers | Pause or kill. Reallocate budget. |

## Tier Distribution in the Dataset

From 2,504 working campaigns:

| Tier | Count | % of Total |
|---|---|---|
| **Star** | 896 | 35.8% |
| **Core** | 788 | 31.5% |
| **Question Mark** | 434 | 17.3% |
| **Dog** | 386 | 15.4% |

**Headline takeaway:** Two-thirds of campaigns are healthy (Star + Core = 67.3%). The remaining third (Question + Dog = 32.7%) is where most budget waste hides.

## How Tier Is Computed

Tier is derived from a campaign's revenue and efficiency relative to dataset percentiles:

- **Revenue thresholds:** 25th percentile = $3,212 ; 75th percentile = $19,096
- **Efficiency proxy:** ROAS and conversion rate vs median (median ROAS = 3.06x)

Roughly:
- **Star:** Revenue in top 25% AND ROAS above median
- **Core:** Revenue in middle 50% AND ROAS at or above median (or top 25% with mid efficiency)
- **Question Mark:** Mixed — either high spend with weak return, or low spend with strong unit economics worth scaling
- **Dog:** Revenue in bottom 25% AND ROAS below median

The exact tier rules live in `backend/main.py` under the `/classify` endpoint logic.

## Tier Classifier Performance

A separate ML model also predicts tier from features (without seeing revenue directly):

| Tier | Precision | Recall | F1 |
|---|---|---|---|
| Core | 0.62 | 0.71 | 0.66 |
| Dog | 0.86 | 0.78 | 0.82 |
| Question | 0.65 | 0.45 | 0.53 |
| Star | 0.82 | 0.87 | 0.84 |

**Overall accuracy: 73%** (weighted F1: 0.73)

The model is **strongest at identifying Stars and Dogs** — the unambiguous cases at the extremes. It's weakest on **Question Marks**, which is expected because they're definitionally the ambiguous middle.

---

## What to Do With Each Tier

### ⭐ Stars (35.8% of campaigns)

**Profile:** Top revenue, healthy ROAS, often Search/Video on East/Central regions.

**Playbook:**
1. **Scale spend by 20–40%** while monitoring ROAS — diminishing returns kick in eventually.
2. **Clone the winning recipe** to adjacent audiences/regions before competitors notice.
3. **Lock in the creative.** Don't refresh prematurely if it's still performing.
4. **Document why it's a Star** so future campaigns can borrow the playbook.

**Watch-outs:**
- Stars eventually saturate — track ROAS month-over-month.
- Don't over-concentrate budget in one Star; portfolio risk.

### 🟢 Core (31.5% of campaigns)

**Profile:** Mid-tier revenue, acceptable efficiency, often broader audience targeting.

**Playbook:**
1. **Hold spend steady.** Don't cut what's working.
2. **Run small (10–20%) optimization tests** — creative variants, landing page tweaks, audience expansion.
3. **Watch for tier drift.** A Core campaign sliding toward Question is an early warning.
4. **Promote to Star?** If a Core campaign shows 2+ weeks of accelerating ROAS, test a 25% budget bump.

**Watch-outs:**
- Comfort trap — Core is the easiest tier to ignore, but small optimizations compound.

### ❓ Question Marks (17.3% of campaigns)

**Profile:** The hardest tier to manage. Either underspending on a promising idea, or overspending on a mediocre one.

**Playbook:**
1. **Diagnose first.** Is this a *creative* problem (low CTR), a *targeting* problem (high CTR but low conversion), or a *landing page* problem (high conversion rate after click but high bounce)?
2. **Set a 30-day decision deadline.** Either move it to Core (improvement working) or Dog (kill it).
3. **A/B test one variable at a time.** Swap creative OR audience OR landing page — not all three at once, you won't learn anything.
4. **Look at the SHAP values** for individual predictions to understand what's holding it back.

**Watch-outs:**
- Question Marks are budget-eaters. Without a deadline they linger and silently drain spend.

### 🐶 Dogs (15.4% of campaigns)

**Profile:** Bottom 25% revenue AND ROAS below median. Often Display + West/North + mismatched audience.

**Playbook:**
1. **Pause within 1 week** unless there's a strategic reason (e.g., brand awareness experiment).
2. **Reallocate budget to Stars** (highest ROI per dollar moved).
3. **Diagnose retroactively.** What went wrong? Channel mismatch? Bad creative? Wrong audience? Add it to your playbook as a "do not repeat."
4. **Don't try to rescue most Dogs.** The data shows Dog → Star transitions are rare. Cut and move on.

**Watch-outs:**
- "But we just launched it" — sunk cost. Past spend is gone; future spend should follow ROI logic.
- Sometimes a Dog is a Dog because of one fixable issue (broken landing page, wrong UTM tag). Quick diagnosis first.

---

## Tier vs Success Flag — They're Different Things

The chatbot will sometimes need to clarify: **tier and "successful campaign" are related but not identical.**

- **Success flag** (binary): Did the campaign hit a revenue threshold (top 25%, > $19,096)? — see `07_success_churn_classification.md`.
- **Tier** (4-class): Where does it sit on the revenue × efficiency 2×2 grid?

A campaign can be flagged "successful" by revenue but still rank as Question Mark if it required massive spend (poor efficiency). A Star is both successful AND efficient.

## Summary for the Chatbot

When asked about tier:
1. State the tier clearly with the icon (Star ⭐, Core 🟢, Question ❓, Dog 🐶).
2. Give the dataset distribution to anchor expectations (e.g., "Only 35.8% of campaigns are Stars — being a Star means top quartile.").
3. Always pair tier with an action — tier without action is just a label.
4. Note the classifier's confidence (especially shaky on Question Marks).
