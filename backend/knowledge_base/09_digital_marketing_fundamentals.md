# Digital Marketing Fundamentals

This document is the chatbot's general knowledge base for digital marketing concepts that aren't dataset-specific. When users ask conceptual questions ("what's a marketing funnel?", "how does retargeting work?", "what is attribution?"), retrieve from here.

---

## The Marketing Funnel

The funnel is the standard mental model for how a stranger becomes a customer. Each stage filters down to a smaller, more committed group.

| Stage | Goal | Key Metrics | Typical Channels |
|---|---|---|---|
| **Awareness** | Get noticed | Impressions, reach, video views | Display, Video (CTV/YouTube), Social |
| **Consideration** | Get them interested | CTR, time on site, page views | Social, Search, Content |
| **Conversion** | Get them to act | Conversion rate, CPA | Search, Email, Retargeting |
| **Retention** | Keep them coming back | Repeat purchase rate, LTV | Email, Push, SMS |
| **Advocacy** | Get them to refer | Referral rate, review volume | Email, Social |

**Key principle:** Don't measure top-of-funnel channels with bottom-of-funnel metrics. A Video campaign won't have a 3% conversion rate — it builds the audience that Search later converts.

---

## Campaign Objectives — Pick One

The four objectives in this dataset map to funnel stages:

| Objective | Funnel Stage | What It Optimizes For | Right Channels |
|---|---|---|---|
| **Awareness** | Top | Impressions, reach | Display, Video, Social |
| **Traffic** | Top–Mid | Clicks, site visits | Search, Social |
| **Leads** | Mid–Bottom | Form fills, signups | Search, Email, Social |
| **Sales** | Bottom | Purchases, revenue | Search, Email, Retargeting |

**Anti-pattern:** Running a Display campaign with a Sales objective and judging it by conversion rate. Display drives awareness; conversions show up later via Search/Email.

---

## Attribution — Who Gets the Credit?

When a customer touches 5 ads before buying, which one "caused" the sale? Attribution models answer this differently:

| Model | How It Credits | Strengths | Weaknesses |
|---|---|---|---|
| **Last-Click** | 100% to final touchpoint | Simple, default in most platforms | Overcredits Search/Email; ignores upper funnel |
| **First-Click** | 100% to first touchpoint | Highlights discovery channels | Ignores closing channels |
| **Linear** | Equal weight across all touches | Fair to all channels | Treats brand impression like a conversion-driving click |
| **Time-Decay** | More weight to recent touches | Reflects recency bias | Still over-credits the close |
| **Position-Based (40-20-40)** | 40% first, 40% last, 20% middle | Balances discovery and conversion | Arbitrary weights |
| **Data-Driven** | Algorithmic (typically Markov chains or Shapley) | Most accurate | Requires lots of data |

**Practical rule:** If your team is using last-click attribution, your Display and Video budgets are probably under-funded relative to their true contribution.

---

## Targeting Approaches

### 1. Demographic Targeting
Age, gender, income, region. The dataset's `audience_segment` is a demographic.
- **Strengths:** Easy, broad reach.
- **Weaknesses:** Misses intent. A 25-year-old man looking to buy diapers won't be hit by "young men" targeting.

### 2. Interest / Behavioral Targeting
Based on platform data (pages liked, content consumed, sites visited).
- **Strengths:** Higher intent signal.
- **Weaknesses:** Privacy regulations (iOS 14+, GDPR) have eroded this significantly.

### 3. Intent Targeting (Search Keywords)
Targeting based on what someone is actively searching.
- **Strengths:** **Highest intent signal in digital advertising.** This is why Search wins in the dataset.
- **Weaknesses:** Limited to people already in-market.

### 4. Lookalike / Similar Audiences
Find new users who resemble existing customers.
- **Strengths:** Scales high-converting audiences.
- **Weaknesses:** Quality depends on the seed audience size and quality.

### 5. Retargeting
Show ads to people who already visited your site / engaged with your brand.
- **Strengths:** Highest conversion rates of any tactic. Warm audiences.
- **Weaknesses:** Limited audience size; frequency fatigue if uncapped.

### 6. Contextual Targeting
Match ads to the content of the page (not the user).
- **Strengths:** Privacy-safe, no cookies needed.
- **Weaknesses:** Lower precision.

---

## Bidding Strategies

When you bid in an ad auction, you can optimize toward different goals:

| Strategy | Optimizes For | When to Use |
|---|---|---|
| **Manual CPC** | You set max click price | Full control, small budgets |
| **Maximize Clicks** | Most clicks for budget | Awareness phase |
| **Target CPA** | Specified cost per acquisition | When CPA is the KPI |
| **Target ROAS** | Specified return on ad spend | E-commerce with revenue tracking |
| **Maximize Conversions** | Most conversions for budget | Lead gen, no strict CPA cap |
| **Maximize Conversion Value** | Most revenue for budget | E-commerce, varying basket sizes |

**Practical advice:** Most platforms recommend automated bidding (Target ROAS, Maximize Conversions) once you have ≥ 30 conversions per month per campaign. Below that, manual bidding gives more control.

---

## Creative Best Practices

Creative quality is the single biggest variable you can control with no extra spend.

### Universal Principles
1. **Hook in 3 seconds.** Mobile users scroll fast. The first 3 sec of video / first headline of static must stop them.
2. **One message per ad.** Multiple value props confuse. One clear hook wins.
3. **Show, don't tell.** Video > static. Real product footage > stock photos.
4. **Match the platform.** A polished TV-style ad bombs on TikTok; a TikTok-native ad looks amateur on YouTube CTV.
5. **Refresh on a schedule.** Creative fatigue is real — performance drops 30–50% by week 4 typically.

### Channel-Specific Notes
- **Search:** Headlines do most of the work. Test 3+ variants.
- **Display:** Banner blindness is the enemy. Bold contrast + a single CTA.
- **Social (Meta):** Native-looking, mobile-first vertical video.
- **TikTok:** Casual, creator-style, trending audio.
- **Video (YouTube):** First 5 sec must hook; show the brand in 3 sec.
- **Email:** Subject line determines open rate; preview text is the second hook.

---

## A/B Testing 101

### The Rules
1. **Test one variable at a time.** Otherwise you can't attribute the lift.
2. **Set a sample size in advance.** Stopping early when results "look good" produces false positives.
3. **Statistical significance: 95%+ confidence.** Below 90% = noise.
4. **Run for at least one full week.** Day-of-week effects are real.
5. **Validate with a holdout group.** Especially on platform-optimized campaigns.

### What to Test
**High-leverage:** Headline, CTA copy, hero image, audience targeting.
**Medium-leverage:** Body copy, secondary CTA, button color, form length.
**Low-leverage:** Font, padding, exact word choice on minor labels.

### Sample Size Heuristic
For binary metrics (conversion rate), you typically need **~1,000 conversions per variant** to detect a 10% relative lift at 95% confidence. Less is fine if the lift is bigger.

---

## Frequency Capping

How many times should one person see your ad?

- **Sweet spot:** 3–5 impressions per user per week.
- **Below 3:** Brand recall doesn't form.
- **Above 7–10:** Diminishing returns set in fast; above 15 you're paying for irritation.

**Especially important on:** Display, Video, Retargeting (where the same user can be hit dozens of times if uncapped).

---

## Email Marketing Specifics

Email has the highest ROI of any channel — typically $36 returned per $1 spent (DMA), but only when done right.

### List Hygiene
- Remove unengaged subscribers (no opens in 90+ days). Their inactivity hurts deliverability.
- Use double opt-in to keep the list clean.
- Honor unsubscribes immediately.

### Deliverability Essentials
- **SPF, DKIM, DMARC** records configured. Without them, you go to spam.
- **Sending domain reputation** — warm up new domains slowly.
- **Avoid spam triggers:** ALL CAPS, "FREE!!!", excessive emojis in subject lines.

### Send Timing
- **B2B:** Tuesday–Thursday, 9–11am local time of recipient.
- **B2C:** Variable. Test against your audience.
- **Frequency:** Twice a week is the sweet spot for most lists. Daily is too much for most.

---

## SEO vs SEM (Important Distinction)

- **SEO (Search Engine Optimization):** Organic search traffic. Free per click, slow to build, compounds over time.
- **SEM (Search Engine Marketing):** Paid search ads. Instant traffic, pay per click, stops when budget stops.

**The dataset is SEM** (paid search). SEO is not in scope here.

**Strategic complementarity:** SEO captures branded and informational queries. SEM captures competitive commercial queries and protects branded terms. Most mature programs run both.

---

## Common KPI Hierarchies

Different teams track different things. Common hierarchies:

### E-commerce
ROAS → Revenue → Conversion Rate → AOV → CAC payback period

### B2B Lead Gen
SQLs (sales-qualified leads) → MQLs (marketing-qualified leads) → CPL (cost per lead) → Lead-to-customer conversion

### SaaS
Trial signups → Activated trials → Paid conversion → MRR / CAC ratio

### Brand / Awareness
Reach → Frequency → Brand lift (survey) → Branded search volume

**Why this matters for the chatbot:** When a user says "we care about leads," interpret that as B2B lead gen and frame answers around CPL and conversion-to-customer, not ROAS.

---

## Summary for the Chatbot

When asked a conceptual question:
1. **Define the term plainly first** — assume the user might be new to it.
2. **Give one or two concrete examples** from the dataset's context (channels, regions, etc.) when possible.
3. **Connect it back to actionable advice** — don't just define and stop.
4. **Avoid jargon piling.** If you use a term, define it inline.
