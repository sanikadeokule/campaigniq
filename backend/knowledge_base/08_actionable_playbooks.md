# Actionable Playbooks — If/Then Decision Guides

This document is the chatbot's "what should I do?" reference. Every playbook is structured: **Situation → Diagnosis → Action → Expected Outcome**. When a user describes a problem, retrieve the matching playbook and adapt the language.

---

## Playbook 1: Predicted Revenue Below $5,000

**Situation:** Model predicts campaign revenue under $5K — bottom of the distribution.

**Diagnosis Checklist:**
- Is the channel Display or Affiliate? → Likely root cause.
- Is the audience Boomers? → Lowest-revenue segment.
- Is the region North or West? → Bottom-tier regions.
- Is conversion_rate_pct < 1%? → Funnel is broken.

**Action:**
1. **Don't launch as-is.** Predicted revenue this low rarely returns positive ROI.
2. **Switch to Search or Video** if the product/objective allows.
3. **Re-target audience** — try Gen X or Gen Z for higher revenue.
4. **Re-run prediction** with the modified plan before committing budget.

**Expected Outcome:** A 20–40% lift in predicted revenue from a single channel/audience swap is typical.

---

## Playbook 2: Predicted ROAS Below 1.5x

**Situation:** Predicted revenue ÷ planned spend < 1.5.

**Diagnosis:** The campaign is likely losing money after COGS and platform fees.

**Action:**
1. **Pause the launch** unless there's a strategic awareness goal.
2. **Cut planned spend by 50%** and re-predict — sometimes lower spend has better unit economics.
3. **Investigate the funnel:** is conversion_rate_pct realistic? Is bounce_rate_pct < 60%?
4. **Compare to similar Star-tier campaigns** in the dashboard to find the gap.

**Expected Outcome:** Either the campaign breaks even after rework, or it's permanently shelved — both are wins versus quietly burning budget.

---

## Playbook 3: High Spend, Low Conversions

**Situation:** spend_usd > $10K but conversions < 50.

**Diagnosis (in priority order):**
1. **Landing page mismatch** — ad creative promises X, page delivers Y. Check bounce rate; if > 70% on a checkout/lead page, this is it.
2. **Audience targeting is too broad** — high impressions, low intent. Check CTR; if < 0.5%, targeting is off.
3. **Wrong channel for the objective** — Display ads for a Sales objective rarely convert.
4. **Tracking is broken** — UTM params, conversion pixel, or postback URL is misconfigured. *Always rule this out first.*

**Action:**
1. **Verify conversion tracking is firing.** Single highest-leverage 30-min check.
2. **Audit landing page** against the ad. Run a 5-second test: would a stranger know what to do?
3. **Tighten audience** — exclude lookalike segments that aren't converting.
4. **If CTR > 2% but conversion rate < 1%:** the problem is downstream of the click (page or product). Don't blame the ad.

**Expected Outcome:** 2–5x improvement in conversion rate is realistic from landing page + tracking fixes alone.

---

## Playbook 4: High CTR, Low Conversion Rate

**Situation:** CTR > 3% (great) but conversion_rate_pct < 1% (poor).

**Diagnosis:** The ad is winning attention, but the post-click experience is failing. This is almost always a **landing page** or **offer** problem.

**Action:**
1. **Check session duration.** If < 30 sec, users land and bounce.
2. **Check bounce rate.** If > 70% on a landing page, the page isn't matching ad intent.
3. **Audit the landing page hero:** does the headline match the ad? Is the CTA above the fold?
4. **Mobile vs desktop split:** is the page broken on mobile?
5. **Page speed:** anything > 3s load time loses 30%+ of mobile users.

**Action plan:** Run a 1-week landing page A/B test — different headline OR different CTA OR different hero image. Don't change three things at once.

---

## Playbook 5: Low CTR, High Conversion Rate

**Situation:** CTR < 0.5% but the few people who click convert at > 5%.

**Diagnosis:** The audience and offer are well-matched — but the creative isn't getting noticed. The campaign is **under-distributing a good product**.

**Action:**
1. **Refresh creative.** New imagery, sharper headline, stronger value prop.
2. **Test more attention-grabbing formats:** video over static, carousel over single image.
3. **Increase bid / budget** modestly — you have a winning conversion engine, you just need more clicks.
4. **Lookalike audience expansion:** the people converting are valuable; build a lookalike from them.

**Expected Outcome:** A 2x CTR with the same conversion rate doubles revenue. This is one of the highest-leverage fixes.

---

## Playbook 6: Display Campaign Underperforming

**Situation:** A Display campaign is in Question Mark or Dog tier.

**Diagnosis:** Display has the worst average revenue in the dataset (~$6.2K vs Search $32.8K). The Ridge model has a **negative coefficient** for Display. It's an uphill battle by default.

**Action:**
1. **First question — was Display the right call?** Display works for *retargeting* warm audiences. It rarely works for cold prospecting.
2. If the campaign is *prospecting* on Display: **kill it and reallocate to Search.** Expected revenue lift: 4–5x per dollar.
3. If the campaign is *retargeting:* tighten the audience to recent visitors (< 14 days), and check frequency caps (max 3–5 impressions per user per week to avoid fatigue).
4. **Don't sink more budget trying to "make Display work."** The dataset shows it rarely does.

---

## Playbook 7: Question Mark Campaign — 30-Day Decision Plan

**Situation:** Campaign tagged Question Mark — mixed signals, unclear if scaling will help.

**Action timeline:**

| Day | Action |
|---|---|
| 1 | Diagnose: which metric is weakest (CTR, conversion rate, bounce rate)? |
| 2–3 | Set up a single A/B test on the weakest variable |
| 4–10 | Run the test with a meaningful sample size |
| 11–14 | Analyze results. Did the variant move the needle? |
| 15–25 | If yes → scale spend 25% and monitor. If no → run one more test on the next-weakest variable. |
| 26–30 | **Decision day:** Has the campaign moved to Core? If not → kill it and reallocate. |

**Anti-pattern:** Letting Question Marks drift for 90+ days while quietly bleeding budget. Always set the deadline.

---

## Playbook 8: Star Campaign — How to Scale Safely

**Situation:** Campaign is a Star ⭐ — top revenue, healthy ROAS.

**Action — staged scaling:**

| Stage | Budget Increase | Watch For | Decision |
|---|---|---|---|
| 1 | +20% | ROAS holds within 10% of baseline | Continue |
| 2 | +20% | Conversion rate stable | Continue |
| 3 | +25% | CTR not collapsing | Continue |
| 4 | Re-evaluate | If ROAS drops >15% | Hold spend, optimize |

**Why staged?** Doubling budget overnight often crashes ROAS — you exhaust the high-intent audience and start paying for low-intent traffic. Staged 20–25% increases let the auction adjust.

**Also do:**
- **Clone the recipe** to adjacent audiences (e.g., Gen X working → test on Boomers).
- **Lock the creative** — don't refresh prematurely if it's still performing.
- **Document why it's a Star** in your team's playbook.

---

## Playbook 9: Conversion Rate Below 1%

**Situation:** Conversion rate is the #1 SHAP driver. Below 1% is a red flag regardless of other metrics.

**Action — diagnostic ladder, top to bottom:**

1. **Tracking check:** Is the conversion event firing? (90% of "broken" funnels are this.)
2. **Page speed:** > 3 sec load time on mobile? Fix first.
3. **CTA clarity:** Can a 5-year-old find the next step?
4. **Friction in the form/checkout:** Reduce fields. Every field cuts conversion ~5%.
5. **Trust signals:** Add reviews, security badges, return policy near the CTA.
6. **Mobile UX:** Test on a real phone, not Chrome DevTools.
7. **Offer strength:** Is the value prop competitive vs alternatives?

A 1% → 2% conversion rate doubles revenue at the same spend. This is the single highest-ROI category of optimization.

---

## Playbook 10: Bounce Rate Above 70%

**Situation:** bounce_rate_pct > 70% — landing page is rejecting visitors.

**Diagnosis:** Bounce > 70% on a conversion-focused page = misalignment between ad and page.

**Action:**
1. **Visual ad-to-page audit:** load the ad and the landing page side by side. Do the messages, imagery, and offer match?
2. **Above-the-fold check:** can a visitor see the value prop and CTA without scrolling?
3. **Page load:** target < 2 sec on mobile (use PageSpeed Insights).
4. **Single CTA:** too many buttons confuses. One primary action per page.
5. **Mobile responsiveness:** check on real devices.

**Expected Outcome:** Reducing bounce from 75% to 55% can double effective traffic at no additional spend.

---

## Playbook 11: Budget Reallocation Framework

**Situation:** User asks "where should I move my budget?"

**Default reallocation rule from the dataset:**

> Move 20–30% of Display + Affiliate spend → Search.

**Detailed framework:**

1. **Identify Dogs** (bottom 15.4% of campaigns by tier). Pause them.
2. **Sum the freed budget.**
3. **Allocate freed budget by ROI tier:**
   - 60% → top 3 Stars (proven scalers)
   - 25% → top 3 Core campaigns being promoted
   - 15% → 1–2 strategic Question Marks worth testing
4. **Don't reallocate to new untested campaigns.** Cold starts drag returns.

**Channel mix target (rough):** 35% Search / 20% Video / 15% Email / 15% Social / 10% Affiliate / 5% Display.

---

## Playbook 12: New Campaign Pre-Launch Checklist

Before any campaign launches, run through this:

| ✓ | Item | Why |
|---|---|---|
| ☐ | Predicted revenue ≥ $5K | Below this rarely returns ROI |
| ☐ | Predicted ROAS ≥ 1.5x | Below this loses money |
| ☐ | Channel matches objective (Search→Sales, Video→Awareness) | Mismatched channels are #2 cause of Dogs |
| ☐ | Conversion tracking tested end-to-end | Broken tracking = invisible failure |
| ☐ | Landing page audited (mobile + desktop) | Ad-to-page alignment |
| ☐ | Audience size > 50K but < 5M | Too small = cold start; too big = generic |
| ☐ | Creative variants ready (≥ 2 for A/B) | Single creative = no learning |
| ☐ | Frequency cap set | Especially Display/Video — avoids fatigue |
| ☐ | Daily budget ≤ 1/30 of monthly | Pacing protection |
| ☐ | Stop-loss rule defined | E.g., "pause if 7-day ROAS < 1.0" |

---

## Summary for the Chatbot

When a user describes a problem:
1. **Match it to a playbook above** based on the symptoms they describe.
2. **Lead with the diagnosis section** — don't jump to the action.
3. **Walk through the action steps in order.** Most are sequenced for a reason.
4. **Quantify expected outcomes** when possible (e.g., "2–5x improvement"), even as ranges.
5. **End with a single concrete next step** the user can take in the next 24 hours.
