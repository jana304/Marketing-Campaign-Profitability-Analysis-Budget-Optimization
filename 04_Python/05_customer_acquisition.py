
# ==========================================================
# MARKETING_PROFITABILITY
# Phase 26: Customer Acquisition Analysis
# File: 05_customer_acquisition.py
# ==========================================================

from pathlib import Path
import pandas as pd
import numpy as np

# ----------------------------------------------------------
# 1. PROJECT PATHS
# ----------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "01_Dataset" / "processed"
OUTPUT = ROOT / "04_Python" / "outputs"

OUTPUT.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("CUSTOMER ACQUISITION ANALYSIS")
print("=" * 60)

# ----------------------------------------------------------
# 2. LOAD CLEANED DATASETS
# ----------------------------------------------------------

campaigns = pd.read_csv(DATA / "campaigns_cleaned.csv")

spend = pd.read_csv(DATA / "daily_spend_cleaned.csv")

leads = pd.read_csv(
    DATA / "leads_cleaned.csv",
    parse_dates=["created_at"]
)

conversions = pd.read_csv(
    DATA / "conversions_cleaned.csv",
    parse_dates=["converted_at"]
)

print("\nAll datasets loaded successfully.")

# ----------------------------------------------------------
# 3. HELPER FUNCTION
# ----------------------------------------------------------

def safe_divide(numerator, denominator):
    return numerator.div(denominator.replace(0, np.nan))


# ----------------------------------------------------------
# 4. OVERALL ACQUISITION KPIs
# ----------------------------------------------------------

total_spend = spend["spend"].sum()
total_leads = len(leads)
total_conversions = len(conversions)

overall_conversion_rate = (
    total_conversions / total_leads * 100
    if total_leads else np.nan
)

overall_cpl = (
    total_spend / total_leads
    if total_leads else np.nan
)

overall_cac = (
    total_spend / total_conversions
    if total_conversions else np.nan
)

print("\nOVERALL ACQUISITION KPIs")
print("-" * 60)

print(f"Total Leads: {total_leads:,}")
print(f"Total Conversions: {total_conversions:,}")
print(f"Lead Conversion Rate: {overall_conversion_rate:.2f}%")
print(f"Cost Per Lead: {overall_cpl:.2f}")
print(f"Cost Per Conversion (CAC Proxy): {overall_cac:.2f}")

# ----------------------------------------------------------
# 5. AGGREGATE SPEND BY CAMPAIGN
# ----------------------------------------------------------

campaign_spend = (
    spend.groupby("campaign_id", as_index=False)
    .agg(total_spend=("spend", "sum"))
)

# ----------------------------------------------------------
# 6. AGGREGATE LEADS BY CAMPAIGN
# ----------------------------------------------------------

campaign_leads = (
    leads.groupby("campaign_id", as_index=False)
    .agg(total_leads=("lead_id", "count"))
)

# ----------------------------------------------------------
# 7. ATTRIBUTE CONVERSIONS TO CAMPAIGNS
# ----------------------------------------------------------

conversion_details = conversions.merge(
    leads[["lead_id", "campaign_id", "created_at"]],
    on="lead_id",
    how="left",
    validate="many_to_one"
)

campaign_conversions = (
    conversion_details.groupby("campaign_id", as_index=False)
    .agg(
        total_conversions=("conversion_id", "count"),
        total_revenue=("revenue", "sum")
    )
)

# ----------------------------------------------------------
# 8. BUILD CAMPAIGN ACQUISITION DATASET
# ----------------------------------------------------------

campaign_acquisition = (
    campaigns[["campaign_id", "campaign_name", "channel"]]
    .merge(
        campaign_spend,
        on="campaign_id",
        how="left",
        validate="one_to_one"
    )
    .merge(
        campaign_leads,
        on="campaign_id",
        how="left",
        validate="one_to_one"
    )
    .merge(
        campaign_conversions,
        on="campaign_id",
        how="left",
        validate="one_to_one"
    )
)

numeric_columns = [
    "total_spend",
    "total_leads",
    "total_conversions",
    "total_revenue"
]

campaign_acquisition[numeric_columns] = (
    campaign_acquisition[numeric_columns].fillna(0)
)

# ----------------------------------------------------------
# 9. CALCULATE CAMPAIGN ACQUISITION KPIs
# ----------------------------------------------------------

campaign_acquisition["conversion_rate_percentage"] = (
    safe_divide(
        campaign_acquisition["total_conversions"],
        campaign_acquisition["total_leads"]
    ) * 100
)

campaign_acquisition["cost_per_lead"] = safe_divide(
    campaign_acquisition["total_spend"],
    campaign_acquisition["total_leads"]
)

campaign_acquisition["cost_per_conversion"] = safe_divide(
    campaign_acquisition["total_spend"],
    campaign_acquisition["total_conversions"]
)

# ----------------------------------------------------------
# 10. CHANNEL ACQUISITION PERFORMANCE
# ----------------------------------------------------------

channel_acquisition = (
    campaign_acquisition.groupby("channel", as_index=False)
    .agg(
        total_spend=("total_spend", "sum"),
        total_leads=("total_leads", "sum"),
        total_conversions=("total_conversions", "sum"),
        total_revenue=("total_revenue", "sum")
    )
)

channel_acquisition["conversion_rate_percentage"] = (
    safe_divide(
        channel_acquisition["total_conversions"],
        channel_acquisition["total_leads"]
    ) * 100
)

channel_acquisition["cost_per_lead"] = safe_divide(
    channel_acquisition["total_spend"],
    channel_acquisition["total_leads"]
)

channel_acquisition["cost_per_conversion"] = safe_divide(
    channel_acquisition["total_spend"],
    channel_acquisition["total_conversions"]
)

channel_acquisition["cac_rank"] = (
    channel_acquisition["cost_per_conversion"]
    .rank(method="min", ascending=True)
    .astype("Int64")
)

channel_acquisition["conversion_rate_rank"] = (
    channel_acquisition["conversion_rate_percentage"]
    .rank(method="min", ascending=False)
    .astype("Int64")
)

channel_acquisition = channel_acquisition.sort_values(
    "cac_rank"
)

print("\nCHANNEL ACQUISITION PERFORMANCE")
print("-" * 60)

print(
    channel_acquisition.round(2).to_string(index=False)
)

# ----------------------------------------------------------
# 11. LEAD SOURCE ANALYSIS
# ----------------------------------------------------------

lead_sources = (
    leads.groupby("lead_source", as_index=False)
    .agg(total_leads=("lead_id", "count"))
    .sort_values("total_leads", ascending=False)
)

print("\nLEADS BY SOURCE")
print("-" * 60)
print(lead_sources.to_string(index=False))

# ----------------------------------------------------------
# 12. LEAD SCORE SEGMENTATION
# ----------------------------------------------------------

leads["lead_score_segment"] = pd.cut(
    leads["lead_score"],
    bins=[-0.01, 25, 50, 75, 100],
    labels=["Low", "Medium", "High", "Very High"],
    include_lowest=True
)

lead_score_summary = (
    leads.groupby(
        "lead_score_segment",
        observed=False
    )
    .agg(total_leads=("lead_id", "count"))
    .reset_index()
)

print("\nLEAD SCORE DISTRIBUTION")
print("-" * 60)
print(lead_score_summary.to_string(index=False))

# ----------------------------------------------------------
# 13. MONTHLY LEAD TREND
# ----------------------------------------------------------

leads["month"] = (
    leads["created_at"].dt.to_period("M").astype(str)
)

monthly_leads = (
    leads.groupby("month", as_index=False)
    .agg(total_leads=("lead_id", "count"))
    .sort_values("month")
)

print("\nMONTHLY LEAD TREND")
print("-" * 60)
print(monthly_leads.to_string(index=False))

# ----------------------------------------------------------
# 14. MONTHLY CONVERSION TREND
# ----------------------------------------------------------

conversions["month"] = (
    conversions["converted_at"].dt.to_period("M").astype(str)
)

monthly_conversions = (
    conversions.groupby("month", as_index=False)
    .agg(total_conversions=("conversion_id", "count"))
    .sort_values("month")
)

print("\nMONTHLY CONVERSION TREND")
print("-" * 60)
print(monthly_conversions.to_string(index=False))

# ----------------------------------------------------------
# 15. TIME TO CONVERSION
# ----------------------------------------------------------

conversion_details["days_to_conversion"] = (
    conversion_details["converted_at"]
    - conversion_details["created_at"]
).dt.total_seconds() / 86400

valid_conversion_times = conversion_details[
    conversion_details["days_to_conversion"].notna()
    & (conversion_details["days_to_conversion"] >= 0)
]

average_days_to_conversion = (
    valid_conversion_times["days_to_conversion"].mean()
)

print("\nTIME TO CONVERSION")
print("-" * 60)

print(
    f"Average Days to Conversion: "
    f"{average_days_to_conversion:.2f}"
)

invalid_conversion_times = (
    conversion_details["days_to_conversion"].lt(0).sum()
)

print(
    f"Conversions Before Lead Creation: "
    f"{invalid_conversion_times}"
)

# ----------------------------------------------------------
# 16. SAVE OUTPUTS
# ----------------------------------------------------------

outputs = {
    "campaign_acquisition_analysis.csv":
        campaign_acquisition,
    "channel_acquisition_analysis.csv":
        channel_acquisition,
    "lead_source_analysis.csv":
        lead_sources,
    "lead_score_distribution.csv":
        lead_score_summary,
    "monthly_lead_trend.csv":
        monthly_leads,
    "monthly_conversion_trend.csv":
        monthly_conversions
}

for filename, dataframe in outputs.items():
    dataframe.round(4).to_csv(
        OUTPUT / filename,
        index=False
    )
    print(f"Saved: {filename}")

# ----------------------------------------------------------
# 17. VALIDATE AGAINST SQL
# ----------------------------------------------------------

print("\nSQL VS PYTHON ACQUISITION VALIDATION")
print("-" * 60)

expected = {
    "total_leads": 261684,
    "total_conversions": 39696,
    "total_spend": 4523050.02
}

actual = {
    "total_leads": total_leads,
    "total_conversions": total_conversions,
    "total_spend": total_spend
}

all_valid = True

for metric, expected_value in expected.items():
    actual_value = actual[metric]

    passed = bool(np.isclose(
        actual_value,
        expected_value,
        rtol=0,
        atol=0.01
    ))

    all_valid = all_valid and passed

    print(
        f"{metric:<20} "
        f"Expected: {expected_value:>15,.2f} "
        f"Actual: {actual_value:>15,.2f} "
        f"Status: {'PASS' if passed else 'FAIL'}"
    )

print("\n" + "=" * 60)
print(
    "CUSTOMER ACQUISITION ANALYSIS COMPLETED"
    if all_valid
    else "ANALYSIS COMPLETED WITH VALIDATION WARNINGS"
)
print("=" * 60)
