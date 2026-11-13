
# ==========================================================
# MARKETING_PROFITABILITY
# Phase 28: Marketing Budget Optimization
# File: 07_budget_optimization.py
# ==========================================================

from pathlib import Path
import pandas as pd
import numpy as np

# ----------------------------------------------------------
# 1. PROJECT PATHS
# ----------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "04_Python" / "outputs"
OUTPUT = INPUT

OUTPUT.mkdir(parents=True, exist_ok=True)

print("=" * 65)
print("MARKETING PROFITABILITY - BUDGET OPTIMIZATION")
print("=" * 65)

# ----------------------------------------------------------
# 2. LOAD CHANNEL PROFITABILITY DATA
# ----------------------------------------------------------

channel = pd.read_csv(
    INPUT / "channel_profitability.csv"
)

print("\nChannel profitability data loaded successfully.")

required_columns = [
    "channel",
    "total_budget",
    "total_spend",
    "total_revenue",
    "total_conversions",
    "marketing_profit",
    "roas"
]

missing_columns = [
    col for col in required_columns
    if col not in channel.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# ----------------------------------------------------------
# 3. CHANNEL BUDGET UTILIZATION
# ----------------------------------------------------------

def safe_divide(numerator, denominator):
    return numerator.div(
        denominator.replace(0, np.nan)
    )

channel["unspent_budget"] = (
    channel["total_budget"] - channel["total_spend"]
)

channel["budget_utilization_percentage"] = (
    safe_divide(
        channel["total_spend"],
        channel["total_budget"]
    ) * 100
)

print("\nCHANNEL BUDGET UTILIZATION")
print("-" * 65)

print(
    channel[
        [
            "channel",
            "total_budget",
            "total_spend",
            "unspent_budget",
            "budget_utilization_percentage"
        ]
    ].round(2).to_string(index=False)
)

# ----------------------------------------------------------
# 4. CHANNEL EFFICIENCY SCORECARD
# ----------------------------------------------------------

channel["cost_per_conversion"] = safe_divide(
    channel["total_spend"],
    channel["total_conversions"]
)

channel["roas_rank"] = (
    channel["roas"]
    .rank(ascending=False, method="min")
    .astype("Int64")
)

channel["cac_rank"] = (
    channel["cost_per_conversion"]
    .rank(ascending=True, method="min")
    .astype("Int64")
)

def classify_strategy(row):
    if row["roas_rank"] <= 2 and row["cac_rank"] <= 2:
        return "Evaluate for Expansion"
    elif row["roas_rank"] >= 4:
        return "Review Budget Efficiency"
    else:
        return "Maintain and Optimize"

channel["strategy"] = channel.apply(
    classify_strategy,
    axis=1
)

print("\nCHANNEL OPTIMIZATION SCORECARD")
print("-" * 65)

print(
    channel[
        [
            "channel",
            "roas",
            "cost_per_conversion",
            "roas_rank",
            "cac_rank",
            "strategy"
        ]
    ].round(2).to_string(index=False)
)

# ----------------------------------------------------------
# 5. BASELINE MARKETING PERFORMANCE
# ----------------------------------------------------------

baseline_spend = channel["total_spend"].sum()
baseline_revenue = channel["total_revenue"].sum()
baseline_profit = baseline_revenue - baseline_spend

baseline_roas = baseline_revenue / baseline_spend

print("\nBASELINE PERFORMANCE")
print("-" * 65)

print(f"Total Spend   : {baseline_spend:,.2f}")
print(f"Total Revenue : {baseline_revenue:,.2f}")
print(f"Total Profit  : {baseline_profit:,.2f}")
print(f"Overall ROAS  : {baseline_roas:.2f}x")

# ----------------------------------------------------------
# 6. BUDGET REALLOCATION SCENARIO
# ----------------------------------------------------------

# Illustrative scenario:
# Reduce Video spend by 10%.
# Reallocate 60% to Affiliate and 40% to Paid Search.

scenario = channel.copy()

video_mask = scenario["channel"] == "video"
affiliate_mask = scenario["channel"] == "affiliate"
search_mask = scenario["channel"] == "paid_search"

for name, mask in [
    ("video", video_mask),
    ("affiliate", affiliate_mask),
    ("paid_search", search_mask)
]:
    if mask.sum() != 1:
        raise ValueError(
            f"Expected exactly one row for channel: {name}"
        )

video_spend = scenario.loc[
    video_mask, "total_spend"
].iloc[0]

reallocated_budget = video_spend * 0.10

affiliate_allocation = reallocated_budget * 0.60
search_allocation = reallocated_budget * 0.40

scenario["spend_change"] = 0.0

scenario.loc[
    video_mask, "spend_change"
] = -reallocated_budget

scenario.loc[
    affiliate_mask, "spend_change"
] = affiliate_allocation

scenario.loc[
    search_mask, "spend_change"
] = search_allocation

scenario["scenario_spend"] = (
    scenario["total_spend"]
    + scenario["spend_change"]
)

# ----------------------------------------------------------
# 7. ESTIMATE SCENARIO REVENUE
# ----------------------------------------------------------

# Assumption:
# Historical channel ROAS remains constant.
# This is a sensitivity scenario, not a causal forecast.

scenario["scenario_revenue"] = (
    scenario["scenario_spend"]
    * scenario["roas"]
)

scenario["scenario_profit"] = (
    scenario["scenario_revenue"]
    - scenario["scenario_spend"]
)

scenario["incremental_revenue"] = (
    scenario["scenario_revenue"]
    - scenario["total_revenue"]
)

scenario["incremental_profit"] = (
    scenario["scenario_profit"]
    - scenario["marketing_profit"]
)

print("\nBUDGET REALLOCATION SCENARIO")
print("-" * 65)

print(f"Video Budget Reduction : {reallocated_budget:,.2f}")
print(f"Affiliate Allocation   : {affiliate_allocation:,.2f}")
print(f"Paid Search Allocation : {search_allocation:,.2f}")

print(
    scenario[
        [
            "channel",
            "total_spend",
            "spend_change",
            "scenario_spend",
            "scenario_revenue",
            "scenario_profit"
        ]
    ].round(2).to_string(index=False)
)

# ----------------------------------------------------------
# 8. SCENARIO PERFORMANCE COMPARISON
# ----------------------------------------------------------

scenario_total_spend = scenario["scenario_spend"].sum()
scenario_total_revenue = scenario["scenario_revenue"].sum()
scenario_total_profit = (
    scenario_total_revenue - scenario_total_spend
)

scenario_roas = (
    scenario_total_revenue / scenario_total_spend
)

comparison = pd.DataFrame({
    "metric": [
        "Total Spend",
        "Total Revenue",
        "Marketing Profit",
        "ROAS"
    ],
    "baseline": [
        baseline_spend,
        baseline_revenue,
        baseline_profit,
        baseline_roas
    ],
    "scenario": [
        scenario_total_spend,
        scenario_total_revenue,
        scenario_total_profit,
        scenario_roas
    ]
})

comparison["change"] = (
    comparison["scenario"]
    - comparison["baseline"]
)

print("\nBASELINE VS OPTIMIZATION SCENARIO")
print("-" * 65)

print(
    comparison.round(2).to_string(index=False)
)

# ----------------------------------------------------------
# 9. CHECK BUDGET CONSERVATION
# ----------------------------------------------------------

budget_difference = (
    scenario_total_spend - baseline_spend
)

budget_pass = bool(np.isclose(
    budget_difference,
    0,
    atol=0.01,
    rtol=0
))

print("\nBUDGET CONSERVATION VALIDATION")
print("-" * 65)

print(f"Budget Difference: {budget_difference:.2f}")
print(f"Status: {'PASS' if budget_pass else 'FAIL'}")

# ----------------------------------------------------------
# 10. SAVE OUTPUTS
# ----------------------------------------------------------

channel.round(4).to_csv(
    OUTPUT / "budget_optimization_scorecard.csv",
    index=False
)

scenario.round(4).to_csv(
    OUTPUT / "budget_reallocation_scenario.csv",
    index=False
)

comparison.round(4).to_csv(
    OUTPUT / "budget_scenario_comparison.csv",
    index=False
)

print("\nSaved output files:")
print("1. budget_optimization_scorecard.csv")
print("2. budget_reallocation_scenario.csv")
print("3. budget_scenario_comparison.csv")

# ----------------------------------------------------------
# 11. FINAL SUMMARY
# ----------------------------------------------------------

print("\n" + "=" * 65)

if budget_pass:
    print("BUDGET OPTIMIZATION ANALYSIS COMPLETED")
else:
    print("BUDGET OPTIMIZATION HAS VALIDATION WARNINGS")

print("=" * 65)

print("\nIMPORTANT:")
print("Scenario assumes constant historical channel ROAS.")
print("Results are illustrative, not guaranteed outcomes.")
