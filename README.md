# CampaignIQ — ML Campaign Performance Platform

🏆 **Winner, BNY [event name] Hackathon (₹10,000 award)**

CampaignIQ turns noisy digital-advertising data into revenue models, campaign health scores and plain-language explanations that a marketing team can actually act on — served through a secured API, a React dashboard and a retrieval-grounded AI advisor.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green) ![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6-orange) ![React](https://img.shields.io/badge/React-18-61DAFB)

---

## The problem

A digital marketing firm runs campaigns across Search, Social, Display, Email, Video and Affiliate, but analyses them only descriptively. The data is noisy (duplicates, missing values, impossible entries like clicks > impressions, extreme outliers), so the firm can't tell which campaigns, channels and audiences actually drive revenue — and budget gets misallocated.

**BNY's brief:** build a locally trained ML pipeline that predicts campaign revenue, compares at least three models with 5-fold cross-validation, and explains its predictions with SHAP — with APIs used only to serve the models, not to replace them.

## What we built

| Layer | What it does |
|---|---|
| **ML pipeline** (`notebooks/`) | Cleaning, feature engineering, 3-model comparison, SHAP + LIME, business summary |
| **Model API** (`backend/`) | FastAPI service: single and batch (CSV) revenue prediction, success / risk classification, analytics, JWT-secured |
| **AI Advisor** | RAG over a 12-document knowledge base (ChromaDB + OpenAI) that answers strategy questions — including "can I trust this prediction?" — grounded in the model's real behaviour and limitations |
| **Dashboard** (`frontend/`) | React + Recharts: analytics, predictor, batch upload, BCG-style campaign tiers, advisor chat |

<!-- Add: architecture diagram (CSV → cleaning → models → FastAPI → React / Advisor) -->
<!-- Add: 2–3 screenshots or a short demo GIF -->

---

## Data quality — what we found and fixed

Dataset: **2,540 campaigns, 18 columns.** Revenue is extremely skewed (median $8.3K, max $2.47M, skewness 20.3; 12 campaigns above $100K).

| Issue | Count | Fix |
|---|---|---|
| Duplicate rows | 36 | Removed |
| Missing values (clicks, spend, conversions, bounce, quality score) | ~35 per column (1.4%) | Median imputation (robust to the heavy skew) |
| Clicks > impressions | 15 | Treated as invalid → corrected |
| Negative impressions / CTR / bounce / quality score | 27 | Treated as invalid → corrected |
| CTR or conversion rate > 100% | 11 | Treated as invalid → corrected |

**Features:** log transforms of impressions, clicks, spend and conversions; one-hot encoding of 5 categorical columns; month, day-of-week and quarter from the date; StandardScaler. CPC, CPA and ROAS are computed for analysis but **kept out of the model** — ROAS is derived from revenue and would leak the target.

---

## Modelling — results

Target: `log1p(revenue_usd)`; predictions are converted back to dollars for evaluation.

| Model | 5-fold CV R² (log) | Test R² (log) | Test R² ($) | Test MAE ($) | Train–test gap |
|---|---|---|---|---|---|
| **Ridge Regression** ✅ | **0.827 ± 0.006** | 0.830 | **0.887** | **$5,788** | **0.003** |
| Random Forest | 0.844 ± 0.016 | 0.835 | 0.189 | $9,205 | 0.059 |
| XGBoost | 0.822 ± 0.026 | 0.814 | 0.483 | $7,928 | 0.146 |

### Why Ridge, not the "fancier" models
- **Random Forest** scored best in log space but collapsed on the dollar scale (R² 0.19): tree models can't extrapolate beyond the revenue values they've seen, so they badly under-predict the high-revenue tail.
- **XGBoost** overfit — train R² 0.96 vs test 0.81 (gap 0.146).
- **Ridge** had essentially no overfitting (gap 0.003), the most stable CV score (± 0.006) and the best dollar-scale accuracy. It also handles the strong multicollinearity between impressions, clicks, spend and conversions.

### The bug that taught us the most
Our first approach **removed** the highly correlated volume features (impressions, clicks, spend, conversions; r ≈ 0.76–0.81 with revenue) to avoid multicollinearity. Dollar-scale test R² dropped to **0.02** — we had thrown away the signal. **Log-transforming** those features instead (which tames both the skew and the collinearity) brought Ridge to **R² 0.887**.

### Honest error reporting
RMSE ($38,984) is dominated by the 12 campaigns above $100K. **MAE ($5,788) is the realistic error for a typical campaign**, and predictions above $100K should be treated as order-of-magnitude estimates.

---

## Explainability

- **Global:** SHAP beeswarm and top-10 bar plot. Conversions are by far the strongest driver (~10× the next feature), followed by CTR, spend and seasonality (quarter).
- **Local:** SHAP waterfall + LIME explanations for the best- and worst-performing campaigns, with a plain-language narrative of why each performed as it did.
- **Domain check:** the drivers match marketing intuition — revenue follows conversion *quality*, not raw impressions. Negative Ridge coefficients on CTR and spend are multicollinearity artefacts, not causal effects, and the advisor explains this when asked.

<!-- Add: shap_summary.png and one waterfall plot -->

---

## Campaign health classifiers

| Task | Label | Best model | Test ROC-AUC |
|---|---|---|---|
| Success | Revenue in the top 25% | Random Forest | 0.964 |
| Risk | Bottom-25% revenue **and** above-median bounce rate | Random Forest | [fill in] |
| Audience segment | Gen Z / Millennials / Gen X / Boomers | — | ~24% accuracy (≈ chance) |

**Finding:** audience segment can't be predicted from campaign metrics — performance looks similar across segments. We report this rather than ship a misleading model.

---

## Business recommendations

- Optimise for **conversion rate**, not reach — it is the #1 revenue driver.
- **Search** (best channel), the **East** region and **Tablet** users show the highest average revenue; prioritise testing budget there.
- Median ROAS is **3.06×**, but only 25% of campaigns land in the top revenue quartile — use the success classifier to flag campaigns worth scaling.
- See the notebook's 1-page non-technical summary for the full list.

---

## AI Advisor (RAG)

- **Knowledge base:** 12 curated documents — metrics glossary, channel and audience analysis, model behaviour, SHAP drivers, classifier definitions, playbooks, and model caveats.
- **Retrieval:** chunks embedded into ChromaDB; the top 4 relevant chunks are injected into the prompt.
- **Grounding:** a dedicated caveats document lets the advisor say when *not* to trust a prediction (e.g. tail revenue, sparse channel/audience combinations).
- `/kb-search` endpoint for inspecting retrieval directly.

---

## API

| Endpoint | Purpose | Auth |
|---|---|---|
| `POST /token` | Log in, get JWT | — |
| `POST /predict` | Revenue prediction for one campaign | JWT |
| `POST /classify` | Success and risk classification | JWT |
| `POST /upload-csv` | Batch predictions with success/risk flags | JWT |
| `GET /analytics` | Summary metrics for the dashboard | — |
| `POST /advisor` | RAG-grounded strategy chat | JWT |
| `POST /kb-search` | Inspect retrieval results | — |

Interactive docs at `http://localhost:8000/docs`.

---

## Limitations

- Observational data: the model shows correlation, not causation.
- Conversions are an input, so this estimates revenue from campaign metrics; it is **not** a pre-launch forecaster.
- No uncertainty intervals yet; typical error is roughly ± $11K (≈ 2 × MAE).
- Random 80/20 split, as specified by the brief; a time-based split would better reflect future performance.

---

## Run it

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env        # add OPENAI_API_KEY and JWT secret
uvicorn main:app --reload   # http://localhost:8000/docs

# Frontend
cd frontend
npm install
npm run dev                 # http://localhost:5173
```

Training: open `notebooks/campaigniq_model_training.ipynb` (Colab or Jupyter) with `digital_media_dataset.csv` in the working directory.
