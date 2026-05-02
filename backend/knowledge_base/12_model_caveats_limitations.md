# Model Caveats and Known Limitations

This document is the chatbot's "honesty layer." When users ask "is this prediction reliable?", "what could go wrong?", or "should I trust this?", retrieve from here. Being upfront about limitations builds user trust faster than overstating accuracy.

---

## Headline Caveats

1. **Test R² of 0.887 is on the original dollar scale, but RMSE is dominated by 12 outlier campaigns** that exceed $100K revenue. For typical campaigns, MAE of $5,788 is the more honest error estimate.
2. **The dataset is observational, not experimental.** Correlations seen here cannot be cleanly interpreted as causal effects.
3. **The audience classifier is broken** (~24% accuracy). Don't use it for production decisions.
4. **Mega-revenue predictions are noisy** — only 12 of 2,540 training rows exceed $100K, so the model has high variance in that region.
5. **The model is conversion-anchored** — if `log_conversions` is unknown (pre-launch), prediction quality drops because you're feeding in a guess.

---

## Data Quality Limitations (What Couldn't Be Fixed)

### Remaining issues after cleaning

While 53 invalid entries and 36 duplicates were corrected, some structural issues remain:

- **No customer-level identifier** — can't compute true LTV, repeat-purchase rate, or true incrementality.
- **`audience_age` is a proxy column**, not a per-customer field. Don't read it as actual customer ages.
- **No timestamp granularity below day-of-month** — temporal features are limited to month / quarter / day-of-week.
- **No spend pacing / time-series structure** — campaigns are treated as point estimates, not as performance over time.
- **No external features** — economy, weather, competitor activity, news cycle. All ignored.
- **No product / SKU information** — the model can't distinguish a $5 product campaign from a $500 product campaign.

### Imputation creates uncertainty

35 missing values for clicks/spend/conversions/bounce/quality_score were median-imputed. For those ~1.4% of rows, model training included synthetic values that may not reflect reality. This adds a small but nonzero noise floor to predictions.

---

## Model Limitations

### Ridge Regression-specific

- **Linear assumption:** Ridge models a linear relationship in the log-transformed feature space. Real campaigns may have nonlinear interactions (e.g., spend × creative_quality interaction effects) that Ridge can't capture.
- **No feature interactions by default.** The model sees `channel_Search` and `audience_Gen X` independently — it doesn't learn that "Search × Gen X is exceptionally good." A practitioner would catch this; the model won't.
- **Coefficient interpretation pitfalls:** Negative coefficients on CTR / spend / impressions are statistical artifacts of multicollinearity, NOT causal signals. Always interpret alongside SHAP.

### General ML limitations

- **No uncertainty estimates.** The model returns a point prediction. The true 95% confidence interval is roughly **±$11K (≈ 2 × MAE)** for typical campaigns and much wider for tail predictions. Communicate uncertainty when the user is making a decision.
- **No causal claims.** A correlation in this data (e.g., "Tablet outperforms Mobile") could be confounded — maybe Tablet campaigns happened to use better landing pages, not because Tablet itself is better.
- **No incrementality.** The model can't say "if you ran this campaign, you would have generated $X *more* revenue than baseline." It only says "campaigns matching this profile averaged $X."

---

## When the Prediction Is Unreliable

### High-risk prediction zones

| Scenario | Why It's Unreliable | What to Do |
|---|---|---|
| Predicted revenue > $100K | Only 12 training examples in this range | Treat as order-of-magnitude estimate; collect 3–5 actual data points before scaling |
| Pre-launch with no conversion history | Model anchors on log_conversions, which you're guessing | Use prediction as one input among many; pilot with small budget first |
| Channel/audience combo with sparse training data | Model leans on global priors, not local patterns | Run a small test campaign before committing |
| Outlier feature combinations (high CTR + zero conversions) | Likely a tracking issue or fraud, not a real campaign | Investigate the data before trusting any prediction |
| Brand-new channels not in training set | Model can't predict for unseen categories | Don't use the model; rely on industry benchmarks |
| Highly seasonal campaigns (Black Friday, Super Bowl) | Model has limited time-series structure | Adjust manually for known seasonal multipliers |

### Sanity checks before trusting a prediction

1. **Does the predicted revenue fall within ±2× of similar past campaigns?** If not, investigate.
2. **Is the predicted ROAS within reasonable bounds (0.5x–10x)?** Outside this range usually signals an input issue.
3. **Does the SHAP explanation align with intuition?** If conversions dominate the prediction but the campaign has zero conversion history, the prediction is fragile.

---

## Audience Classifier — Known Failure Mode

**Test accuracy: 23%. CV accuracy: 24–26%. Random baseline: 25%.**

This model effectively guesses. Despite that, it's still saved as `audience_classifier.pkl` and exposed via the API for completeness. The chatbot should **always** disclose its accuracy when this output is referenced.

**What to do instead:**
- Trust the labeled audience segment (set by the marketer) as the source of truth.
- Use behavioral data to refine within a segment, not to identify segments.
- For new untargeted traffic, treat audience as unknown rather than letting the classifier guess.

---

## What the Model CAN'T Tell You

Be explicit when these come up:

| Question | Why the Model Can't Answer | Where to Look Instead |
|---|---|---|
| "What's my customer LTV?" | No customer-level data | Your CRM / analytics platform |
| "Is this campaign profitable after COGS?" | No cost-of-goods data | Internal financials |
| "What's the optimal bid for this auction?" | No auction-level data | Platform's bid simulator |
| "Should I run this ad on Meta vs TikTok?" | Dataset has no platform sub-categorization | Platform-specific tests |
| "How long should this campaign run?" | No campaign duration field | A/B test framework |
| "Is my creative fatigued?" | No creative-level performance over time | Creative-level reporting in your ad platform |
| "What competitor is taking my budget?" | No competitive data | Tools like SEMrush / Pathmatics |

---

## Reproducibility and Drift

### Model freshness

The training dataset is a static snapshot. The model **does not retrain automatically**. Performance can degrade if:

- Channel performance shifts (e.g., iOS 14 attribution changes already happened post-2021; further policy changes will impact accuracy).
- Audience behavior changes (Gen Z's media habits change rapidly).
- Macroeconomic conditions shift (recession affects conversion rates broadly).

**Recommendation:** Retrain quarterly, or whenever predicted vs actual deviation exceeds 25% on rolling samples.

### Reproducibility

The training pipeline is deterministic given the input CSV — same inputs produce same `.pkl` files. However:
- Random Forest and XGBoost use random seeds; results can shift slightly without `random_state` set.
- Cross-validation splits use a fixed seed; consistent across runs.

---

## Ethical and Practical Caveats

### What "successful" means here is narrow

A campaign labeled "successful" by the classifier just means it landed in the top 25% of revenue. This says nothing about:
- Brand safety
- Customer satisfaction post-purchase
- Long-term customer value
- Whether the campaign reached the *right* audience ethically

Treat success/tier classifications as **revenue-economics labels**, not holistic campaign quality labels.

### Bias risk in audience-segment effects

The dataset shows Gen X and Gen Z outperforming Millennials. This is the *observed* behavior of the campaigns trained on, not an intrinsic truth about audiences. Different products, different brands, different creative would yield different patterns. Don't generalize beyond the dataset.

### Survivorship in the data

The dataset only contains campaigns that ran to completion and reported revenue. Campaigns that failed silently, were paused early, or had broken tracking are likely under-represented. The model's view of "what works" is filtered through this survivorship.

---

## How the Chatbot Should Communicate Caveats

1. **Don't over-disclaim.** Listing every limitation upfront is annoying and unhelpful. Surface caveats only when relevant.
2. **Lead with the answer, end with the caveat.** "Predicted revenue is $X — note this has typical error of ±$6K and is most reliable for campaigns under $100K."
3. **Be honest about the audience classifier.** When asked about it: state it's near-random and recommend trusting labeled segments.
4. **Don't oversell ROAS predictions.** Mid-range ROAS (1.5–4x) predictions are reliable. Tail predictions (>10x or <0.5x) deserve extra scrutiny.
5. **Frame uncertainty as ranges.** "Likely $15K–$25K" is more useful than "exactly $19,847."

---

## Summary for the Chatbot

When asked about reliability:
1. Cite the model's actual numbers (R² 0.887, MAE $5,788).
2. Identify the specific risk factors for the user's scenario (high-revenue tail, pre-launch, sparse channel).
3. Always disclose audience classifier limitations when its output is referenced.
4. Recommend pilot testing before scaling on any high-stakes prediction.
