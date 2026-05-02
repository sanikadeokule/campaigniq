# Optimization Strategies — How to Improve Campaign Performance

This document is the chatbot's playbook for *improving* a metric. Where Playbooks (doc 08) handle "this is broken, fix it," this document handles "this is fine, make it better."

---

## Master Optimization Principle

**Conversion rate is the highest-leverage metric to optimize.** A 1% → 2% lift on conversion rate = 100% revenue lift at the same spend. Nothing else compounds like this.

Order of optimization priority (top = highest leverage):
1. Conversion rate (page + offer + funnel)
2. CTR (creative + audience match)
3. Channel mix (move budget from low-revenue to high-revenue channels)
4. Audience targeting (lookalikes from converters)
5. Bidding strategy (only after 1–4 are dialed in)
6. Creative refresh cadence
7. Bid floors / frequency caps

---

## How to Improve Conversion Rate

### Tier 1: The Tracking and Mechanics Layer (do first)

1. **Verify conversion tracking end-to-end.** Misfiring tracking is the #1 cause of "low conversion rate." Test every event in a private session.
2. **Page speed audit.** Anything over 3 sec on mobile loses ~30% of users. Use PageSpeed Insights.
3. **Mobile usability.** 60–80% of paid traffic is mobile. Test on actual devices.

### Tier 2: The Funnel Layer

1. **Reduce form fields.** Each field cuts conversion ~5–10%. Ask only what you need.
2. **Single primary CTA per page.** Multiple CTAs = decision paralysis.
3. **CTA above the fold.** Don't make users scroll to find the action.
4. **Match landing page headline to ad headline.** Word-for-word ideal. 80% match minimum.

### Tier 3: The Trust Layer

1. **Social proof:** reviews, testimonials, customer logos near the CTA.
2. **Security badges:** SSL indicator, payment trust marks at checkout.
3. **Risk reversal:** money-back guarantee, free returns, free trial.
4. **Urgency / scarcity (used honestly):** "47 in stock," "sale ends Friday."

### Tier 4: The Offer Layer

1. **Value prop A/B test.** Try a different headline angle (savings vs convenience vs status).
2. **Pricing presentation:** anchor higher to make your price look like a deal.
3. **Bundle vs single product test.** Often bundles convert better at higher AOV.
4. **Free shipping threshold.** $50+ free shipping is a known conversion lever.

---

## How to Improve CTR

### Creative-Side Levers

1. **Test 5+ headline variants.** Headlines drive 60%+ of CTR variance.
2. **Lead with the strongest benefit.** Not feature lists.
3. **Use numbers in headlines.** "Save 30%" beats "Save big."
4. **Faces in ads.** Human faces draw the eye on social.
5. **Carousel > single image.** More content surface = more click triggers.
6. **Native creative.** Match the platform's organic aesthetic, especially TikTok and Instagram.

### Targeting-Side Levers

1. **Tighten the audience.** Broad audiences → low CTR. Narrower = more relevant ads = higher CTR.
2. **Layer in interest filters** on Social.
3. **Negative keywords** on Search to exclude irrelevant queries.
4. **Lookalikes from converters** (not site visitors). Quality of seed matters.

### Format-Side Levers

1. **Video over static** on Social and CTV (typically 1.5–2x CTR).
2. **Responsive Search Ads** on Google (let the algorithm pick best combos).
3. **Try different ad placements** (e.g., Instagram Reels vs Feed).

---

## How to Improve ROAS

ROAS = Revenue / Spend. So you can either:
- **Increase revenue per dollar** (better targeting, better conversion rate, higher AOV)
- **Decrease spend per result** (lower CPC via Quality Score, eliminate waste)

### Increase Revenue Side

1. **Optimize for conversion value, not just conversions.** A $200 customer ≠ a $20 customer. Use Maximize Conversion Value bidding when the platform supports it.
2. **AOV (Average Order Value) lifts:** upsells at checkout, bundles, free shipping thresholds.
3. **Retarget cart abandoners.** Highest-converting audience by far. 10–20x ROAS is common.
4. **Email follow-up flows.** A welcome series + abandoned cart series can add 20–30% to top line.

### Decrease Spend Side

1. **Quality Score improvements** (Google Ads): better ad relevance + landing page experience = lower CPCs.
2. **Negative keyword pruning:** every irrelevant search you exclude saves $$.
3. **Day-parting:** if conversions cluster around specific hours, schedule budget there.
4. **Geo-bidding:** bid up in high-revenue regions (East/Central in this dataset), bid down in low-revenue ones.
5. **Audience exclusions:** exclude non-converting audiences explicitly.

---

## How to Improve Bounce Rate

High bounce = the page failed the visitor. Every fix is on the page side, not the ad side.

1. **Page load < 2 sec on mobile.** Single biggest factor.
2. **Hero section answers "what is this and why should I care" in 5 sec.**
3. **No popups in the first 30 sec.** They feel hostile to new visitors.
4. **No unexpected redirects.** Users sniff bait-and-switch instantly.
5. **No autoplay video with sound.** Universal hostility.
6. **Mobile-first design** — fingers, not mice.
7. **Match landing page voice/visual to ad voice/visual.**

---

## How to Improve Quality Score (Google Ads)

Quality Score is Google's 1–10 rating of your ad relevance. Higher score = lower CPCs and better placements. Three components:

| Component | What It Measures | How to Improve |
|---|---|---|
| **Expected CTR** | Predicted click-through rate vs competitors | Sharper headlines, tighter keyword-to-ad relevance |
| **Ad Relevance** | How closely your ad text matches the keyword | One ad group per intent; keyword in headline |
| **Landing Page Experience** | Page relevance + load speed | Match page content to ad promise; fast load |

**Practical impact:** A campaign with Quality Score 8/10 pays roughly half as much per click as one with 4/10 for the same auction position. Quality Score is one of the most under-invested optimizations in most accounts.

---

## How to Reallocate Budget Strategically

The framework, in order:

1. **Identify the bottom 15–20% of campaigns by ROAS.** Pause or cut.
2. **Sum the freed budget.**
3. **Top up the proven Stars by 20–25%** (don't double overnight — you'll crash unit economics).
4. **Fund 1–2 strategic Question Mark experiments** with the remainder.
5. **Re-run the analysis monthly.**

The dataset's headline finding: **Move 20–30% of Display + Affiliate spend to Search.** This is the single highest-EV reallocation in the data.

---

## Optimization Calendar (How Often to Do What)

| Frequency | What |
|---|---|
| **Daily** | Pacing check (are we under/over budget?), anomaly check (any campaign crashed?) |
| **Weekly** | Performance review by tier, creative refresh decisions, A/B test reads |
| **Bi-weekly** | Audience refresh, lookalike rebuilds, exclusion list updates |
| **Monthly** | Full account audit, channel mix review, budget reallocation, strategic experiments |
| **Quarterly** | Channel strategy review, attribution model review, MMM (if applicable) |
| **Annually** | Full-account strategic review, vendor renegotiation, tooling audit |

**Anti-pattern:** Optimizing daily on metrics that need weekly cycles to stabilize. Daily fiddling causes more harm than good.

---

## What NOT to Optimize

Some things look optimizable but rarely move the needle:

1. **Button color.** Famous case studies are mostly cherry-picked. Below 5% lift typically.
2. **Tiny copy tweaks** (e.g., "Buy Now" vs "Purchase"). Marginal.
3. **Font size** beyond legibility. Marginal.
4. **Audience age tweaks** of 1–2 years. Noise.
5. **Bid adjustments** of <10%. Below platform's smoothing threshold.

Focus optimization energy on big levers — creative, audience, channel mix, conversion mechanics — not micro-tweaks.

---

## Diminishing Returns: A Realistic Mental Model

Each round of optimization is harder than the last:

- **Round 1:** Easy 30–50% lifts (fixing basics — tracking, page speed, obvious bugs).
- **Round 2:** 15–25% lifts (creative tests, audience refinement).
- **Round 3:** 5–15% lifts (advanced bidding, attribution-driven reallocation).
- **Round 4+:** 1–5% lifts (creative cadence, fine-tuning, exclusions).

Calibrate user expectations: if a user has been optimizing for 18 months and asks "how do I get another 50% lift?", the honest answer is "you probably won't from optimization alone — you need a new audience, new product, or new channel."

---

## Summary for the Chatbot

When asked "how do I improve X?":
1. **Lead with the highest-leverage lever** (usually conversion rate or creative).
2. **Tier the suggestions** — easy wins first, then deeper changes.
3. **Quantify expected lift** as ranges, not point estimates.
4. **Flag when the user might be in diminishing returns territory.** "If you've already done these, the next round is harder."
5. **Always end with one specific action** they can take this week.
