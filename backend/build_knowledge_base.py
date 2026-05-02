import pandas as pd
import numpy as np
import json
from pathlib import Path

df = pd.read_csv("digital_media_dataset.csv")
df.columns = df.columns.str.lower()
df["roas"] = df["revenue_usd"] / df["spend_usd"].replace(0, np.nan)

chunks = []

# --- 1. Per-channel stats ---
for channel, grp in df.groupby("channel"):
    chunks.append(
        f"Channel: {channel}. "
        f"Average revenue: ${grp['revenue_usd'].mean():,.0f}. "
        f"Average spend: ${grp['spend_usd'].mean():,.0f}. "
        f"Average ROAS: {grp['roas'].mean():.2f}x. "
        f"Average CTR: {grp['ctr_pct'].mean():.2f}%. "
        f"Average conversion rate: {grp['conversion_rate_pct'].mean():.2f}%. "
        f"Total campaigns: {len(grp)}."
    )

# --- 2. Per-region stats ---
for region, grp in df.groupby("region"):
    chunks.append(
        f"Region: {region}. "
        f"Average revenue: ${grp['revenue_usd'].mean():,.0f}. "
        f"Average spend: ${grp['spend_usd'].mean():,.0f}. "
        f"Best performing channel in this region: "
        f"{grp.groupby('channel')['revenue_usd'].mean().idxmax()}."
    )

# --- 3. Per-device stats ---
for device, grp in df.groupby("device_type"):
    chunks.append(
        f"Device type: {device}. "
        f"Average revenue: ${grp['revenue_usd'].mean():,.0f}. "
        f"Average CTR: {grp['ctr_pct'].mean():.2f}%. "
        f"Average conversion rate: {grp['conversion_rate_pct'].mean():.2f}%."
    )

# --- 4. Per-audience segment ---
for seg, grp in df.groupby("audience_segment"):
    chunks.append(
        f"Audience segment: {seg}. "
        f"Average revenue: ${grp['revenue_usd'].mean():,.0f}. "
        f"Average age: {grp['audience_age'].mean():.0f}. "
        f"Best channel for this segment: "
        f"{grp.groupby('channel')['revenue_usd'].mean().idxmax()}."
    )

# --- 5. Per-campaign objective ---
for obj, grp in df.groupby("campaign_objective"):
    chunks.append(
        f"Campaign objective: {obj}. "
        f"Average revenue: ${grp['revenue_usd'].mean():,.0f}. "
        f"Average conversion rate: {grp['conversion_rate_pct'].mean():.2f}%. "
        f"Best channel: {grp.groupby('channel')['revenue_usd'].mean().idxmax()}."
    )

# --- 6. Overall dataset summary ---
chunks.append(
    f"Overall CampaignIQ dataset summary: {len(df)} total campaigns. "
    f"Average revenue: ${df['revenue_usd'].mean():,.0f}. "
    f"Median ROAS: {df['roas'].median():.2f}x. "
    f"Top channel by revenue: {df.groupby('channel')['revenue_usd'].mean().idxmax()}. "
    f"Top region: {df.groupby('region')['revenue_usd'].mean().idxmax()}. "
    f"Top device: {df.groupby('device_type')['revenue_usd'].mean().idxmax()}. "
    f"Success rate (revenue > $19k): {(df['revenue_usd'] > 19000).mean()*100:.1f}%."
)

# Save
Path("knowledge_base.json").write_text(json.dumps(chunks, indent=2))
print(f"Saved {len(chunks)} chunks to knowledge_base.json")