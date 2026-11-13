
# ==========================================================
# MARKETING_PROFITABILITY
# Phase 27: Revenue and Profitability Analysis
# File: 06_profitability_analysis.py
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

print("=" * 65)
print("MARKETING PROFITABILITY - REVENUE & PROFIT ANALYSIS")
print("=" * 65)

# ----------------------------------------------------------
# 2. LOAD CLEANED DATASETS
# ----------------------------------------------------------

campaigns = pd.read_csv(DATA / "campaigns_cleaned.csv")
spend = pd.read_csv(DATA / "daily_spend_cleaned.csv")
leads = pd.read_csv(DATA / "leads_cleaned.csv")
conversions = pd.read_csv(DATA / "conversions_cleaned.csv")

print("\nAll four cleaned datasets loaded successfully.")

# ----------------------------------------------------------
# 3. HELPER FUNCTION
# ----------------------------------------------------------

def safe_divide(numerator, denominator):
    return numerator.div(denominator.replace(0, np.nan))

# ----------------------------------------------------------
# 4. OVERALL PROFITABILITY
# ----------------------------------------------------------

total_spend = spend["spend"].sum()
total_revenue = conversions["revenue"].sum()
total_profit = total_revenue - total_spend

overall_roas = total_revenue / total_spend
overall_roi = (total_profit / total_spend) * 100
overall_margin = (total_profit / total_revenue) * 100

print("\nOVERALL PROFITABILITY")
print("-" * 65)

print(f"Total Marketing Spend : {total_spend:,.2f}")
print(f"Total Revenue         : {total_revenue:,.2f}")
print(f"Marketing Profit      : {total_profit:,.2f}")
print(f"ROAS                  : {overall_roas:.2f}x")
print(f"Marketing ROI         : {overall_roi:.2f}%")
print(f"Marketing Margin      : {overall_margin:.2f}%")

# ----------------------------------------------------------
# 5. AGGREGATE CAMPAIGN SPEND
# ----------------------------------------------------------

campaign_spend = (
    spend.groupby("campaign_id", as_index=False)
    .agg(
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        total_spend=("spend", "sum")
    )
)

# ----------------------------------------------------------
# 6. ATTRIBUTE REVENUE TO CAMPAIGNS
# ----------------------------------------------------------

conversion_details = conversions.merge(
    leads[["lead_id", "campaign_id"]],
    on="lead_id",
    how="left",
    validate="many_to_one"
)

campaign_revenue = (
    conversion_details.groupby("campaign_id", as_index=False)
    .agg(
        total_conversions=("conversion_id", "count"),
        total_revenue=("revenue", "sum")
    )
)

# ----------------------------------------------------------
# 7. BUILD CAMPAIGN PROFITABILITY DATASET
# ----------------------------------------------------------

campaign_profitability = (
    campaigns
    .merge(
        campaign_spend,
        on="campaign_id",
        how="left",
        validate="one_to_one"
    )
    .merge(
        campaign_revenue,
        on="campaign_id",
        how="left",
        validate="one_to_one"
    )
)

numeric_columns = [
    "impressions",
    "clicks",
    "total_spend",
    "total_conversions",
    "total_revenue"
]

campaign_profitability[numeric_columns] = (
    campaign_profitability[numeric_columns].fillna(0)
)

# ----------------------------------------------------------
# 8. CALCULATE CAMPAIGN PROFITABILITY METRICS
# ----------------------------------------------------------

campaign_profitability["marketing_profit"] = (
    campaign_profitability["total_revenue"]
    - campaign_profitability["total_spend"]
)

campaign_profitability["roas"] = safe_divide(
    campaign_profitability["total_revenue"],
    campaign_profitability["total_spend"]
)

campaign_profitability["roi_percentage"] = (
    safe_divide(
        campaign_profitability["marketing_profit"],
        campaign_profitability["total_spend"]
    ) * 100
)

campaign_profitability["profit_margin_percentage"] = (
    safe_divide(
        campaign_profitability["marketing_profit"],
        campaign_profitability["total_revenue"]
    ) * 100
)

campaign_profitability["budget_utilization_percentage"] = (
    safe_divide(
        campaign_profitability["total_spend"],
        campaign_profitability["budget"]
    ) * 100
)

campaign_profitability["cost_per_conversion"] = (
    safe_divide(
        campaign_profitability["total_spend"],
        campaign_profitability["total_conversions"]
    )
)

# ----------------------------------------------------------
# 9. CHANNEL PROFITABILITY ANALYSIS
# ----------------------------------------------------------

channel_profitability = (
    campaign_profitability.groupby("channel", as_index=False)
    .agg(
        campaign_count=("campaign_id", "count"),
        total_budget=("budget", "sum"),
        total_spend=("total_spend", "sum"),
        total_conversions=("total_conversions", "sum"),
        total_revenue=("total_revenue", "sum")
    )
)

channel_profitability["marketing_profit"] = (
    channel_profitability["total_revenue"]
    - channel_profitability["total_spend"]
)

channel_profitability["roas"] = safe_divide(
    channel_profitability["total_revenue"],
    channel_profitability["total_spend"]
)

channel_profitability["roi_percentage"] = (
    safe_divide(
        channel_profitability["marketing_profit"],
        channel_profitability["total_spend"]
    ) * 100
)

channel_profitability["profit_margin_percentage"] = (
    safe_divide(
        channel_profitability["marketing_profit"],
        channel_profitability["total_revenue"]
    ) * 100
)

channel_profitability["cost_per_conversion"] = (
    safe_divide(
        channel_profitability["total_spend"],
        channel_profitability["total_conversions"]
    )
)

channel_profitability["budget_utilization_percentage"] = (
    safe_divide(
        channel_profitability["total_spend"],
        channel_profitability["total_budget"]
    ) * 100
)

# ----------------------------------------------------------
# 10. RANK CHANNELS
# ----------------------------------------------------------

channel_profitability["roas_rank"] = (
    channel_profitability["roas"]
    .rank(ascending=False, method="min")
    .astype("Int64")
)

channel_profitability["profit_rank"] = (
    channel_profitability["marketing_profit"]
    .rank(ascending=False, method="min")
    .astype("Int64")
)

channel_profitability = channel_profitability.sort_values(
    "roas_rank"
)

print("\nCHANNEL PROFITABILITY SCORECARD")
print("-" * 65)

display_columns = [
    "channel",
    "total_spend",
    "total_revenue",
    "marketing_profit",
    "roas",
    "roi_percentage",
    "roas_rank"
]

print(
    channel_profitability[display_columns]
    .round(2)
    .to_string(index=False)
)

# ----------------------------------------------------------
# 11. TOP 10 MOST PROFITABLE CAMPAIGNS
# ----------------------------------------------------------

top_campaigns = campaign_profitability.nlargest(
    10, "marketing_profit"
)

print("\nTOP 10 MOST PROFITABLE CAMPAIGNS")
print("-" * 65)

print(
    top_campaigns[
        [
            "campaign_id",
            "campaign_name",
            "channel",
            "total_spend",
            "total_revenue",
            "marketing_profit",
            "roas"
        ]
    ].round(2).to_string(index=False)
)

# ----------------------------------------------------------
# 12. BOTTOM 10 CAMPAIGNS BY PROFIT
# ----------------------------------------------------------

bottom_campaigns = campaign_profitability.nsmallest(
    10, "marketing_profit"
)

print("\nBOTTOM 10 CAMPAIGNS BY MARKETING PROFIT")
print("-" * 65)

print(
    bottom_campaigns[
        [
            "campaign_id",
            "campaign_name",
            "channel",
            "marketing_profit",
            "roas"
        ]
    ].round(2).to_string(index=False)
)

# ----------------------------------------------------------
# 13. CHANNEL REVENUE CONTRIBUTION
# ----------------------------------------------------------

channel_profitability["revenue_share_percentage"] = (
    channel_profitability["total_revenue"]
    / total_revenue * 100
)

channel_profitability["spend_share_percentage"] = (
    channel_profitability["total_spend"]
    / total_spend * 100
)

print("\nCHANNEL REVENUE AND SPEND SHARES")
print("-" * 65)

print(
    channel_profitability[
        [
            "channel",
            "revenue_share_percentage",
            "spend_share_percentage"
        ]
    ].round(2).to_string(index=False)
)

# ----------------------------------------------------------
# 14. SAVE ANALYSIS OUTPUTS
# ----------------------------------------------------------

overall_summary = pd.DataFrame([{
    "total_spend": total_spend,
    "total_revenue": total_revenue,
    "marketing_profit": total_profit,
    "roas": overall_roas,
    "roi_percentage": overall_roi,
    "profit_margin_percentage": overall_margin
}])

outputs = {
    "overall_profitability.csv": overall_summary,
    "campaign_profitability.csv": campaign_profitability,
    "channel_profitability.csv": channel_profitability,
    "top_10_profitable_campaigns.csv": top_campaigns,
    "bottom_10_profit_campaigns.csv": bottom_campaigns
}

for filename, dataframe in outputs.items():
    dataframe.round(4).to_csv(
        OUTPUT / filename,
        index=False
    )
    print(f"Saved: {filename}")

# ----------------------------------------------------------
# 15. SQL VS PYTHON VALIDATION
# ----------------------------------------------------------

print("\nSQL VS PYTHON PROFITABILITY VALIDATION")
print("-" * 65)

expected = {
    "Total Spend": 4523050.02,
    "Total Revenue": 21561839.01,
    "Marketing Profit": 17038788.99,
    "ROAS": 4.77,
    "Marketing ROI": 376.71
}

actual = {
    "Total Spend": total_spend,
    "Total Revenue": total_revenue,
    "Marketing Profit": total_profit,
    "ROAS": overall_roas,
    "Marketing ROI": overall_roi
}

all_valid = True

for metric, expected_value in expected.items():

    actual_value = actual[metric]

    tolerance = 0.02 if metric in ["ROAS", "Marketing ROI"] else 0.01

    passed = bool(np.isclose(
        actual_value,
        expected_value,
        atol=tolerance,
        rtol=0
    ))

    all_valid = all_valid and passed

    print(
        f"{metric:<20} "
        f"Expected: {expected_value:>15,.2f} "
        f"Actual: {actual_value:>15,.2f} "
        f"Status: {'PASS' if passed else 'FAIL'}"
    )

print("\n" + "=" * 65)

if all_valid:
    print("PROFITABILITY ANALYSIS COMPLETED SUCCESSFULLY")
else:
    print("ANALYSIS COMPLETED WITH VALIDATION WARNINGS")

print("=" * 65)
