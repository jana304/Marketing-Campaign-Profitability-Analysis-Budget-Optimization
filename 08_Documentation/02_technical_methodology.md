# MARKETING_PROFITABILITY
## Technical Methodology & Analytical Workflow

### 1. Introduction

This document explains the technical approach used in the Marketing Campaign Profitability Analysis & Budget Optimization project.

The workflow combines Excel, MySQL, and Python to validate marketing data, calculate performance indicators, analyze profitability, and evaluate advertising budget allocation.

### 2. Data Sources

The project contains four related datasets.

| Dataset | Records | Primary Identifier |
|---|---:|---|
| Campaigns | 120 | campaign_id |
| Daily Spend | 11,240 | spend_id |
| Leads | 261,684 | lead_id |
| Conversions | 39,696 | conversion_id |

**Data Relationships**

- Campaigns → Daily Spend: `campaign_id`
- Campaigns → Leads: `campaign_id`
- Leads → Conversions: `lead_id`

These relationships allow advertising expenditure to be analyzed alongside lead generation, conversions, and attributed revenue.

### 3. Data Validation

Data validation was performed using MySQL and Python.

The checks included:

- Record count verification.
- Missing and null value checks.
- Duplicate primary identifier checks.
- Invalid numeric value detection.
- Foreign key relationship validation.
- Date and data type consistency checks.

The SQL validation queries are available in `03_SQL/02_data_validation.sql`.

### 4. Data Cleaning

Python and Pandas were used to prepare the datasets for analysis.

The cleaning workflow included:

1. Loading raw CSV datasets.
2. Standardizing column values and data types.
3. Converting date fields into consistent formats.
4. Removing duplicate primary identifiers.
5. Checking missing and invalid numeric values.
6. Validating relationships between datasets.
7. Exporting processed CSV files.

The cleaned datasets are stored in `01_Dataset/processed/`.

Invalid values and relationship issues are reported for review rather than automatically corrected without supporting information.

### 5. SQL Analysis

MySQL was used for relational analysis and KPI calculations.

| SQL Script | Purpose |
|---|---|
| 01_create_tables.sql | Create database tables |
| 02_data_validation.sql | Validate imported data |
| 03_marketing_performance.sql | Analyze spending, CTR, and CPC |
| 04_customer_acquisition.sql | Evaluate leads and conversions |
| 05_revenue_profitability.sql | Calculate revenue, profit, and ROAS |
| 06_advanced_analysis.sql | Perform advanced campaign analysis |
| 07_budget_optimization.sql | Evaluate channel budget efficiency |

The SQL analysis uses joins, aggregations, conditional calculations, ranking functions, and a campaign performance view.

### 6. Python Analytical Workflow

The project includes eight Python analysis scripts.

| Script | Function |
|---|---|
| 01_data_loading.py | Load and inspect datasets |
| 02_data_cleaning.py | Clean and validate records |
| 03_exploratory_analysis.py | Perform exploratory analysis |
| 04_marketing_kpis.py | Calculate marketing KPIs |
| 05_customer_acquisition.py | Analyze lead and conversion performance |
| 06_profitability_analysis.py | Evaluate campaign profitability |
| 07_budget_optimization.py | Model budget allocation scenarios |
| 08_data_visualizations.py | Generate analytical charts |

The scripts generate CSV outputs and PNG visualizations for reporting.

### 7. Marketing KPI Formulas

**Click-Through Rate (CTR)**

CTR (%) = (Total Clicks / Total Impressions) × 100

**Cost per Click (CPC)**

CPC = Total Advertising Spend / Total Clicks

**Cost per Lead (CPL)**

CPL = Total Advertising Spend / Total Leads

**Lead Conversion Rate**

Conversion Rate (%) = (Total Conversions / Total Leads) × 100

**Advertising Cost per Conversion**

Cost per Conversion = Total Advertising Spend / Total Conversions

**Return on Ad Spend (ROAS)**

ROAS = Total Attributed Revenue / Total Advertising Spend

**Marketing Profit**

Marketing Profit = Attributed Revenue − Advertising Spend

**Marketing ROI**

Marketing ROI (%) = (Marketing Profit / Advertising Spend) × 100

**Marketing Profit Margin**

Marketing Profit Margin (%) = (Marketing Profit / Attributed Revenue) × 100

All division calculations should handle zero denominators safely.

Marketing profit excludes costs outside advertising expenditure.

### 8. Customer Acquisition Analysis

Customer acquisition analysis evaluates:

- Lead volume by campaign and channel.
- Conversion volume and conversion rates.
- Advertising cost per conversion.
- Lead source distribution.
- Lead score distribution.
- Monthly lead and conversion trends.
- Time between lead creation and conversion.

Cost per conversion is used as an acquisition efficiency proxy and does not necessarily represent the cost of acquiring a unique new customer.

### 9. Profitability Analysis

Campaign and channel profitability were evaluated using attributed revenue and advertising expenditure.

The main financial indicators include:

- Total attributed revenue.
- Total advertising spend.
- Marketing profit.
- ROAS.
- Marketing ROI.
- Marketing profit margin.

The analysis also identifies the top and bottom campaigns based on marketing profit.

Campaign-level and channel-level results are exported as CSV files for reporting.

### 10. Budget Optimization Methodology

The project evaluates an illustrative scenario involving a 10% reduction in Video advertising spend.

The released budget is redistributed as follows:

| Channel | Budget Adjustment |
|---|---:|
| Video | -82,809.45 |
| Affiliate | +49,685.67 |
| Paid Search | +33,123.78 |
| Net Change | 0.00 |

The scenario calculates estimated revenue using historical channel ROAS.

**Scenario Revenue = Scenario Spend × Historical ROAS**

**Scenario Marketing Profit = Scenario Revenue − Scenario Spend**

The model assumes historical ROAS remains constant after budget reallocation.

This is a simplified scenario analysis, not a causal forecast. Actual incremental returns require testing.

### 11. Data Visualization

Matplotlib and Seaborn were used to create eight visualizations:

1. Revenue by Marketing Channel.
2. ROAS by Marketing Channel.
3. Monthly Spend vs Revenue.
4. Advertising Cost per Conversion.
5. Lead Conversion Rate by Channel.
6. Marketing Profit by Channel.
7. Top 10 Profitable Campaigns.
8. Budget Optimization Comparison.

Charts are saved in the `05_Visualizations/` directory.

### 12. Validation and Consistency

The analytical workflow includes comparisons between SQL and Python outputs.

Key validation points include:

- Dataset record counts.
- Total advertising spend.
- Total attributed revenue.
- Total conversions.
- Channel-level KPI calculations.
- Budget allocation totals.

Historical baseline totals are:

| Metric | Value |
|---|---:|
| Advertising Spend | 4,523,050.02 |
| Attributed Revenue | 21,561,839.01 |
| Marketing Profit | 17,038,788.99 |
| Total Conversions | 39,696 |

Small rounding differences may occur between displayed KPI values and calculations using full-precision data.

### 13. Technical Limitations

- Historical ROAS may not represent marginal advertising returns.
- Attributed revenue does not establish incremental revenue.
- Marketing profit excludes operating costs beyond advertising.
- Conversion counts may not represent unique customers.
- Campaign objectives and attribution methods can affect channel comparisons.
- Budget optimization estimates depend on simplifying assumptions.

### 14. Conclusion

The project follows a structured analytical workflow from raw data to business recommendations.

Excel supports spreadsheet analysis, MySQL enables relational queries, and Python automates cleaning, KPI calculations, profitability analysis, and visualizations.

The methodology demonstrates practical data analytics skills while recognizing the limitations of historical marketing performance and scenario modeling.