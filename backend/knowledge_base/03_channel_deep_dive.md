# Channel Performance Deep Dive

This document covers each of the six channels CampaignIQ tracks, with dataset-specific revenue numbers and channel-specific recommendations. When the chatbot is asked "which channel performs best?" or "should I run Display ads?" — retrieve from here.

## Channel Ranking by Average Revenue (from 2,540 campaigns)

| Rank | Channel | Avg Revenue (USD) | Notes |
|---|---|---|---|
| 1 | **Search** | ~$32,800 | Top performer — high purchase intent |
| 2 | Video | ~$26,500 | Strong, especially CTV / YouTube |
| 3 | Email | ~$26,400 | Best ROI vs spend; existing audience |
| 4 | Social | ~$13,700 | Mid-tier; varies wildly by creative |
| 5 | Affiliate | ~$11,800 | Below average; quality varies |
| 6 | **Display** | ~$6,200 | Worst performer — banner blindness, low intent |

**Headline insight:** Search generates **5.3x** the revenue of Display per campaign on average. The single highest-leverage move in this dataset is moving budget from Display/Affiliate to Search.

## Channel-by-Channel Profiles

### 🔍 Search

- **Average revenue:** ~$32,800 (best)
- **Why it wins:** People searching for specific keywords have already declared intent. The conversion funnel is short.
- **Best for:** Sales, Leads objectives. High-intent transactional queries.
- **Watch outs:** CPCs in competitive verticals can be brutal ($5–$50 per click). Quality Score directly impacts cost.
- **Action item:** First place to reallocate budget from underperforming channels. Aim to grow Search share to 35–45% of spend if not already.

### 📺 Video

- **Average revenue:** ~$26,500 (#2)
- **Why it works:** Video drives both awareness and consideration. Connected TV (CTV) inventory has been growing fast.
- **Best for:** Awareness + mid-funnel nurture. Brand storytelling.
- **Watch outs:** CPMs are high. Attribution is harder — many video-driven conversions happen later via Search.
- **Action item:** Use video to build the audience that Search and Email can later harvest.

### 📧 Email

- **Average revenue:** ~$26,400 (#3, basically tied with Video)
- **Why it works:** It costs almost nothing per send and targets people who already opted in. Highest ROI per dollar in most setups.
- **Best for:** Retention, repeat purchase, lifecycle marketing.
- **Watch outs:** List quality decays. Deliverability rules (DMARC/SPF/DKIM) are now strict.
- **Action item:** Treat Email as the highest-margin acquisition tool *if* you already have list growth coming from elsewhere.

### 👥 Social

- **Average revenue:** ~$13,700 (mid-tier)
- **Why it's mediocre:** Performance varies wildly by platform, creative, and audience freshness. The dataset doesn't separate Meta vs TikTok vs LinkedIn — averages mask the spread.
- **Best for:** Awareness, mid-funnel. Lookalike + interest targeting.
- **Watch outs:** Creative fatigue is real — refresh ads every 2–4 weeks. iOS 14+ attribution loss hurts Meta especially.
- **Action item:** Don't kill Social, but audit it — likely 70/30 rule applies (30% of campaigns generate 70% of revenue).

### 🤝 Affiliate

- **Average revenue:** ~$11,800 (#5)
- **Why it underperforms here:** Affiliate quality is highly variable. Some networks are full of low-intent coupon traffic.
- **Best for:** Performance-based, last-click conversions if affiliates are vetted.
- **Watch outs:** Last-click attribution often inflates affiliate's apparent value (they harvest demand created by other channels).
- **Action item:** Audit individual affiliates — often a small % drive nearly all the value. Cut the rest.

### 🖼️ Display

- **Average revenue:** ~$6,200 (worst, by a wide margin)
- **Why it loses:** Banner blindness, low click-through, audiences that don't want to be interrupted. Often used for "branding" without a clear conversion path.
- **The model agrees:** `channel_Display` has a **negative coefficient** in the Ridge model — controlling for other variables, choosing Display reduces predicted revenue.
- **When it's still useful:** Retargeting (warm audiences who already visited the site).
- **Action item:** **First channel to cut for budget reallocation.** Specifically, the top recommendation in our business summary is *"Move 20–30% of Display/Affiliate spend to Search."*

## Channel × Audience Cross-Cuts (Patterns to Note)

While the dataset doesn't break out every cell, general patterns observed:

- **Search + Boomers / Gen X:** Highest revenue cluster — older audiences are heavier search-intent users.
- **Video + Gen Z:** TikTok / YouTube native — works for awareness but conversion lags.
- **Email + Millennials:** Strong inbox engagement when content is well-targeted.
- **Display + any audience:** Underperforms across the board.

## Cross-Channel Strategy Notes

1. **Don't optimize channels in isolation.** Search often "harvests" demand created by Video and Social. Killing top-of-funnel channels can hollow out Search's pipeline 2–4 weeks later.
2. **Attribution matters.** Last-click models over-credit Search and Email. Position-based or data-driven attribution gives a fairer picture.
3. **Channel mix benchmark:** A diversified, profitable mix in this dataset tends toward roughly 35% Search / 20% Video / 15% Email / 15% Social / 10% Affiliate / 5% Display.

## Summary for the Chatbot

When a user asks about a channel, lead with:
1. Where it ranks in this dataset (specific revenue number)
2. What it's actually best at (use case)
3. The top action item

Always remind that channel performance is contextual — a mediocre Search campaign can lose to a great Display campaign, but on average, the channel rank holds.
