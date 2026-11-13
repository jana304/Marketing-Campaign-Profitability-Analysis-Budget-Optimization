
# ==========================================================
# MARKETING_PROFITABILITY
# Phase 29: Python Data Visualizations
# File: 08_data_visualizations.py
# ==========================================================

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------
# 1. PROJECT PATHS
# ----------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "04_Python" / "outputs"
OUTPUT = ROOT / "05_Visualizations"

OUTPUT.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------
# 2. CHART STYLING
# ----------------------------------------------------------

sns.set_theme(style="whitegrid", context="notebook")

plt.rcParams.update({
    "figure.figsize": (11, 6),
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "font.size": 11,
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False
})

COLORS = {
    "blue": "#2563EB",
    "green": "#059669",
    "orange": "#F59E0B",
    "red": "#DC2626",
    "purple": "#7C3AED"
}

print("=" * 65)
print("MARKETING PROFITABILITY - DATA VISUALIZATIONS")
print("=" * 65)

# ----------------------------------------------------------
# 3. LOAD ANALYSIS OUTPUTS
# ----------------------------------------------------------

channel = pd.read_csv(
    INPUT / "channel_profitability.csv"
)

acquisition = pd.read_csv(
    INPUT / "channel_acquisition_analysis.csv"
)

monthly_spend = pd.read_csv(
    INPUT / "eda_monthly_spend.csv"
)

monthly_revenue = pd.read_csv(
    INPUT / "eda_monthly_revenue.csv"
)

campaigns = pd.read_csv(
    INPUT / "campaign_profitability.csv"
)

scenario = pd.read_csv(
    INPUT / "budget_scenario_comparison.csv"
)

print("\nAll analysis files loaded successfully.")

# ----------------------------------------------------------
# 4. HELPER FUNCTION
# ----------------------------------------------------------

def save_chart(filename):
    plt.tight_layout()
    plt.savefig(
        OUTPUT / filename,
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )
    plt.close()
    print(f"Saved: {filename}")


def format_millions(value):
    return f"{value / 1_000_000:.2f}M"


# ----------------------------------------------------------
# CHART 1: REVENUE BY MARKETING CHANNEL
# ----------------------------------------------------------

data = channel.sort_values("total_revenue")

fig, ax = plt.subplots()

bars = ax.barh(
    data["channel"],
    data["total_revenue"],
    color=COLORS["blue"]
)

ax.bar_label(
    bars,
    labels=[
        format_millions(v)
        for v in data["total_revenue"]
    ],
    padding=5
)

ax.set_title("Revenue by Marketing Channel")
ax.set_xlabel("Attributed Revenue")
ax.set_ylabel("Marketing Channel")
ax.set_xlim(0, data["total_revenue"].max() * 1.18)

save_chart("01_revenue_by_channel.png")

# ----------------------------------------------------------
# CHART 2: ROAS BY MARKETING CHANNEL
# ----------------------------------------------------------

data = channel.sort_values("roas")

fig, ax = plt.subplots()

bars = ax.barh(
    data["channel"],
    data["roas"],
    color=COLORS["green"]
)

ax.bar_label(
    bars,
    fmt="%.2fx",
    padding=5
)

ax.set_title("Return on Ad Spend by Channel")
ax.set_xlabel("ROAS (x)")
ax.set_ylabel("Marketing Channel")
ax.set_xlim(0, data["roas"].max() * 1.20)

save_chart("02_roas_by_channel.png")

# ----------------------------------------------------------
# CHART 3: MONTHLY SPEND VS REVENUE
# ----------------------------------------------------------

monthly = monthly_spend.merge(
    monthly_revenue,
    on="month",
    how="outer"
).fillna(0)

monthly = monthly.sort_values("month")

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    monthly["month"],
    monthly["total_spend"],
    marker="o",
    linewidth=2.5,
    label="Marketing Spend",
    color=COLORS["orange"]
)

ax.plot(
    monthly["month"],
    monthly["total_revenue"],
    marker="o",
    linewidth=2.5,
    label="Attributed Revenue",
    color=COLORS["blue"]
)

ax.set_title("Monthly Marketing Spend vs Revenue")
ax.set_xlabel("Month")
ax.set_ylabel("Amount")
ax.legend()

plt.xticks(rotation=45, ha="right")

save_chart("03_monthly_spend_vs_revenue.png")

# ----------------------------------------------------------
# CHART 4: COST PER CONVERSION BY CHANNEL
# ----------------------------------------------------------

data = acquisition.sort_values(
    "cost_per_conversion",
    ascending=False
)

fig, ax = plt.subplots()

bars = ax.barh(
    data["channel"],
    data["cost_per_conversion"],
    color=COLORS["red"]
)

ax.bar_label(
    bars,
    fmt="%.2f",
    padding=5
)

ax.set_title("Cost Per Conversion by Channel")
ax.set_xlabel("Advertising Cost per Conversion")
ax.set_ylabel("Marketing Channel")
ax.set_xlim(
    0,
    data["cost_per_conversion"].max() * 1.20
)

save_chart("04_cost_per_conversion.png")

# ----------------------------------------------------------
# CHART 5: LEAD CONVERSION RATE BY CHANNEL
# ----------------------------------------------------------

data = acquisition.sort_values(
    "conversion_rate_percentage"
)

fig, ax = plt.subplots()

bars = ax.barh(
    data["channel"],
    data["conversion_rate_percentage"],
    color=COLORS["purple"]
)

ax.bar_label(
    bars,
    fmt="%.2f%%",
    padding=5
)

ax.set_title("Lead Conversion Rate by Channel")
ax.set_xlabel("Lead Conversion Rate (%)")
ax.set_ylabel("Marketing Channel")
ax.set_xlim(
    0,
    data["conversion_rate_percentage"].max() * 1.20
)

save_chart("05_conversion_rate_by_channel.png")

# ----------------------------------------------------------
# CHART 6: MARKETING PROFIT BY CHANNEL
# ----------------------------------------------------------

data = channel.sort_values("marketing_profit")

fig, ax = plt.subplots()

bars = ax.barh(
    data["channel"],
    data["marketing_profit"],
    color=COLORS["green"]
)

ax.bar_label(
    bars,
    labels=[
        format_millions(v)
        for v in data["marketing_profit"]
    ],
    padding=5
)

ax.set_title("Marketing Profit by Channel")
ax.set_xlabel("Attributed Revenue Minus Ad Spend")
ax.set_ylabel("Marketing Channel")
ax.set_xlim(
    min(0, data["marketing_profit"].min() * 1.1),
    data["marketing_profit"].max() * 1.20
)

save_chart("06_marketing_profit_by_channel.png")

# ----------------------------------------------------------
# CHART 7: TOP 10 PROFITABLE CAMPAIGNS
# ----------------------------------------------------------

data = campaigns.nlargest(
    10, "marketing_profit"
).sort_values("marketing_profit")

fig, ax = plt.subplots(figsize=(12, 7))

bars = ax.barh(
    data["campaign_id"],
    data["marketing_profit"],
    color=COLORS["blue"]
)

ax.bar_label(
    bars,
    labels=[
        f"{v:,.0f}"
        for v in data["marketing_profit"]
    ],
    padding=5
)

ax.set_title("Top 10 Campaigns by Marketing Profit")
ax.set_xlabel("Marketing Profit")
ax.set_ylabel("Campaign ID")
ax.set_xlim(
    0,
    data["marketing_profit"].max() * 1.25
)

save_chart("07_top_10_profitable_campaigns.png")

# ----------------------------------------------------------
# CHART 8: BUDGET OPTIMIZATION COMPARISON
# ----------------------------------------------------------

data = scenario[
    scenario["metric"].isin([
        "Total Revenue",
        "Marketing Profit"
    ])
].copy()

x = np.arange(len(data))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))

baseline_bars = ax.bar(
    x - width / 2,
    data["baseline"],
    width,
    label="Baseline",
    color=COLORS["blue"]
)

scenario_bars = ax.bar(
    x + width / 2,
    data["scenario"],
    width,
    label="Illustrative Scenario",
    color=COLORS["green"]
)

ax.set_xticks(x)
ax.set_xticklabels(data["metric"])

ax.set_title(
    "Budget Optimization: Baseline vs Scenario"
)

ax.set_ylabel("Amount")
ax.legend()

ax.bar_label(
    baseline_bars,
    labels=[
        format_millions(v)
        for v in data["baseline"]
    ],
    padding=3
)

ax.bar_label(
    scenario_bars,
    labels=[
        format_millions(v)
        for v in data["scenario"]
    ],
    padding=3
)

ax.set_ylim(
    0,
    max(
        data["baseline"].max(),
        data["scenario"].max()
    ) * 1.20
)

save_chart("08_budget_optimization_comparison.png")

# ----------------------------------------------------------
# 5. FINAL SUMMARY
# ----------------------------------------------------------

print("\n" + "=" * 65)
print("ALL 8 VISUALIZATIONS GENERATED SUCCESSFULLY")
print("=" * 65)

print(f"\nOutput Folder: {OUTPUT}")

print("\nNote:")
print("Marketing profit excludes non-advertising costs.")
print("Budget scenario assumes constant historical ROAS.")
