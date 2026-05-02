# Region, Audience, and Device Performance

This document covers the geographic, demographic, and device dimensions of the dataset. Use it for questions like "where do my campaigns perform best?", "which audience converts?", and "should I prioritize mobile?"

## Region Performance

### Average Revenue by Region

| Rank | Region | Avg Revenue (USD) |
|---|---|---|
| 1 | **East** | ~$23,300 (best) |
| 2 | Central | ~$23,000 |
| 3 | South | ~$20,200 |
| 4 | North | ~$15,200 |
| 5 | West | ~$15,100 |

### Insights

- **East and Central** are essentially tied at the top — these are the highest-value markets for the campaigns in this dataset. East has a slight edge.
- **North and West** lag the top tier by ~35%. This could reflect lower purchasing power, stronger competition, or audience-product fit issues — the dataset doesn't tell us which.
- **South** sits in the middle; volume + revenue per campaign is solid but not best-in-class.

### Action Items

- **Reallocate from West/North toward East/Central** if the product is geographically agnostic.
- **Test region-specific creative** before expanding into West/North — generic creative may be the issue rather than the region itself.
- **Localize landing pages** by region if AOV varies — currency formatting, regional shipping promises, and local brand mentions help.

---

## Audience Segment Performance

### Average Revenue by Audience

| Rank | Segment | Avg Revenue (USD) |
|---|---|---|
| 1 | **Gen X** | ~$23,000 (tied for best) |
| 1 | **Gen Z** | ~$22,800 (tied for best) |
| 3 | Millennials | ~$16,800 |
| 4 | Boomers | ~$14,800 |

### Surprising Finding: Gen X and Gen Z Tied at the Top

This is the most counter-intuitive insight in the dataset. Conventional wisdom says Millennials are the prime digital ad audience — but in this data, **Gen X (older, higher disposable income, brand-loyal) and Gen Z (digital-native, mobile-first) outperform Millennials by 35%+**.

Possible explanations:
- **Gen X** has higher disposable income and responds well to search-driven, intent-based advertising.
- **Gen Z** drives strong impulse / discovery purchases on Video and Social, especially mobile.
- **Millennials** are saturated with ads and have developed strong ad-skipping habits (ad-blockers, premium subscriptions).
- **Boomers** convert at decent rates but with smaller basket sizes.

### Model-Side Detail

The model has small but **positive Ridge coefficients** for `audience_segment_Gen Z` (+0.049) and `audience_segment_Millennials` (+0.068) versus the Boomers reference. This means, controlling for everything else, those two segments slightly *increase* predicted log-revenue.

Note: There is also a separate **audience-segment classifier** that tries to predict audience from behavior. **It performs at ~24% accuracy — barely above random (25%) for 4 classes.** This means behavior alone, without targeting metadata, is a poor predictor of audience segment in this dataset. **The classifier should NOT be used for production targeting decisions.** See `07_success_churn_classification.md`.

### Action Items

- **Don't auto-default to Millennials** as the prime target — the data says otherwise here.
- **Match channel to audience:**
  - Gen X → Search, Email
  - Gen Z → Video, Social (especially short-form)
  - Millennials → Multi-touch (Search + Social + Email)
  - Boomers → Search + Email; minimal Social

---

## Device Performance

### Average Revenue by Device

| Rank | Device | Avg Revenue (USD) |
|---|---|---|
| 1 | **Tablet** | ~$21,500 (best) |
| 2 | Mobile | ~$20,200 |
| 3 | Desktop | ~$18,800 |
| 4 | CTV | ~$17,400 |

### Insight: Tablet Outperforms Mobile and Desktop

This is also unexpected. Industry data usually has Desktop or Mobile leading, with Tablet as a small slice. In this dataset, Tablet wins — possibly because:
- Tablet users are often in "consideration mode" (couch browsing, decision-making sessions).
- Larger screen than mobile = better landing page experience.
- Tablet sessions tend to be longer than mobile (less context-switching).

The gap is modest (~14% from best to worst) — device matters less than channel or audience.

### Action Items

- **Don't ignore Tablet inventory.** Many media buyers lump tablet into mobile and miss out.
- **Optimize creative + landing pages for tablet aspect ratios.** Often broken because tablet gets neither mobile-first nor desktop-first design.
- **CTV at the bottom is expected** — it drives awareness, with conversions usually attributed downstream to Search/Email.

---

## Cross-Dimension Patterns

### Highest-Performing Combination (Inferred)

Search + East + Gen X + Tablet — combines the top performer in each dimension. While the dataset doesn't break out every cell, campaigns in this intersection consistently appear in the Star tier.

### Lowest-Performing Combination

Display + West + Boomers + CTV — bottom of every dimension. Campaigns matching this profile cluster in the Dog tier and should be paused or radically reworked.

### What the Model Says

In the Ridge feature coefficients, after the dominant log-numeric features, the next tier of impact comes from:
- `audience_segment_Millennials` (+, modest boost)
- `channel_Display` (–, drag)
- `audience_segment_Gen Z` (+, modest boost)

Region and device coefficients are smaller in magnitude — they shift predictions but don't dominate.

---

## Summary for the Chatbot

When asked about geography or audience:
1. Lead with the rank from this dataset, with the specific number.
2. Note any counter-intuitive findings (Gen X tied with Gen Z; Tablet > Desktop).
3. Give an action item, not just a stat.
4. Caveat that the dataset is observational — these are correlations, not guarantees of causation.
