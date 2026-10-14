# CampaignIQ — ML Training & Analysis Notebook

## Overview

This directory contains the Google Colab notebook used to explore digital marketing campaign data, engineer features, train and evaluate machine learning models, interpret model predictions, and derive business insights for **CampaignIQ**, a digital media campaign performance optimization project.

The notebook focuses on analyzing campaign performance and predicting revenue, while also exploring campaign success, performance tiers, and audience segmentation. It combines exploratory data analysis, regression, classification, model evaluation, explainable AI (XAI), and business-oriented reporting.

## Objectives

- Understand campaign performance patterns across advertising channels, regions, devices, and audience segments.
- Clean and preprocess campaign data for machine learning.
- Engineer numerical and temporal features to improve model inputs.
- Train and compare multiple regression models for revenue prediction.
- Build classification models for campaign success and campaign tier prediction.
- Evaluate model performance using appropriate regression and classification metrics.
- Interpret model behavior using SHAP and LIME.
- Generate visualizations and a business summary to support campaign analysis and optimization.

## Dataset

The notebook loads the dataset from `digital_media_dataset.csv`.

The analysis uses campaign-related attributes, including:

- **Campaign performance:** impressions, clicks, conversions, revenue and advertising spend.
- **Engagement metrics:** click-through rate (CTR), conversion rate, bounce rate and session duration.
- **Campaign quality:** ad quality score.
- **Categorical attributes:** advertising channel, region, device type and audience segment.
- **Temporal attributes:** campaign date information used to derive month, day of the week and quarter.

The notebook expects the dataset to be available in the runtime's working directory. Update the file path if using Google Drive or another environment.

## Workflow and Implementation

### 1. Exploratory Data Analysis (EDA)

The notebook examines the dataset's structure, data types, missing values, duplicate records, numerical distributions, and relationships between campaign variables.

Visualizations are generated to explore:

- Revenue and other numerical feature distributions.
- Outliers and variability in campaign metrics.
- Correlations between numerical variables.
- Performance differences across channels, regions, devices and audience segments.
- Relationships between advertising activity, engagement and revenue.

These analyses help identify data-quality issues and establish an initial understanding of campaign performance.

### 2. Data Cleaning and Preprocessing

The preprocessing pipeline includes:

- Removing duplicate records.
- Excluding the campaign identifier from the model features.
- Correcting invalid values, including negative impressions and clicks exceeding impressions.
- Treating invalid CTR, conversion-rate, bounce-rate and ad-quality values as missing.
- Imputing missing numerical values using median-based imputation.
- Applying logarithmic transformations to skewed variables such as impressions, clicks, advertising spend and conversions.
- Encoding categorical variables using one-hot encoding.
- Scaling numerical model inputs using `StandardScaler`.
- Creating temporal features such as month, day of the week and quarter.

Derived metrics such as cost per click (CPC), cost per acquisition (CPA), and return on advertising spend (ROAS) are also calculated for campaign analysis.

The regression target is `log1p(revenue_usd)`, allowing the notebook to train models on a transformed revenue target and convert predictions back to the original revenue scale for evaluation.

### 3. Revenue Prediction — Regression

The notebook trains and compares three regression algorithms:

| Model | Purpose |
|---|---|
| Ridge Regression | Regularized linear regression that helps control coefficient magnitude and overfitting. |
| Random Forest Regressor | An ensemble of decision trees capable of modeling nonlinear relationships and feature interactions. |
| XGBoost Regressor | Gradient-boosted decision trees for learning complex patterns in campaign data. |

The models use configured hyperparameters, including regularization for Ridge and XGBoost, tree-depth limits, and sampling controls for the ensemble models.

#### Evaluation methodology implemented

- Train/test split for model evaluation.
- Five-fold cross-validation using `KFold`.
- Training and test \(R^2\) scores.
- Cross-validation mean \(R^2\) and standard deviation.
- RMSE (Root Mean Squared Error).
- MAE (Mean Absolute Error).
- \(R^2\) after transforming predictions back to the original revenue scale.
- Train–test performance-gap checks to flag potential overfitting.
- Model-comparison visualizations.

The notebook selects a preferred regression model based on its evaluation results and saves the selected model for reuse.

**Important:** The notebook's reported metrics are experimental results from its current implementation, not independently validated production performance. See the limitations section below before interpreting them as generalizable predictive accuracy.

### 4. Additional Classification Models

The notebook also explores classification tasks to categorize campaign outcomes.

**Campaign success classification**

A binary target is constructed from campaign performance criteria. A Random Forest classifier is trained to predict the resulting success label, with performance assessed using classification reports and a confusion matrix.

**Campaign tier classification**

Campaign tiers are derived from the notebook's defined campaign rules. A Random Forest classifier is used to predict the resulting tier labels, and class-level evaluation metrics are reported.

**Revenue-based success and churn-risk classification**

An additional section constructs labels using revenue percentiles and bounce-rate thresholds. These targets are used to explore whether campaigns can be categorized by relative revenue performance and potential churn risk.

**Audience segment classification**

The notebook also includes an audience-segment prediction experiment using campaign attributes, with audience labels encoded for model training and evaluation.

These classification experiments extend the analysis beyond revenue regression and demonstrate multiple approaches to campaign categorization.

### 5. Model Evaluation and Visual Diagnostics

The notebook generates plots to assess regression performance and compare the trained models, including:

- Model comparison visualizations.
- Actual-versus-predicted revenue plots.
- Actual-versus-predicted plots in log space and original currency units.
- Residuals-versus-predicted plots.
- Residual distribution histograms.
- Training and test performance comparisons.

These visual diagnostics help identify prediction errors, differences between models, and potential overfitting.

### 6. Explainable AI — SHAP

The notebook uses **SHAP (SHapley Additive exPlanations)** to examine which features influence the selected regression model's predictions.

Depending on the selected model, it uses an appropriate explainer, including `LinearExplainer` for Ridge Regression and a tree-based explainer for tree models.

The analysis includes:

- Global feature-importance rankings based on mean absolute SHAP values.
- SHAP bar plots for the most influential features.
- SHAP beeswarm plots to examine feature impact across observations.
- Local waterfall explanations for supported tree-based models.
- Feature coefficient analysis for Ridge Regression.

The goal is to make model behavior more interpretable by identifying which campaign attributes contribute to higher or lower predicted revenue.

### 7. Local Explanations — LIME

The notebook uses **LIME (Local Interpretable Model-agnostic Explanations)** to investigate individual revenue predictions.

It generates local explanations for selected high-revenue and low-revenue observations, showing the features that contribute to the model's prediction around each observation.

These explanations complement SHAP by focusing on individual cases rather than only global feature importance.

### 8. Business Insights and Reporting

The notebook summarizes observed campaign performance and produces business-oriented visualizations.

The analysis compares average revenue across:

- Advertising channels.
- Regions.
- Device types.
- Audience segments.

It identifies categories associated with higher average revenue in the supplied dataset and generates a text-based business summary containing proposed optimization recommendations.

These results are intended to help stakeholders explore potential areas for further campaign investigation, budget experimentation, and performance improvement.

Observed revenue differences are descriptive associations; they do not, by themselves, establish that reallocating advertising spend will causally increase revenue.

## Generated Outputs

The notebook saves plots, reports and model artifacts for further inspection and potential reuse.

**Visualizations**

- `revenue_distribution.png`
- `distributions.png`
- `boxplots.png`
- `correlation_matrix.png`
- `category_performance.png`
- `engineered_features.png`
- `model_comparison_final.png`
- `actual_vs_predicted_final.png`
- `residuals_plot.png`
- `shap_bar_top10.png`
- `shap_beeswarm.png`
- `shap_waterfall_best.png`
- `shap_waterfall_poor.png`
- `lime_best.png`
- `lime_poor.png`
- `business_insights.png`
- `ridge_coefficients.png`

Some explanation plots are generated conditionally depending on the selected model.

**Model artifacts**

- `best_model.pkl` — serialized selected regression model.
- `scaler.pkl` — serialized feature scaler.
- `feature_names.pkl` — saved feature-name metadata.

**Business report**

- `business_summary.txt` — generated summary of observed campaign performance and proposed recommendations.

The notebook also prints model evaluation results, classification reports, feature-importance rankings and a summary of generated outputs.

## Technology Stack

- **Language:** Python
- **Data analysis:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Machine learning:** scikit-learn
- **Regression:** Ridge Regression, Random Forest, XGBoost
- **Classification:** Random Forest and Ridge-based classification experiments
- **Explainable AI:** SHAP, LIME
- **Model persistence:** Joblib
- **Execution environment:** Google Colab / Jupyter Notebook

## Running the Notebook

1. Open the notebook in Google Colab or Jupyter.
2. Install the required libraries. The notebook includes installation for SHAP, LIME and LightGBM; ensure the remaining imported dependencies, including scikit-learn, XGBoost, Pandas, NumPy, Matplotlib and Seaborn, are available.
3. Place `digital_media_dataset.csv` in the runtime's working directory or update the dataset path.
4. Execute the cells in order, ensuring each preprocessing, training and evaluation stage completes successfully.
5. Review the generated plots, model metrics, explanations and business summary.
6. Download the desired artifacts from the runtime output directory.

The notebook is a standalone training and analysis workflow. It does not need to be integrated into the CampaignIQ FastAPI backend or React frontend to run its analysis.

## Project Context

This notebook supports the machine-learning and analytical component of CampaignIQ, a digital media campaign performance optimization project. The wider project combines predictive analytics, explainability, backend inference APIs and an interactive dashboard to help users investigate campaign performance.

The notebook is maintained separately so that the model-training workflow remains accessible, inspectable and reproducible without requiring the application stack to run.
