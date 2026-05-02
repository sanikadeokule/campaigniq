# ML Model Behavior — Ridge Regression, SHAP, and What Drives Predictions

This is the canonical reference for the prediction model. Use it for questions like "how accurate is this?", "what drives the prediction?", "why didn't you pick XGBoost?", and "can I trust this for my campaign?"

## Production Model: Ridge Regression

CampaignIQ uses **Ridge Regression** (L2-regularized linear regression) as the production revenue prediction model.

### Why Ridge Was Selected

Three models were trained and compared:

| Model | CV R² (log) | Test R² (log) | Test R² (orig $) | Train-Test Gap | Status |
|---|---|---|---|---|---|
| **Ridge Regression** | 0.827 ± 0.006 | 0.830 | **0.887** | 0.003 | ✅ **Selected** |
| Random Forest | 0.844 ± 0.016 | 0.835 | 0.189 | 0.059 | Good CV, poor on raw $ |
| XGBoost | 0.822 ± 0.026 | 0.814 | 0.483 | **0.146** | Overfit (gap > 0.10) |

### Why Not Random Forest or XGBoost?

- **Random Forest** had the best cross-validated log R² (0.844), but its test R² on the original dollar scale was only 0.189 — it badly mispredicts the high-revenue tail because tree-based models can't extrapolate beyond seen values.
- **XGBoost** was visibly overfit: train R² was 0.96 but test R² was 0.81, a gap of 0.146 — well above the 0.10 overfit threshold.
- **Ridge** had the lowest train-test gap (0.003 — essentially zero overfitting) AND the highest test R² on the original dollar scale (0.887). It is robust to the heavy multicollinearity in this dataset and extrapolates well into the long-tail revenue region.

### Model Performance Summary

| Metric | Value | Interpretation |
|---|---|---|
| **Test R² (original $)** | **0.887** | Explains ~89% of variance in revenue |
| Test RMSE (original $) | $38,984 | Average prediction error in dollars |
| Test MAE (original $) | $5,788 | Median typical error (less affected by outliers) |
| 5-fold CV R² (log) | 0.827 ± 0.006 | Stable across data splits |
| Train-Test Gap | 0.003 | Essentially zero overfitting |

**The headline:** "The model explains 89% of revenue variation across our 2,540 campaigns, with an average error of about $39K. RMSE is dominated by ~12 mega-revenue outliers; MAE of $5,788 is closer to the typical campaign experience."

---

## Top Features by SHAP (What Actually Drives Predictions)

SHAP measures how much each feature shifts a prediction away from the dataset mean. Ranked by mean absolute SHAP value:

| Rank | Feature | Mean \|SHAP\| | What It Means |
|---|---|---|---|
| 1 | `log_conversions` | **1.450** | Conversions are the overwhelming driver. Far above everything else. |
| 2 | `ctr_pct` | 0.160 | Better creative = more clicks = more revenue opportunity |
| 3 | `log_spend_usd` | 0.112 | Spend correlates, but not as much as conversion *quality* |
| 4 | `log_clicks` | 0.098 | Clicks matter, but only via conversions |
| 5 | `log_impressions` | 0.089 | Volume helps, but with diminishing returns |
| 6 | `quarter` | 0.075 | Seasonality has a real effect |
| 7 | `audience_segment_Millennials` | 0.055 | Audience targeting effects |
| 8 | `conversion_rate_pct` | 0.053 | Reinforces the conversion theme |
| 9 | `audience_segment_Gen Z` | 0.044 | Audience targeting effects |
| 10 | `month` | 0.042 | Within-year seasonality |

### The Number One Insight: Conversions Dominate

`log_conversions` has nearly **10x** the SHAP impact of the second-most-important feature. This is the single most important takeaway:

> **The amount of conversions a campaign drives — and the quality of conversions per click — overwhelmingly determines revenue. Chasing impressions or clicks without conversion focus is suboptimal.**

This is why every recommendation in CampaignIQ leads with "improve conversion rate."

---

## Ridge Coefficients (What Each Feature Does Linearly)

These are the actual learned linear weights (after StandardScaler), so they're directly comparable.

### Top 10 by absolute coefficient

| Feature | Coefficient | Direction |
|---|---|---|
| log_conversions | **+2.220** | Increases revenue |
| ctr_pct | -0.210 | **Decreases** (counter-intuitive — see below) |
| log_impressions | -0.169 | Decreases |
| log_clicks | +0.168 | Increases |
| log_spend_usd | -0.148 | **Decreases** (after controlling for conversions) |
| conversion_rate_pct | -0.084 | Slight decrease |
| quarter | -0.082 | Later quarters slightly lower |
| audience_segment_Millennials | +0.068 | Slight boost vs Boomers reference |
| channel_Display | -0.059 | Drag (vs Affiliate reference) |
| audience_segment_Gen Z | +0.049 | Slight boost vs Boomers reference |

### Why CTR and Spend Have Negative Coefficients (Important!)

This is a classic case where **regression coefficients ≠ causal effects** in the presence of correlated features.

- The model already has `log_conversions` doing most of the work.
- Once conversions are accounted for, *additional* CTR or spend without additional conversions is wasteful — so the model learns a small negative coefficient as a "correction."
- This does **not** mean "spending more is bad" or "higher CTR hurts revenue." It means "two campaigns with identical conversions but one has higher spend → the higher-spend one was less efficient and slightly underperforms."

Always interpret these coefficients in conjunction with SHAP, which captures actual prediction shifts.

---

## When to Trust the Prediction

### Predictions are RELIABLE when:
- The campaign profile (channel, audience, region, device, objective) is well-represented in the training data.
- Feature values are within the observed range — typical e-commerce/lead-gen scale.
- The campaign has a real conversion mechanism (model is conversion-anchored).

### Predictions are LESS RELIABLE when:
- **Mega-campaigns ($100k+ revenue):** Only 12 of 2,540 training examples — high variance.
- **Brand-new channels not in training:** The 6 channels are fixed.
- **Outlier feature combinations:** e.g., extremely high CTR with zero conversions.
- **Pre-launch campaigns with no historical conversion data:** The model leans on `log_conversions`. If you predict for a campaign that hasn't run yet, you're feeding in a guess.

### Confidence Heuristic

For a single-campaign prediction, give the user a band: **±$5,800 (MAE)** is the typical error magnitude. For high-revenue tail campaigns, expect wider bands (RMSE up to ±$39k). The model is most accurate on campaigns near the median ($8,259) and weakest on the rare $100k+ campaigns.

---

## What Happens at Inference Time

The pipeline at `POST /predict` does:
1. Load the input JSON (channel, region, device, audience, objective, impressions, clicks, spend, conversions, ctr, conversion_rate, bounce_rate, session_duration, age, quality_score, start_date)
2. Engineer features identically to training (log transforms, time features, one-hot encoding aligned to `feature_names.pkl`)
3. Apply the same `StandardScaler` from training
4. Predict in log-space → inverse-transform via `expm1` to get back to dollars
5. Optionally compute SHAP values for explainability

The classifier endpoints (`/classify`) use the same preprocessed features but route through `success_classifier.pkl` and `churn_classifier.pkl`.

---

## Summary for the Chatbot

Key facts to surface:
1. **Model:** Ridge Regression. **Accuracy:** 89% R². **Avg error:** $5,788 (median) to $38,984 (RMSE-weighted).
2. **Top driver:** Conversions, by a wide margin. Anything that increases conversions increases predicted revenue.
3. **Confidence:** Typical campaign predictions are within ±$6k. Mega-revenue predictions are noisier.
4. **Why not XGBoost:** It overfit. Ridge generalizes better here.
5. **Coefficient quirks:** Negative coefficients on CTR/spend are statistical artifacts of multicollinearity — don't read them as "more spend = less revenue."
