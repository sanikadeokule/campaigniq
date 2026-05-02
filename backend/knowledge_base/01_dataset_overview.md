# Dataset Overview — CampaignIQ Training Data

## Summary

CampaignIQ models were trained on **2,540 digital marketing campaigns** spanning six channels, five regions, four device types, and four audience segments. This document is the canonical reference for what the dataset contains, how it was cleaned, and how it should be described to users asking "what data is this based on?"

## Source File

- File: `backend/digital_media_dataset.csv`
- Original shape: 2,540 rows × 18 columns
- After deduplication: 2,504 rows × 17 working columns
- After feature engineering + one-hot encoding: 2,504 rows × 36 columns
- Train/Test split: 2,003 / 501 (≈80/20)

## Schema (Original 18 Columns)

| Column | Type | Description |
|---|---|---|
| campaign_id | id | Unique campaign identifier |
| channel | categorical | Search, Social, Display, Email, Video, Affiliate |
| region | categorical | East, Central, South, North, West |
| device_type | categorical | Desktop, Mobile, Tablet, CTV |
| audience_segment | categorical | Boomers, Gen X, Millennials, Gen Z |
| campaign_objective | categorical | Awareness, Leads, Sales, Traffic |
| impressions | numeric | Total ad impressions served |
| clicks | numeric | Total ad clicks |
| ctr_pct | numeric | Click-through rate (%) |
| spend_usd | numeric | Total media spend in USD |
| conversions | numeric | Number of conversion events |
| conversion_rate_pct | numeric | Conversions / clicks (%) |
| bounce_rate_pct | numeric | Single-page-session rate (%) |
| session_duration_sec | numeric | Average session duration (seconds) |
| audience_age | numeric | Audience age proxy |
| ad_quality_score | numeric | Internal quality score (0–10ish) |
| start_date | date | Campaign start date |
| revenue_usd | **target** | Total revenue generated (model target) |

## Target Variable: `revenue_usd`

The model predicts `revenue_usd` — the total revenue a campaign generated.

| Statistic | Value |
|---|---|
| Mean | $19,395 |
| Median | $8,259 |
| Std Dev | $100,171 |
| Max | $2,467,985 |
| Skewness (raw) | 20.29 (extremely right-skewed) |
| Rows above $100k | 12 of 2,540 (0.47%) |
| Skewness after log(1+x) | -2.26 (near-normal) |

**Key insight:** Revenue is *extremely* right-skewed. A handful of mega-campaigns dwarf the rest. This is why the model trains on `log(1 + revenue_usd)` instead of raw dollars — it stabilizes variance and prevents outliers from dominating the loss.

## Data Quality Issues Found and Fixed

The raw dataset had multiple integrity problems that were corrected during preprocessing:

| Issue | Count | Fix |
|---|---|---|
| Duplicate rows | 36 | Dropped |
| Missing `clicks` | 35 | Median-imputed |
| Missing `spend_usd` | 35 | Median-imputed |
| Missing `conversions` | 35 | Median-imputed |
| Missing `bounce_rate_pct` | 34 | Median-imputed |
| Missing `ad_quality_score` | 35 | Median-imputed |
| Negative impressions | 10 | Set to absolute value |
| Negative CTR | 10 | Clipped to 0 |
| CTR > 100% | 5 | Capped at 100% |
| Clicks > Impressions | 15 | Clicks capped at impressions |
| Conversion rate > 100% | 6 | Capped at 100% |
| Negative bounce rate | 5 | Clipped to 0 |
| Negative ad_quality_score | 2 | Clipped to 0 |

**When users ask "is your data clean?":** Yes — duplicates removed, missing values imputed, and 53 invalid entries (negative or out-of-range values) corrected.

## Feature Engineering Applied

1. **Log transforms** on the four high-skew, high-correlation features:
   - `log_impressions` = log(1 + impressions)
   - `log_clicks` = log(1 + clicks)
   - `log_spend_usd` = log(1 + spend_usd)
   - `log_conversions` = log(1 + conversions)
2. **Time features** extracted from `start_date`: `month`, `day_of_week`, `quarter`
3. **Derived ratios** computed for analytics (not all used in model): `cpc`, `cpa`, `roas`
4. **One-hot encoding** of 5 categorical columns (channel, region, device_type, audience_segment, campaign_objective) — produces 32 final regression features after dropping one reference level per category
5. **StandardScaler** applied so all features have mean 0, std 1

## Final Feature List (32 Regression Features)

Numeric / engineered: `ctr_pct`, `conversion_rate_pct`, `bounce_rate_pct`, `session_duration_sec`, `audience_age`, `ad_quality_score`, `log_impressions`, `log_clicks`, `log_spend_usd`, `log_conversions`, `month`, `day_of_week`, `quarter`

One-hot encoded:
- Channel: Display, Email, Search, Social, Video (Affiliate is reference)
- Region: East, North, South, West (Central is reference)
- Device: Desktop, Mobile, Tablet (CTV is reference)
- Audience: Gen X, Gen Z, Millennials (Boomers is reference)
- Objective: Awareness, Leads, Sales, Traffic

## Correlation Highlights

Variables most correlated with `revenue_usd`:
- `impressions`: 0.811
- `conversions`: 0.793
- `clicks`: 0.779
- `spend_usd`: 0.761

Inter-feature correlations show heavy multicollinearity in the spend/clicks/impressions/conversions cluster (all 0.78–0.93). This is why **Ridge** (L2-regularized linear regression) was selected — it is robust to multicollinearity.

## Important Caveats

- The dataset does **not** contain a unique customer/user ID, so the model cannot do customer-level prediction or LTV estimation.
- `audience_age` is a proxy column, not a per-customer field.
- 12 mega-revenue outliers (>$100k) heavily influence raw-scale RMSE; log-space metrics are more reliable.
- No timestamp granularity below day-of-month — temporal feature engineering is limited to month/quarter/day-of-week.
- The dataset is observational, not experimental — correlations seen here cannot be cleanly interpreted as causal effects.
