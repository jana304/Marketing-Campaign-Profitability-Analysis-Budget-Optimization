
# ==========================================================
# MARKETING_PROFITABILITY
# Phase 23: Data Cleaning and Preprocessing
# File: 02_data_cleaning.py
# ==========================================================

from pathlib import Path
import pandas as pd

# ----------------------------------------------------------
# 1. PROJECT PATHS
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FOLDER = PROJECT_ROOT / "01_Dataset" / "raw"
PROCESSED_FOLDER = PROJECT_ROOT / "01_Dataset" / "processed"

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("MARKETING PROFITABILITY - DATA CLEANING")
print("=" * 60)

# ----------------------------------------------------------
# 2. LOAD DATASETS
# ----------------------------------------------------------

datasets = {
    "campaigns": pd.read_csv(RAW_FOLDER / "campaigns.csv"),
    "daily_spend": pd.read_csv(RAW_FOLDER / "daily_spend.csv"),
    "leads": pd.read_csv(RAW_FOLDER / "leads.csv"),
    "conversions": pd.read_csv(RAW_FOLDER / "conversions.csv")
}

print("\nAll datasets loaded successfully.")

# ----------------------------------------------------------
# 3. REMOVE DUPLICATE PRIMARY KEYS
# ----------------------------------------------------------

primary_keys = {
    "campaigns": "campaign_id",
    "daily_spend": "spend_id",
    "leads": "lead_id",
    "conversions": "conversion_id"
}

for name, df in datasets.items():

    original_count = len(df)

    df = df.drop_duplicates(
        subset=[primary_keys[name]],
        keep="first"
    ).copy()

    datasets[name] = df

    removed = original_count - len(df)

    print(f"{name}: {removed} duplicate records removed")

# ----------------------------------------------------------
# 4. STANDARDIZE TEXT COLUMNS
# ----------------------------------------------------------

for name, df in datasets.items():

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    datasets[name] = df

print("\nText columns standardized.")

# ----------------------------------------------------------
# 5. CONVERT DATE COLUMNS
# ----------------------------------------------------------

date_columns = {
    "campaigns": ["start_date", "end_date"],
    "daily_spend": ["spend_date"],
    "leads": ["created_at"],
    "conversions": ["converted_at"]
}

for name, columns in date_columns.items():

    for column in columns:
        datasets[name][column] = pd.to_datetime(
            datasets[name][column],
            errors="coerce"
        )

print("Date columns converted successfully.")

# ----------------------------------------------------------
# 6. CONVERT NUMERIC COLUMNS
# ----------------------------------------------------------

numeric_columns = {
    "campaigns": ["budget"],
    "daily_spend": ["impressions", "clicks", "spend"],
    "leads": ["lead_score"],
    "conversions": ["revenue"]
}

for name, columns in numeric_columns.items():

    for column in columns:
        datasets[name][column] = pd.to_numeric(
            datasets[name][column],
            errors="coerce"
        )

print("Numeric columns converted successfully.")

# ----------------------------------------------------------
# 7. CHECK MISSING VALUES
# ----------------------------------------------------------

print("\nMISSING VALUES AFTER TYPE CONVERSION")
print("-" * 60)

for name, df in datasets.items():

    missing = df.isna().sum().sum()

    print(f"{name:<20} Missing Values: {missing}")

# ----------------------------------------------------------
# 8. VALIDATE BUSINESS RULES
# ----------------------------------------------------------

print("\nBUSINESS RULE VALIDATION")
print("-" * 60)

campaigns = datasets["campaigns"]
daily_spend = datasets["daily_spend"]
leads = datasets["leads"]
conversions = datasets["conversions"]

checks = {
    "Negative campaign budgets":
        (campaigns["budget"] < 0).sum(),

    "Negative daily spend":
        (daily_spend["spend"] < 0).sum(),

    "Negative impressions":
        (daily_spend["impressions"] < 0).sum(),

    "Negative clicks":
        (daily_spend["clicks"] < 0).sum(),

    "Clicks greater than impressions":
        (daily_spend["clicks"] >
         daily_spend["impressions"]).sum(),

    "Lead scores outside 0-100":
        (~leads["lead_score"].between(0, 100)).sum(),

    "Negative conversion revenue":
        (conversions["revenue"] < 0).sum(),

    "Campaign end before start":
        (campaigns["end_date"] <
         campaigns["start_date"]).sum()
}

for check, count in checks.items():
    print(f"{check:<38} {count}")

# ----------------------------------------------------------
# 9. CHECK REFERENTIAL INTEGRITY
# ----------------------------------------------------------

print("\nREFERENTIAL INTEGRITY")
print("-" * 60)

orphan_spend = (
    ~daily_spend["campaign_id"].isin(
        campaigns["campaign_id"]
    )
).sum()

orphan_leads = (
    ~leads["campaign_id"].isin(
        campaigns["campaign_id"]
    )
).sum()

orphan_conversions = (
    ~conversions["lead_id"].isin(
        leads["lead_id"]
    )
).sum()

print(f"Orphan daily spend records: {orphan_spend}")
print(f"Orphan lead records: {orphan_leads}")
print(f"Orphan conversion records: {orphan_conversions}")

# ----------------------------------------------------------
# 10. SAVE PROCESSED DATASETS
# ----------------------------------------------------------

for name, df in datasets.items():

    output_file = PROCESSED_FOLDER / f"{name}_cleaned.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file.name}")

# ----------------------------------------------------------
# 11. FINAL SUMMARY
# ----------------------------------------------------------

print("\nFINAL DATASET COUNTS")
print("-" * 60)

for name, df in datasets.items():
    print(f"{name:<20} {len(df):>8,} rows")

print("\n" + "=" * 60)
print("DATA CLEANING AND PREPROCESSING COMPLETED")
print("=" * 60)
