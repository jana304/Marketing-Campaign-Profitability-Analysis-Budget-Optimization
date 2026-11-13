# MARKETING_PROFITABILITY
## Dataset Dictionary & Database Schema

### 1. Overview

This document describes the four datasets used in the Marketing Campaign Profitability Analysis & Budget Optimization project.

The datasets contain campaign details, advertising spend, lead information, and conversion records.

### 2. Dataset Summary

| Dataset | Records | Primary Key |
|---|---:|---|
| campaigns.csv | 120 | campaign_id |
| daily_spend.csv | 11,240 | spend_id |
| leads.csv | 261,684 | lead_id |
| conversions.csv | 39,696 | conversion_id |

### 3. Campaigns Dataset

**File:** `01_Dataset/raw/campaigns.csv`

| Column | Data Type | Description |
|---|---|---|
| campaign_id | VARCHAR(20) | Unique campaign identifier |
| campaign_name | VARCHAR(150) | Marketing campaign name |
| channel | VARCHAR(50) | Advertising channel |
| objective | VARCHAR(50) | Campaign objective |
| start_date | DATE | Campaign start date |
| end_date | DATE | Campaign end date |
| budget | DECIMAL(12,2) | Allocated campaign budget |

**Primary Key:** `campaign_id`

### 4. Daily Spend Dataset

**File:** `01_Dataset/raw/daily_spend.csv`

| Column | Data Type | Description |
|---|---|---|
| spend_id | VARCHAR(20) | Unique spend record identifier |
| campaign_id | VARCHAR(20) | Related campaign identifier |
| spend_date | DATE | Advertising expenditure date |
| impressions | INT | Number of advertisement impressions |
| clicks | INT | Number of advertisement clicks |
| spend | DECIMAL(12,2) | Advertising expenditure |

**Primary Key:** `spend_id`

**Foreign Key:** `campaign_id` references `campaigns.campaign_id`

### 5. Leads Dataset

**File:** `01_Dataset/raw/leads.csv`

| Column | Data Type | Description |
|---|---|---|
| lead_id | VARCHAR(20) | Unique lead identifier |
| campaign_id | VARCHAR(20) | Campaign associated with the lead |
| created_at | DATE/DATETIME | Lead creation date or timestamp |
| lead_source | VARCHAR | Source of the lead |
| lead_score | Numeric | Lead scoring value |

**Primary Key:** `lead_id`

**Foreign Key:** `campaign_id` references `campaigns.campaign_id`

*The exact SQL types and lengths for `lead_source` and `lead_score` should be confirmed against the table creation script.*

### 6. Conversions Dataset

**File:** `01_Dataset/raw/conversions.csv`

| Column | Data Type | Description |
|---|---|---|
| conversion_id | VARCHAR(20) | Unique conversion identifier |
| lead_id | VARCHAR(20) | Related lead identifier |
| converted_at | DATE | Conversion date |
| conversion_type | VARCHAR(50) | Type of conversion event |
| revenue | DECIMAL(12,2) | Revenue attributed to conversion |

**Primary Key:** `conversion_id`

**Foreign Key:** `lead_id` references `leads.lead_id`

### 7. Database Relationships

The project uses three main relationships:

- `campaigns.campaign_id` → `daily_spend.campaign_id`
- `campaigns.campaign_id` → `leads.campaign_id`
- `leads.lead_id` → `conversions.lead_id`

These relationships enable campaign-level and channel-level analysis.

Spend and conversions should be aggregated to the appropriate level before joining to avoid duplicating financial totals.

### 8. Derived Marketing Metrics

| Metric | Formula |
|---|---|
| CTR (%) | Clicks / Impressions × 100 |
| CPC | Advertising Spend / Clicks |
| CPL | Advertising Spend / Leads |
| Conversion Rate (%) | Conversions / Leads × 100 |
| Cost per Conversion | Advertising Spend / Conversions |
| ROAS | Attributed Revenue / Advertising Spend |
| Marketing Profit | Attributed Revenue − Advertising Spend |
| Marketing ROI (%) | Marketing Profit / Advertising Spend × 100 |
| Marketing Margin (%) | Marketing Profit / Attributed Revenue × 100 |

Zero denominators must be handled safely.

### 9. Data Quality Validation

The data validation process checks:

- Missing values.
- Duplicate primary identifiers.
- Invalid numeric values.
- Orphan foreign keys.
- Dataset record counts.
- Date formatting and consistency.

The validation queries are available in `03_SQL/02_data_validation.sql`.

### 10. Data Limitations

- Revenue represents attributed conversion revenue.
- Conversion events may not represent unique customers.
- Marketing profit excludes non-advertising business costs.
- Campaign performance may vary by objectives and attribution methods.
- The exact data-generation provenance should be documented before public release.

### 11. Conclusion

The four datasets provide a relational foundation for evaluating marketing engagement, lead generation, conversion efficiency, attributed revenue, profitability, and budget optimization.

The data dictionary supports reproducibility and helps analysts understand the structure and meaning of the project data.