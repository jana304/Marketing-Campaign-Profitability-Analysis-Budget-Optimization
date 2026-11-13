
# ==========================================================
# MARKETING_PROFITABILITY
# Phase 24: Exploratory Data Analysis
# File: 03_exploratory_analysis.py
# ==========================================================

from pathlib import Path
import pandas as pd

# ----------------------------------------------------------
# 1. PROJECT PATHS
# ----------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "01_Dataset" / "processed"
OUTPUT = ROOT / "04_Python" / "outputs"

OUTPUT.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("MARKETING PROFITABILITY - EXPLORATORY ANALYSIS")
print("=" * 60)

# ----------------------------------------------------------
# 2. LOAD CLEANED DATASETS
# ----------------------------------------------------------

campaigns = pd.read_csv(DATA / "campaigns_cleaned.csv")
spend = pd.read_csv(
    DATA / "daily_spend_cleaned.csv",
    parse_dates=["spend_date"]
)
leads = pd.read_csv(
    DATA / "leads_cleaned.csv",
    parse_dates=["created_at"]
)
conversions = pd.read_csv(
    DATA / "conversions_cleaned.csv",
    parse_dates=["converted_at"]
)

print("\nCleaned datasets loaded successfully.")

# ----------------------------------------------------------
# 3. DATASET SUMMARY
# ----------------------------------------------------------

datasets = {
    "Campaigns": campaigns,
    "Daily Spend": spend,
    "Leads": leads,
    "Conversions": conversions
}

print("\nDATASET SUMMARY")
print("-" * 60)

for name, df in datasets.items():
    print(f"{name}: {len(df):,} rows, {len(df.columns)} columns")

# ----------------------------------------------------------
# 4. NUMERICAL STATISTICS
# ----------------------------------------------------------

print("\nNUMERICAL STATISTICS")
print("-" * 60)

for name, df in datasets.items():
    print(f"\n{name}")
    print(df.describe(include="number").round(2).to_string())

# ----------------------------------------------------------
# 5. CAMPAIGNS BY CHANNEL
# ----------------------------------------------------------

campaign_count = (
    campaigns.groupby("channel")
    .size()
    .reset_index(name="campaign_count")
    .sort_values("campaign_count", ascending=False)
)

print("\nCAMPAIGNS BY CHANNEL")
print(campaign_count.to_string(index=False))

# ----------------------------------------------------------
# 6. MARKETING SPEND BY CHANNEL
# ----------------------------------------------------------

spend_channel = spend.merge(
    campaigns[["campaign_id", "channel"]],
    on="campaign_id",
    how="left",
    validate="many_to_one"
)

channel_spend = (
    spend_channel.groupby("channel", as_index=False)
    .agg(
        total_spend=("spend", "sum"),
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum")
    )
)

channel_spend["ctr_percentage"] = (
    channel_spend["clicks"] /
    channel_spend["impressions"].replace(0, float("nan"))
    * 100
)

channel_spend["cpc"] = (
    channel_spend["total_spend"] /
    channel_spend["clicks"].replace(0, float("nan"))
)

print("\nMARKETING PERFORMANCE BY CHANNEL")
print(channel_spend.round(2).to_string(index=False))

# ----------------------------------------------------------
# 7. LEADS BY CHANNEL
# ----------------------------------------------------------

lead_channel = leads.merge(
    campaigns[["campaign_id", "channel"]],
    on="campaign_id",
    how="left",
    validate="many_to_one"
)

channel_leads = (
    lead_channel.groupby("channel")
    .size()
    .reset_index(name="total_leads")
)

print("\nLEADS BY CHANNEL")
print(channel_leads.to_string(index=False))

# ----------------------------------------------------------
# 8. CONVERSIONS AND REVENUE BY CHANNEL
# ----------------------------------------------------------

conversion_channel = conversions.merge(
    leads[["lead_id", "campaign_id"]],
    on="lead_id",
    how="left",
    validate="many_to_one"
).merge(
    campaigns[["campaign_id", "channel"]],
    on="campaign_id",
    how="left",
    validate="many_to_one"
)

channel_revenue = (
    conversion_channel.groupby("channel", as_index=False)
    .agg(
        total_conversions=("conversion_id", "count"),
        total_revenue=("revenue", "sum")
    )
)

print("\nCONVERSIONS AND REVENUE BY CHANNEL")
print(channel_revenue.round(2).to_string(index=False))

# ----------------------------------------------------------
# 9. COMBINED CHANNEL PERFORMANCE
# ----------------------------------------------------------

summary = (
    channel_spend
    .merge(channel_leads, on="channel", how="outer")
    .merge(channel_revenue, on="channel", how="outer")
)

count_columns = [
    "impressions", "clicks", "total_leads",
    "total_conversions"
]

summary[count_columns] = summary[count_columns].fillna(0)

summary[["total_spend", "total_revenue"]] = (
    summary[["total_spend", "total_revenue"]].fillna(0)
)

summary["marketing_profit"] = (
    summary["total_revenue"] - summary["total_spend"]
)

summary["roas"] = (
    summary["total_revenue"] /
    summary["total_spend"].replace(0, float("nan"))
)

summary["conversion_rate_percentage"] = (
    summary["total_conversions"] /
    summary["total_leads"].replace(0, float("nan"))
    * 100
)

summary["cost_per_lead"] = (
    summary["total_spend"] /
    summary["total_leads"].replace(0, float("nan"))
)

summary["cost_per_conversion"] = (
    summary["total_spend"] /
    summary["total_conversions"].replace(0, float("nan"))
)

summary = summary.sort_values("marketing_profit", ascending=False)

print("\nCOMPLETE CHANNEL PERFORMANCE SUMMARY")
print(summary.round(2).to_string(index=False))

# ----------------------------------------------------------
# 10. MONTHLY SPEND TREND
# ----------------------------------------------------------

spend["month"] = spend["spend_date"].dt.to_period("M").astype(str)

monthly_spend = (
    spend.groupby("month", as_index=False)
    .agg(total_spend=("spend", "sum"))
    .sort_values("month")
)

print("\nMONTHLY SPEND TREND")
print(monthly_spend.round(2).to_string(index=False))

# ----------------------------------------------------------
# 11. MONTHLY REVENUE TREND
# ----------------------------------------------------------

conversions["month"] = (
    conversions["converted_at"].dt.to_period("M").astype(str)
)

monthly_revenue = (
    conversions.groupby("month", as_index=False)
    .agg(total_revenue=("revenue", "sum"))
    .sort_values("month")
)

print("\nMONTHLY REVENUE TREND")
print(monthly_revenue.round(2).to_string(index=False))

# ----------------------------------------------------------
# 12. SAVE ANALYSIS OUTPUTS
# ----------------------------------------------------------

campaign_count.to_csv(
    OUTPUT / "eda_campaign_count.csv", index=False
)

summary.round(4).to_csv(
    OUTPUT / "eda_channel_summary.csv", index=False
)

monthly_spend.to_csv(
    OUTPUT / "eda_monthly_spend.csv", index=False
)

monthly_revenue.to_csv(
    OUTPUT / "eda_monthly_revenue.csv", index=False
)

print("\nAnalysis files saved successfully.")

# ----------------------------------------------------------
# 13. VALIDATE AGAINST SQL TOTALS
# ----------------------------------------------------------

print("\nSQL VS PYTHON VALIDATION")
print("-" * 60)

expected = {
    "spend": 4523050.02,
    "leads": 261684,
    "conversions": 39696,
    "revenue": 21561839.01
}

actual = {
    "spend": spend["spend"].sum(),
    "leads": len(leads),
    "conversions": len(conversions),
    "revenue": conversions["revenue"].sum()
}

for metric in expected:
    difference = abs(actual[metric] - expected[metric])
    status = "PASS" if difference < 0.01 else "FAIL"

    print(
        f"{metric:<15} "
        f"Expected: {expected[metric]:>15,.2f} "
        f"Actual: {actual[metric]:>15,.2f} "
        f"Status: {status}"
    )

print("\n" + "=" * 60)
print("EXPLORATORY DATA ANALYSIS COMPLETED")
print("=" * 60)
