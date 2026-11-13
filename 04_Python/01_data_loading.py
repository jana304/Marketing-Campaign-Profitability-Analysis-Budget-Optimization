
# ==========================================================
# MARKETING_PROFITABILITY
# Phase 22: Python Data Loading and Validation
# File: 01_data_loading.py
# ==========================================================

from pathlib import Path
import pandas as pd


# ----------------------------------------------------------
# 1. PROJECT PATH CONFIGURATION
# ----------------------------------------------------------

# Find the project root automatically
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "01_Dataset" / "raw"

print("=" * 60)
print("MARKETING PROFITABILITY - DATA LOADING")
print("=" * 60)

print(f"\nProject Directory: {PROJECT_ROOT}")
print(f"Dataset Directory: {DATA_FOLDER}")


# ----------------------------------------------------------
# 2. LOAD CSV DATASETS
# ----------------------------------------------------------

campaigns = pd.read_csv(DATA_FOLDER / "campaigns.csv")

daily_spend = pd.read_csv(DATA_FOLDER / "daily_spend.csv")

leads = pd.read_csv(DATA_FOLDER / "leads.csv")

conversions = pd.read_csv(DATA_FOLDER / "conversions.csv")

print("\nAll four datasets loaded successfully!")


# ----------------------------------------------------------
# 3. DISPLAY DATASET DIMENSIONS
# ----------------------------------------------------------

datasets = {
    "Campaigns": campaigns,
    "Daily Spend": daily_spend,
    "Leads": leads,
    "Conversions": conversions
}

print("\nDATASET OVERVIEW")
print("-" * 60)

for name, df in datasets.items():
    print(
        f"{name:<20} Rows: {len(df):>8,} "
        f"Columns: {df.shape[1]}"
    )


# ----------------------------------------------------------
# 4. DISPLAY FIRST FIVE RECORDS
# ----------------------------------------------------------

for name, df in datasets.items():
    print(f"\n{name.upper()} - FIRST 5 ROWS")
    print("-" * 60)
    print(df.head().to_string(index=False))


# ----------------------------------------------------------
# 5. CHECK MISSING VALUES
# ----------------------------------------------------------

print("\nMISSING VALUE VALIDATION")
print("-" * 60)

for name, df in datasets.items():
    missing = df.isnull().sum().sum()
    print(f"{name:<20} Missing Values: {missing}")


# ----------------------------------------------------------
# 6. CHECK DUPLICATE PRIMARY KEYS
# ----------------------------------------------------------

primary_keys = {
    "Campaigns": "campaign_id",
    "Daily Spend": "spend_id",
    "Leads": "lead_id",
    "Conversions": "conversion_id"
}

print("\nPRIMARY KEY DUPLICATE VALIDATION")
print("-" * 60)

for name, key in primary_keys.items():
    duplicate_count = datasets[name][key].duplicated().sum()

    print(
        f"{name:<20} Duplicate Keys: {duplicate_count}"
    )


# ----------------------------------------------------------
# 7. VERIFY EXPECTED RECORD COUNTS
# ----------------------------------------------------------

expected_counts = {
    "Campaigns": 120,
    "Daily Spend": 11240,
    "Leads": 261684,
    "Conversions": 39696
}

print("\nDATASET RECORD COUNT VALIDATION")
print("-" * 60)

all_valid = True

for name, expected in expected_counts.items():

    actual = len(datasets[name])

    status = "PASS" if actual == expected else "FAIL"

    if actual != expected:
        all_valid = False

    print(
        f"{name:<20} "
        f"Expected: {expected:>8,} "
        f"Actual: {actual:>8,} "
        f"Status: {status}"
    )


# ----------------------------------------------------------
# 8. FINAL VALIDATION SUMMARY
# ----------------------------------------------------------

print("\n" + "=" * 60)

if all_valid:
    print("SUCCESS: ALL DATASET RECORD COUNTS MATCH SQL")
else:
    print("WARNING: DATASET RECORD COUNT MISMATCH FOUND")

print("=" * 60)
