# Marketing Metrics Glossary — Definitions, Formulas, and Benchmarks

This document defines every metric used in CampaignIQ, gives the formula, dataset-specific stats, and industry benchmarks. When the chatbot is asked "what is X?" or "is my CTR good?", retrieve from here.

## CTR — Click-Through Rate

- **Formula:** `(clicks / impressions) × 100`
- **What it means:** The percentage of people who saw the ad and clicked it. A direct measure of creative + targeting fit.
- **Dataset distribution:** Heavily concentrated near 0–5% with a long right tail. A handful of negative or >100% values existed in raw data and were cleaned.
- **Industry benchmarks (2024–2025):**
  - Search ads: 3–6% (Google Search avg ~3.17%)
  - Social: 0.9–1.5% (Facebook ~0.9%, Instagram ~0.8%, TikTok ~1%)
  - Display: 0.05–0.5% (banner blindness)
  - Email: 2–3% click-to-open
  - Video (YouTube): 0.5–1.5%
- **Rule of thumb in this dataset:** CTR > 2% is healthy; CTR < 0.5% on Search/Social is a creative problem.

## CPC — Cost Per Click

- **Formula:** `spend_usd / clicks`
- **What it means:** How much you pay each time someone clicks. Driven by auction competition + Quality Score.
- **Dataset distribution:** Bimodal-ish, peaks around $0.5–$1.5; some outliers at $2.20+ (cap from data cleaning).
- **Industry benchmarks:**
  - Search (high-intent verticals like insurance, legal): $5–$50
  - Search (e-commerce): $1–$3
  - Social: $0.50–$2
  - Display: $0.10–$1
- **Rule of thumb:** CPC alone is meaningless without CPA — cheap clicks that don't convert are still wasted.

## CPA — Cost Per Acquisition (Cost Per Conversion)

- **Formula:** `spend_usd / conversions`
- **What it means:** The all-in cost to win one conversion. The key efficiency metric.
- **Dataset distribution:** Right-skewed, peaks $5–$30, with a tail of inefficient campaigns hitting the $100 cap.
- **Industry benchmarks:**
  - E-commerce: $20–$45
  - Lead generation B2B: $50–$200+
  - SaaS trial signup: $50–$150
- **Rule of thumb:** CPA must be lower than (LTV × target margin) for profitability. A CPA above the campaign's average order value usually signals a kill-or-fix decision.

## ROAS — Return On Ad Spend

- **Formula:** `revenue_usd / spend_usd`
- **What it means:** For every $1 spent, how many $ of revenue came back. The headline efficiency number.
- **Dataset stats:**
  - **Median ROAS: 3.06x** — every $1 spent returns $3.06
  - Long right tail with successful campaigns hitting 15–20x+
- **Industry benchmarks:**
  - Break-even (varies by margin): typically 2–3x for retail, 4x+ for low-margin
  - Excellent: 5x+
  - Concerning: < 1.5x (likely losing money after COGS)
- **CampaignIQ rule:** Pause campaigns predicted below 1.5x ROAS. Scale spend on those above 4x.

## Conversion Rate (`conversion_rate_pct`)

- **Formula:** `(conversions / clicks) × 100`
- **What it means:** Of the people who clicked, what % completed the goal action (purchase, signup, etc.).
- **Importance:** **THE #1 driver of revenue in our SHAP analysis.** Mean SHAP impact ~1.45 — far above any other feature.
- **Industry benchmarks:**
  - E-commerce average: 2–3%
  - Lead gen average: 2–5%
  - Top quartile: 5–10%
  - Best-in-class (e.g., Amazon checkout): 13%+
- **Why it dominates:** A 1% improvement in conversion rate compounds with the same spend — you get more revenue without paying more for traffic. This is why our model and recommendations always lead with conversion rate.

## Bounce Rate (`bounce_rate_pct`)

- **Formula:** `(single-page sessions / total sessions) × 100`
- **What it means:** % of visitors who land and leave without further action. High bounce = landing page misalignment.
- **Dataset distribution:** Roughly normal, centered around 50%, std ~15%. Median 52.12%.
- **Industry benchmarks:**
  - Landing pages: 60–90% (high by design)
  - Content pages: 40–60%
  - E-commerce: 20–45%
- **Interpretation:** Lower is generally better, BUT context matters. A 70% bounce on a "quick answer" content page can be fine. A 70% bounce on a checkout funnel landing page is a crisis.

## Ad Quality Score (`ad_quality_score`)

- **Range:** Internal score, treated as continuous (cleaned of negatives).
- **What it means:** Composite metric blending expected CTR, ad relevance, and landing page experience. Higher quality = better ad placement, often at lower cost.
- **Why it matters:** Affects auction rank in Google Ads (and similar). A low quality score means you pay more per click for worse placement.
- **Rule of thumb:** Below median quality scores correlate with poor downstream conversion, even with strong creative.

## Session Duration (`session_duration_sec`)

- **What it means:** Average time visitors spend on the site after landing.
- **Industry benchmarks:**
  - E-commerce: 2–3 minutes (120–180 sec)
  - Content: 3–5 minutes (180–300 sec)
  - Below 30 sec: usually a bounce signal
- **Use:** A high-CTR campaign with low session duration = strong creative, weak landing page or audience mismatch.

## Impressions, Clicks, Conversions, Spend — The Volume Quartet

- **Impressions:** Times the ad was rendered (not necessarily seen). Top of funnel.
- **Clicks:** Times the ad was clicked. Mid-funnel intent signal.
- **Conversions:** Goal completions (purchase, signup, lead). Bottom of funnel.
- **Spend:** Money paid to the ad platform.

These four are highly correlated (0.78–0.93 with each other) because campaigns scale together. The model log-transforms all four to prevent the long-tail of mega-campaigns from dominating. A campaign with 10x impressions does *not* generate 10x revenue — the relationship is sub-linear, which the log transform captures.

## Derived / Engineered Metrics

These are computed but not always sent to the model:
- `cpc` = spend_usd / clicks
- `cpa` = spend_usd / conversions
- `roas` = revenue_usd / spend_usd

The model relies primarily on **log_conversions, ctr_pct, log_spend, log_clicks, log_impressions, conversion_rate_pct** — see `05_model_behavior.md` for SHAP rankings.

## Quick-Reference Benchmark Table

| Metric | Poor | OK | Good | Excellent |
|---|---|---|---|---|
| CTR (Search) | <1% | 1–3% | 3–6% | >6% |
| CTR (Display) | <0.05% | 0.05–0.2% | 0.2–0.5% | >0.5% |
| Conversion Rate | <1% | 1–3% | 3–7% | >7% |
| ROAS | <1.5x | 1.5–3x | 3–5x | >5x |
| Bounce Rate | >80% | 60–80% | 40–60% | <40% |
| CPA vs AOV | >100% | 50–100% | 20–50% | <20% |

Use these as *defaults* — the bot should always note that healthy benchmarks vary by industry, season, and funnel position.
