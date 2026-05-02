# FAQ — Frequently Asked Questions (Structured for RAG)

This document is structured as **Q&A chunks** for direct retrieval. Each chunk is self-contained — retrieval can return a single Q&A and have full context. Chunks are tagged with topic for filtering.

---

## Q: How accurate is CampaignIQ's revenue prediction?
**Tags:** model, accuracy, performance

**A:** The production model is **Ridge Regression**, which achieves:
- **Test R² of 0.887 on the original dollar scale** — it explains roughly 89% of revenue variation across 2,540 campaigns.
- **MAE (typical error) of $5,788** — half of all predictions are within this range of actual revenue.
- **RMSE of $38,984** — heavily influenced by ~12 mega-revenue outliers; for typical campaigns, expect MAE-scale error.
- **Train-test gap of 0.003** — essentially zero overfitting.

For a single campaign prediction, give the user a confidence band of **±$5,800** for typical campaigns, wider for predicted high-revenue tail campaigns.

---

## Q: Which model does CampaignIQ use, and why?
**Tags:** model, ridge, comparison

**A:** **Ridge Regression** was selected over Random Forest and XGBoost because:
- It had the lowest train-test gap (0.003 vs 0.146 for XGBoost, which was clearly overfit).
- It scored highest on test R² in original dollar scale (0.887 vs 0.189 for Random Forest, 0.483 for XGBoost).
- It's robust to multicollinearity — the dataset has heavy correlation among impressions/clicks/spend/conversions (0.78–0.93), and Ridge's L2 regularization handles this gracefully.
- It generalizes well into the long-tail mega-revenue region where tree-based models can't extrapolate.

---

## Q: What is the most important driver of campaign revenue?
**Tags:** shap, drivers, conversions

**A:** **Conversions, by a wide margin.** SHAP analysis ranks features by impact on predictions:

1. `log_conversions` — mean SHAP impact of 1.45
2. `ctr_pct` — 0.16 (about 9x less)
3. `log_spend_usd` — 0.11
4. `log_clicks` — 0.10
5. `log_impressions` — 0.09

**Practical implication:** Anything that increases conversions per click (better landing page, better offer, better targeting) has roughly 10x the leverage of optimizing CTR or spend. Always lead recommendations with conversion rate.

---

## Q: Which channel performs best?
**Tags:** channels, search, recommendation

**A:** **Search** — averaging ~$32,800 in revenue per campaign, which is **5.3x more than Display** (~$6,200, the worst performer). The full ranking:

1. Search ~$32,800
2. Video ~$26,500
3. Email ~$26,400
4. Social ~$13,700
5. Affiliate ~$11,800
6. Display ~$6,200

The top recommendation in our analysis: **move 20–30% of Display + Affiliate spend to Search.** This is the single highest-leverage budget reallocation in the dataset.

---

## Q: Should I run Display ads at all?
**Tags:** display, channels

**A:** **Mostly no, with one exception: retargeting.** Display has the worst average revenue (~$6.2K, 5x below Search) and the Ridge model gives `channel_Display` a negative coefficient — controlling for everything else, choosing Display reduces predicted revenue.

**The exception:** Display works for **retargeting warm audiences** (people who already visited your site within 14 days). Tighten the audience, set frequency caps (3–5 per user per week), and treat it as a recovery channel — not a prospecting channel.

---

## Q: What audience should I target?
**Tags:** audience, gen-x, gen-z, targeting

**A:** Counter-intuitively, **Gen X (~$23,000) and Gen Z (~$22,800) are tied at the top** — outperforming Millennials (~$16,800) by 35%+.

Reasons:
- Gen X has higher disposable income and responds well to intent-based search advertising.
- Gen Z drives strong impulse / discovery purchases, especially on mobile and short-form video.
- Millennials are saturated with ads and have developed stronger ad-skipping habits.

**Action:** Don't auto-default to Millennials. Match channel to audience: Gen X → Search/Email, Gen Z → Video/Social.

---

## Q: What does it mean if my campaign is tagged "Star"?
**Tags:** bcg, tier, star

**A:** A **Star ⭐** campaign is in the top tier — high revenue **AND** high efficiency. About 35.8% of campaigns earn this label.

**Action plan:**
1. **Scale spend by 20–25%** (not more — overnight doubling crashes ROAS).
2. **Clone the recipe** to adjacent audiences.
3. **Lock in the creative.** Don't refresh prematurely if it's still working.
4. **Monitor monthly** — Stars eventually saturate.

---

## Q: What does "Question Mark" tier mean and what should I do?
**Tags:** bcg, tier, question

**A:** A **Question Mark ❓** campaign has mixed signals — either high spend with mediocre return, or low spend with promise. 17.3% of campaigns fall here. They're the most dangerous tier because they linger and silently drain budget.

**Set a 30-day decision plan:**
- Days 1–3: Diagnose the weakest metric (CTR? conversion rate? bounce?)
- Days 4–14: Run an A/B test on one variable
- Days 15–25: If the test moved the needle → scale 25% to promote toward Core. If not → run one more test.
- Day 30: **Decision day.** Either it's now Core, or it's a Dog. No more waiting.

---

## Q: Should I kill a Dog campaign immediately?
**Tags:** bcg, tier, dog, kill

**A:** **Yes, within ~1 week**, unless one of these applies:
- It's a deliberate brand awareness experiment with a defined budget cap.
- The tracking might be broken (rule this out first).
- A single fixable issue (broken UTM, wrong audience tag) is suspected.

15.4% of campaigns are Dogs. Past spend is sunk cost — future spend should follow ROI logic. Document why the campaign failed and add it to your team's "do not repeat" list.

---

## Q: When does CampaignIQ predict a campaign will be "successful"?
**Tags:** success, classifier, threshold

**A:** A campaign is labeled **successful** when its predicted revenue lands in the **top 25%** of the dataset — i.e., **revenue ≥ $19,096**.

The success classifier (Random Forest) operates at:
- **84% precision** — when it flags success, it's right 84% of the time.
- **84% recall** — it catches 84% of actually successful campaigns.
- **96% AUC** — strong overall discrimination.

Treat probability ≥ 0.7 as a strong success signal; 0.4–0.7 as borderline; < 0.4 as unlikely.

---

## Q: My campaign is flagged at-risk. What do I do?
**Tags:** churn, risk, diagnostics

**A:** The churn classifier (XGBoost) flags campaigns showing poor engagement signals — typically **bounce rate above 52%** combined with low conversion rate or short session duration. The model has 94% precision, so when it flags, it's almost always right.

**Diagnostic ladder (most common to least):**
1. **Landing page misalignment** (~40%) — ad promises one thing, page delivers another.
2. **Audience saturation / fatigue** (~25%) — refresh creative or audience.
3. **Channel mismatch** (~15%) — Display/Affiliate driving low-intent traffic.
4. **Creative quality** (~10%) — improve ad quality score.
5. **Seasonal / external** (~10%) — sometimes you have to wait it out.

Investigate within 48–72 hours of the flag.

---

## Q: My CTR is high but my conversion rate is low. What's wrong?
**Tags:** conversion, ctr, diagnosis

**A:** Classic **post-click failure** — the ad is winning attention but the landing page or offer isn't closing.

**Check in this order:**
1. **Conversion tracking** — is it firing correctly? (Often the answer.)
2. **Bounce rate** — if > 70%, the page doesn't match the ad.
3. **Page load speed** — > 3 sec on mobile loses 30%+ of traffic.
4. **CTA clarity** — is the next step obvious above the fold?
5. **Form friction** — too many fields? Each field cuts conversion ~5–10%.
6. **Mobile UX** — test on a real phone, not DevTools.

Run a 1-week landing page A/B test on the weakest element. Don't change three things at once.

---

## Q: How do I improve my conversion rate?
**Tags:** conversion, optimization

**A:** Conversion rate is the **single highest-leverage metric** — a 1% → 2% lift doubles revenue at the same spend. Work in tiers:

**Tier 1 (mechanics):**
- Verify tracking is firing
- Page speed under 3s on mobile
- Mobile usability

**Tier 2 (funnel):**
- Reduce form fields (each one costs ~5%)
- Single CTA above the fold
- Match page headline to ad headline

**Tier 3 (trust):**
- Add reviews / testimonials near CTA
- Security / payment trust badges
- Money-back guarantee

**Tier 4 (offer):**
- A/B test value-prop framing
- Price anchoring
- Bundle vs single-item tests

Realistic expectation: tier 1+2 fixes can yield 30–50% lifts on broken funnels; further rounds yield smaller gains.

---

## Q: How accurate is the audience segment classifier?
**Tags:** audience, classifier, caveat

**A:** **Only ~24% accuracy — barely above random (25% for 4 classes).** The audience classifier should **not** be used for production targeting.

Why it fails: behavioral features (CTR, conversion rate, bounce, session duration) aren't strongly distinguishable across Boomers / Gen X / Gen Z / Millennials in this dataset. You can't reverse-engineer the audience from behavior alone.

**Use the labeled audience segment** as the source of truth. The classifier is informational only, useful at most for flagging unusual mismatches.

---

## Q: Why does the Ridge model show negative coefficients on CTR and spend?
**Tags:** model, coefficients, multicollinearity

**A:** This is a **statistical artifact of multicollinearity, not a causal claim.**

The model has `log_conversions` doing most of the work (coefficient +2.22). Once conversions are accounted for, *additional* CTR or spend without additional conversions is wasteful — so the model learns small negative coefficients as a "correction."

This does **not** mean "more spend = less revenue" or "higher CTR hurts." It means: among two campaigns with identical conversions, the higher-spend one was less efficient and slightly underperformed.

**Always interpret regression coefficients alongside SHAP**, which captures actual prediction shifts.

---

## Q: How was the dataset cleaned?
**Tags:** data, quality, preprocessing

**A:** The raw 2,540-row dataset had multiple quality issues that were corrected:
- **36 duplicates** removed
- **35 missing values** in clicks / spend / conversions / bounce / quality score → median-imputed
- **53 invalid entries** corrected (negative impressions, CTR > 100%, clicks > impressions, conversion rate > 100%, negative bounce, negative quality score)
- Final cleaned shape: **2,504 rows × 17 working columns** (expanded to 36 after one-hot encoding)

The cleaning was conservative — no rows dropped beyond exact duplicates.

---

## Q: When should I NOT trust a prediction?
**Tags:** model, caveats, reliability

**A:** Predictions are less reliable when:
- **Predicted revenue is over $100K** — only 12 of 2,540 training campaigns fall in this range; the model has high variance there.
- **The campaign hasn't run yet and you're guessing input values** — the model leans heavily on `log_conversions`. Garbage in, garbage out.
- **Outlier feature combinations** — e.g., extremely high CTR with zero conversions.
- **Brand-new channels** — the model only knows the 6 channels in training data.

For typical-scale campaigns within familiar channel/audience profiles, predictions are reliable within ±$6K MAE.

---

## Q: What's the median ROAS in the dataset?
**Tags:** roas, benchmark

**A:** **3.06x** — every $1 spent returned $3.06 in revenue on the median campaign. This is a healthy benchmark for performance marketing.

**Interpretation tiers:**
- **Concerning:** < 1.5x (likely losing money after COGS)
- **Acceptable:** 1.5–3x
- **Good:** 3–5x
- **Excellent:** > 5x

Pause campaigns predicted to land below 1.5x ROAS.

---

## Q: How do I prepare a new campaign for launch?
**Tags:** launch, checklist

**A:** Pre-launch checklist:
- ☐ Predicted revenue ≥ $5K
- ☐ Predicted ROAS ≥ 1.5x
- ☐ Channel matches objective (Search → Sales, Video → Awareness)
- ☐ Conversion tracking tested end-to-end
- ☐ Landing page audited (mobile + desktop)
- ☐ Audience size between 50K and 5M
- ☐ At least 2 creative variants ready for A/B
- ☐ Frequency cap set (especially Display/Video)
- ☐ Daily budget pacing rule defined
- ☐ Stop-loss rule (e.g., "pause if 7-day ROAS < 1.0")

Run the campaign through CampaignIQ's `/predict` and `/classify` endpoints before launch. If predicted tier is Dog, redesign before launching.

---

## Q: What time features does the model use?
**Tags:** model, features, time

**A:** The model derives three time features from `start_date`:
- `month` (1–12)
- `day_of_week` (0–6)
- `quarter` (1–4)

`quarter` is the strongest of the three (mean SHAP 0.075). The model captures broad seasonality but not finer time-of-day or campaign-duration effects — those features aren't in the dataset.

---

## Q: Can I trust the model for a new product I've never advertised?
**Tags:** model, cold-start, limitations

**A:** **Carefully.** The model uses channel/region/device/audience/objective as proxies for the campaign profile, but it can't account for:
- **Product-market fit** — a great campaign for a bad product still fails.
- **Brand awareness baseline** — established brands convert better than unknown ones.
- **Competitive context** — the model doesn't know your competitors.

Treat the prediction as a **structural baseline** — what the channel/audience/budget combination would normally yield. Then mentally adjust:
- New brand, no awareness: discount predicted revenue by 30–50%.
- Strong brand awareness: predictions probably hold.
- Strong differentiator (10x cheaper, etc.): you may exceed prediction.

---

## Summary for the Chatbot

These Q&A pairs are written so each one stands alone. When retrieving for the chatbot:
1. Match user query to the closest Q.
2. Return the full A — they're already concise.
3. If multiple Qs are relevant, retrieve the top 2–3 and let the LLM synthesize.
4. Always preserve the dataset-specific numbers — generic answers without the actual stats are what made the previous KB feel "too generic."
