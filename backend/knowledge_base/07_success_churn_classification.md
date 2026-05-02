# Success and Churn Classification

CampaignIQ has two binary classifiers and one multi-class audience predictor. This document explains how each one is defined, how well it performs, and how the chatbot should interpret their outputs.

## 1. Success Classifier — "Will this campaign be successful?"

### Definition

A campaign is labeled **successful** if its revenue lands in the **top 25%** of the dataset.

- **Success threshold:** revenue ≥ $19,096 (75th percentile)
- **Floor reference:** 25th percentile = $3,212

### Class Distribution

| Class | Count | % |
|---|---|---|
| Not Successful (0) | 1,878 | 75.0% |
| **Successful (1)** | 626 | 25.0% |

**Implication:** Only 1 in 4 campaigns is "successful" by this definition. A predicted "successful" flag is therefore a *strong* signal — the model is saying this campaign clears a high bar.

### Model Performance

Three classifiers were tested:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | CV AUC |
|---|---|---|---|---|---|---|
| Ridge Classifier | 0.854 | 0.686 | 0.768 | 0.725 | 0.932 | n/a |
| **Random Forest** | **0.922** | **0.847** | **0.840** | **0.843** | **0.964** | **0.978 ± 0.006** |
| XGBoost | 0.920 | 0.840 | 0.840 | 0.840 | 0.970 | 0.979 ± 0.006 |

**Production model:** Random Forest (Ridge is faster but lower F1; RF and XGB are nearly tied — RF chosen for stability).

### How to Interpret Output

- **Predicted Successful (1):** Model is highly confident (~84% precision). When it flags a campaign as successful, it's right ~84% of the time.
- **Predicted Not Successful (0):** Default class — most campaigns. Don't read this as "definitely fail," just "not in the top quartile."
- **Probability score:** The endpoint returns a probability. Treat ≥ 0.7 as a strong success signal; 0.4–0.7 as borderline; < 0.4 as unlikely.

### Common User Questions

**Q: My campaign has a 60% success probability — is that good?**
A: It's borderline. The model thinks the campaign is *more likely than not* to land in the top quartile, but only weakly. Look at the SHAP/factor explanation to see what's pushing it up or down before increasing budget.

**Q: Why was my campaign predicted not successful when revenue was high?**
A: Most likely the prediction was made with input values that didn't match the actual campaign. Or the campaign falls in the 16% of cases the classifier mislabels.

---

## 2. Churn / Risk Classifier — "Is this campaign at risk?"

### Definition

A campaign is flagged **at-risk (churn)** if it shows poor engagement signals:
- Bounce rate above the dataset median (52.12%)
- Combined with low conversion rate or short session duration

### Class Distribution

| Class | Count | % |
|---|---|---|
| Not at risk (0) | 2,208 | 88.2% |
| **At risk (1)** | 296 | 11.8% |

### Model Performance

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | CV AUC |
|---|---|---|---|---|---|---|
| Ridge Classifier | 0.904 | 0.789 | 0.254 | 0.385 | 0.934 | n/a |
| Random Forest | 0.962 | 0.955 | 0.712 | 0.815 | 0.987 | 0.975 ± 0.009 |
| **XGBoost** | **0.974** | **0.942** | **0.831** | **0.883** | **0.991** | **0.983 ± 0.005** |

**Production model:** XGBoost (best F1 and AUC).

### Interpretation Notes

- **Class imbalance is real** — only 11.8% of campaigns are at-risk, so accuracy alone is misleading. Look at F1 and recall.
- **High precision (0.94)** means false alarms are rare — when the model says "at risk," it's almost always right.
- **Recall of 0.83** means the model catches ~83% of actual at-risk campaigns; ~17% slip through.

### How to Use the Flag

- **At-risk = 1, high confidence:** Investigate within 48–72 hours. Common fixes: landing page audit, audience refresh, creative swap.
- **At-risk = 1, low confidence (< 0.6):** Watch but don't panic. Could be a temporary dip.
- **At-risk = 0:** No action needed; revisit at next normal review cycle.

### Common Root Causes (Diagnostic Guide)

When churn=1 is triggered, the typical fixes ranked by frequency:

1. **Landing page misalignment** (~40% of cases) — ad creative promises one thing, landing page delivers another.
2. **Audience saturation / fatigue** (~25%) — same creative shown to same audience too long.
3. **Channel mismatch** (~15%) — Display / Affiliate driving low-intent traffic.
4. **Creative quality** (~10%) — low ad quality score dragging engagement down.
5. **Seasonal / external factors** (~10%) — e.g., off-cycle for the product category.

---

## 3. Audience Segment Classifier — Use With Extreme Caution

### What It Tries to Do

Predict which audience segment (Boomers / Gen X / Gen Z / Millennials) a campaign is targeting, based on behavioral features alone (without seeing the segment label).

### Performance — It Doesn't Work Well

| Model | Test Accuracy | CV Accuracy |
|---|---|---|
| Random Forest | 0.230 | 0.245 ± 0.014 |
| **XGBoost** | **0.236** | **0.259 ± 0.019** |

**Random baseline for 4 classes: 25%.** The model performs at **~24–26%** — barely above random.

### Why It Fails

Behavioral features (CTR, conversion rate, bounce rate, session duration, etc.) are not strongly distinguishable across audience segments in this dataset. Audience targeting decisions create a campaign's behavior, but you can't reverse-engineer the audience from the behavior alone.

### Confusion Matrix Pattern

The XGBoost confusion matrix shows roughly uniform misclassification across all four segments — no segment is reliably identifiable. The model essentially guesses.

### Important: Do NOT Use This in Production

The audience classifier:
- ❌ Should not drive targeting decisions
- ❌ Should not override marketer-assigned segments
- ✅ Can be used to flag *unusual* campaigns where predicted ≠ actual (might indicate audience-creative mismatch)
- ✅ Documents that audience identification is intrinsically hard from behavior alone

If a user asks the chatbot "what audience is this campaign for?", the answer should be:
> "I can predict it, but my audience classifier only achieves ~24% accuracy — barely above random. The campaign's labeled audience segment is the source of truth."

---

## Threshold Reference Table (Quick Lookup)

| Question | Threshold | Source |
|---|---|---|
| When is a campaign "successful"? | Revenue ≥ $19,096 (top 25%) | 75th percentile of dataset |
| Floor for "low revenue"? | Revenue ≤ $3,212 | 25th percentile |
| Median revenue? | $8,259 | dataset median |
| Median ROAS? | 3.06x | dataset median |
| Median bounce rate? | 52.12% | dataset median |
| When to flag churn risk? | Bounce > 52.12% AND low conversion or session | classifier rule |

## Summary for the Chatbot

1. **Success classifier** is reliable (84% precision, 96% AUC). Trust its high-confidence outputs.
2. **Churn classifier** is also strong (94% precision, 99% AUC). Use it as an early-warning system.
3. **Audience classifier** is broken — only 24% accuracy. Don't rely on it for any production decision. Mention this caveat openly when a user asks about it.
