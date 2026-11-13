
# ==========================================================
# MARKETING_PROFITABILITY
# Phase 25: Marketing KPI Analysis
# File: 04_marketing_kpis.py
# ==========================================================

from pathlib import Path
import pandas as pd
import numpy as np

# ----------------------------------------------------------
# 1. PROJECT PATH CONFIGURATION
# ----------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "01_Dataset" / "processed"
OUTPUT = ROOT / "04_Python" / "outputs"

OUTPUT.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("MARKETING PROFITABILITY - KPI ANALYSIS")
print("=" * 60)

# ----------------------------------------------------------
# 2. LOAD CLEANED DATASETS
# ----------------------------------------------------------

campaigns = pd.read_csv(DATA / "campaigns_cleaned.csv")
spend = pd.read_csv(DATA / "daily_spend_cleaned.csv")
leads = pd.read_csv(DATA / "leads_cleaned.csv")
conversions = pd.read_csv(DATA / "conversions_cleaned.csv")

print("\nAll cleaned datasets loaded successfully.")

# ----------------------------------------------------------
# 3. CALCULATE OVERALL MARKETING KPIs
# ----------------------------------------------------------

total_budget = campaigns["budget"].sum()
total_spend = spend["spend"].sum()
total_impressions = spend["impressions"].sum()
total_clicks = spend["clicks"].sum()
total_leads = len(leads)
total_conversions = len(conversions)
total_revenue = conversions["revenue"].sum()

def safe_divide(numerator, denominator):
    return numerator / denominator if denominator != 0 else np.nan

kpis = {
    "Total Budget": total_budget,
    "Total Spend": total_spend,
    "Total Impressions": total_impressions,
    "Total Clicks": total_clicks,
    "Total Leads": total_leads,
    "Total Conversions": total_conversions,
    "Total Revenue": total_revenue,
    "Marketing Profit": total_revenue - total_spend,
    "CTR (%)": safe_divide(total_clicks, total_impressions) * 100,
    "CPC": safe_divide(total_spend, total_clicks),
    "CPM": safe_divide(total_spend, total_impressions) * 1000,
    "CPL": safe_divide(total_spend, total_leads),
    "Cost Per Conversion": safe_divide(total_spend, total_conversions),
    "Lead Conversion Rate (%)": (
        safe_divide(total_conversions, total_leads) * 100
    ),
    "ROAS": safe_divide(total_revenue, total_spend),
    "Marketing ROI (%)": (
        safe_divide(total_revenue - total_spend, total_spend) * 100
    ),
    "Marketing Profit Margin (%)": (
        safe_divide(total_revenue - total_spend, total_revenue) * 100
    ),
    "Budget Utilization (%)": (
        safe_divide(total_spend, total_budget) * 100
    )
}

overall_kpis = pd.DataFrame(
    list(kpis.items()),
    columns=["KPI", "Value"]
)

print("\nOVERALL MARKETING KPIs")
print("-" * 60)
print(overall_kpis.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))

# ----------------------------------------------------------
# 4. AGGREGATE MARKETING SPEND BY CAMPAIGN
# ----------------------------------------------------------

spend_by_campaign = (
    spend.groupby("campaign_id", as_index=False)
    .agg(
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        spend=("spend", "sum")
    )
)

# ----------------------------------------------------------
# 5. AGGREGATE LEADS BY CAMPAIGN
# ----------------------------------------------------------

leads_by_campaign = (
    leads.groupby("campaign_id", as_index=False)
    .agg(leads=("lead_id", "count"))
)

# ----------------------------------------------------------
# 6. ATTRIBUTE CONVERSIONS TO CAMPAIGNS
# ----------------------------------------------------------

conversion_details = conversions.merge(
    leads[["lead_id", "campaign_id"]],
    on="lead_id",
    how="left",
    validate="many_to_one"
)

conversions_by_campaign = (
    conversion_details.groupby("campaign_id", as_index=False)
    .agg(
        conversions=("conversion_id", "count"),
        revenue=("revenue", "sum")
    )
)

# ----------------------------------------------------------
# 7. BUILD CAMPAIGN-LEVEL KPI DATASET
# ----------------------------------------------------------

campaign_kpis = (
    campaigns
    .merge(
        spend_by_campaign,
        on="campaign_id",
        how="left",
        validate="one_to_one"
    )
    .merge(
        leads_by_campaign,
        on="campaign_id",
        how="left",
        validate="one_to_one"
    )
    .merge(
        conversions_by_campaign,
        on="campaign_id",
        how="left",
        validate="one_to_one"
    )
)

numeric_columns = [
    "impressions", "clicks", "spend",
    "leads", "conversions", "revenue"
]

campaign_kpis[numeric_columns] = (
    campaign_kpis[numeric_columns].fillna(0)
)

# ----------------------------------------------------------
# 8. CALCULATE CAMPAIGN KPIs
# ----------------------------------------------------------

def divide_series(numerator, denominator):
    return numerator.div(denominator.replace(0, np.nan))

campaign_kpis["ctr_percentage"] = (
    divide_series(
        campaign_kpis["clicks"],
        campaign_kpis["impressions"]
    ) * 100
)

campaign_kpis["cpc"] = divide_series(
    campaign_kpis["spend"],
    campaign_kpis["clicks"]
)

campaign_kpis["cpl"] = divide_series(
    campaign_kpis["spend"],
    campaign_kpis["leads"]
)

campaign_kpis["cost_per_conversion"] = divide_series(
    campaign_kpis["spend"],
    campaign_kpis["conversions"]
)

campaign_kpis["conversion_rate_percentage"] = (
    divide_series(
        campaign_kpis["conversions"],
        campaign_kpis["leads"]
    ) * 100
)

campaign_kpis["roas"] = divide_series(
    campaign_kpis["revenue"],
    campaign_kpis["spend"]
)

campaign_kpis["marketing_profit"] = (
    campaign_kpis["revenue"] - campaign_kpis["spend"]
)

campaign_kpis["budget_utilization_percentage"] = (
    divide_series(
        campaign_kpis["spend"],
        campaign_kpis["budget"]
    ) * 100
)

# ----------------------------------------------------------
# 9. CHANNEL-LEVEL KPI ANALYSIS
# ----------------------------------------------------------

channel_kpis = (
    campaign_kpis.groupby("channel", as_index=False)
    .agg(
        campaigns=("campaign_id", "count"),
        budget=("budget", "sum"),
        spend=("spend", "sum"),
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        leads=("leads", "sum"),
        conversions=("conversions", "sum"),
        revenue=("revenue", "sum")
    )
)

channel_kpis["marketing_profit"] = (
    channel_kpis["revenue"] - channel_kpis["spend"]
)

channel_kpis["ctr_percentage"] = (
    divide_series(
        channel_kpis["clicks"],
        channel_kpis["impressions"]
    ) * 100
)

channel_kpis["cpc"] = divide_series(
    channel_kpis["spend"],
    channel_kpis["clicks"]
)

channel_kpis["cpl"] = divide_series(
    channel_kpis["spend"],
    channel_kpis["leads"]
)

channel_kpis["cost_per_conversion"] = divide_series(
    channel_kpis["spend"],
    channel_kpis["conversions"]
)

channel_kpis["conversion_rate_percentage"] = (
    divide_series(
        channel_kpis["conversions"],
        channel_kpis["leads"]
    ) * 100
)

channel_kpis["roas"] = divide_series(
    channel_kpis["revenue"],
    channel_kpis["spend"]
)

channel_kpis["roi_percentage"] = (
    divide_series(
        channel_kpis["marketing_profit"],
        channel_kpis["spend"]
    ) * 100
)

channel_kpis["budget_utilization_percentage"] = (
    divide_series(
        channel_kpis["spend"],
        channel_kpis["budget"]
    ) * 100
)

channel_kpis = channel_kpis.sort_values(
    "marketing_profit",
    ascending=False
)

print("\nCHANNEL MARKETING KPIs")
print("-" * 60)

display_columns = [
    "channel",
    "spend",
    "leads",
    "conversions",
    "revenue",
    "marketing_profit",
    "roas",
    "cost_per_conversion"
]

print(
    channel_kpis[display_columns]
    .round(2)
    .to_string(index=False)
)

# ----------------------------------------------------------
# 10. RANK CHANNELS
# ----------------------------------------------------------

channel_kpis["roas_rank"] = (
    channel_kpis["roas"]
    .rank(ascending=False, method="min")
    .astype("Int64")
)

channel_kpis["profit_rank"] = (
    channel_kpis["marketing_profit"]
    .rank(ascending=False, method="min")
    .astype("Int64")
)

channel_kpis["acquisition_cost_rank"] = (
    channel_kpis["cost_per_conversion"]
    .rank(ascending=True, method="min")
    .astype("Int64")
)

print("\nCHANNEL RANKINGS")
print("-" * 60)

print(
    channel_kpis[
        [
            "channel",
            "roas_rank",
            "profit_rank",
            "acquisition_cost_rank"
        ]
    ].to_string(index=False)
)

# ----------------------------------------------------------
# 11. SAVE OUTPUT FILES
# ----------------------------------------------------------

overall_kpis.to_csv(
    OUTPUT / "overall_marketing_kpis.csv",
    index=False
)

campaign_kpis.round(4).to_csv(
    OUTPUT / "campaign_marketing_kpis.csv",
    index=False
)

channel_kpis.round(4).to_csv(
    OUTPUT / "channel_marketing_kpis.csv",
    index=False
)

print("\nSaved output files:")
print("1. overall_marketing_kpis.csv")
print("2. campaign_marketing_kpis.csv")
print("3. channel_marketing_kpis.csv")

# ----------------------------------------------------------
# 12. VALIDATE AGAINST SQL
# ----------------------------------------------------------

print("\nSQL VS PYTHON KPI VALIDATION")
print("-" * 60)

expected_values = {
    "total_spend": 4523050.02,
    "total_leads": 261684,
    "total_conversions": 39696,
    "total_revenue": 21561839.01
}

actual_values = {
    "total_spend": total_spend,
    "total_leads": total_leads,
    "total_conversions": total_conversions,
    "total_revenue": total_revenue
}

all_valid = True

for metric, expected in expected_values.items():
    actual = actual_values[metric]
    passed = bool(np.isclose(actual, expected, rtol=0, atol=0.01))
    all_valid = all_valid and passed

    print(
        f"{metric:<20} "
        f"Expected: {expected:>15,.2f} "
        f"Actual: {actual:>15,.2f} "
        f"Status: {'PASS' if passed else 'FAIL'}"
    )

print("\n" + "=" * 60)
print(
    "KPI ANALYSIS COMPLETED"
    if all_valid
    else "KPI ANALYSIS COMPLETED WITH VALIDATION WARNINGS"
)
print("=" * 60)
