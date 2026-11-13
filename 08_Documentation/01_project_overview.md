# MARKETING_PROFITABILITY
## Project Overview & Business Requirements

### 1. Project Introduction

MARKETING_PROFITABILITY is an end-to-end Data Analyst portfolio project focused on evaluating marketing campaign performance, customer acquisition efficiency, attributed revenue, profitability, and advertising budget optimization.

The project integrates Microsoft Excel, MySQL, and Python to analyze marketing data and communicate actionable business insights.

### 2. Business Problem

Organizations invest in multiple digital marketing channels, but advertising expenditure does not always produce proportional financial returns.

Marketing teams need reliable analytical methods to identify efficient campaigns, evaluate acquisition costs, and make informed budget allocation decisions.

**Primary Business Question:**

How can marketing performance data help improve advertising profitability and support better budget allocation decisions?

### 3. Project Objectives

1. Analyze advertising expenditure and engagement.
2. Evaluate lead generation and conversion performance.
3. Calculate marketing KPIs such as CTR, CPC, ROAS, and conversion rate.
4. Measure campaign and channel profitability.
5. Identify opportunities to improve advertising efficiency.
6. Evaluate an illustrative budget optimization scenario.
7. Communicate findings through visualizations and reports.

### 4. Dataset Overview

The project uses four interconnected datasets.

| Dataset | Records | Purpose |
|---|---:|---|
| Campaigns | 120 | Campaign details and allocated budgets |
| Daily Spend | 11,240 | Advertising spend, impressions, and clicks |
| Leads | 261,684 | Lead acquisition information |
| Conversions | 39,696 | Conversion events and attributed revenue |

The datasets are connected using campaign IDs and lead IDs.

### 5. Marketing Channels

The analysis covers five advertising channels:

- Affiliate
- Paid Search
- Paid Social
- Display
- Video

These channels are compared using engagement, acquisition, revenue, and profitability metrics.

### 6. Technologies Used

| Technology | Purpose |
|---|---|
| Microsoft Excel | Marketing analysis and charts |
| MySQL | Data validation and SQL analysis |
| Python | Data cleaning and automation |
| Pandas and NumPy | Data processing and KPI calculations |
| Matplotlib and Seaborn | Data visualization |
| PowerPoint | Project presentation |
| VS Code | Development environment |

### 7. Key Performance Indicators

| KPI | Result |
|---|---:|
| Advertising Spend | 4,523,050.02 |
| Attributed Revenue | 21,561,839.01 |
| Marketing Profit | 17,038,788.99 |
| ROAS | 4.77x |
| Marketing ROI | 376.71% |
| Lead Conversion Rate | 15.17% |
| Advertising Cost per Conversion | 113.94 |

Marketing profit represents attributed revenue minus advertising spend and excludes other operating costs.

### 8. Key Business Findings

**Affiliate:** Highest ROAS at 6.54x and lowest advertising cost per conversion at 82.87.

**Paid Search:** Highest CTR at 3.49% and lead conversion rate at 15.35%.

**Paid Social:** Generated approximately 4.69 million in attributed revenue with a ROAS of 4.76x.

**Display:** Recorded the lowest CTR at 0.60% and a ROAS of 3.91x.

**Video:** Recorded the lowest ROAS at 2.52x and highest advertising cost per conversion at 210.55.

### 9. Budget Optimization Approach

The project evaluates an illustrative reallocation of 10% of Video advertising spend.

The released budget is distributed as follows:

| Channel | Budget Adjustment |
|---|---:|
| Video | -82,809.45 |
| Affiliate | +49,685.67 |
| Paid Search | +33,123.78 |
| Total Change | 0.00 |

The scenario assumes constant historical channel ROAS and should not be interpreted as a guaranteed financial forecast.

### 10. Project Deliverables

The project includes:

- Raw and cleaned marketing datasets.
- Excel profitability analysis workbook.
- SQL scripts for validation and marketing analysis.
- Python scripts for cleaning, KPIs, and optimization.
- Eight analytical visualizations.
- Four business reports.
- A 13-slide PowerPoint presentation.
- GitHub README and technical documentation.

### 11. Business Recommendations

- Evaluate controlled Affiliate and Paid Search expansion.
- Optimize Paid Social campaign performance.
- Investigate Display and Video efficiency.
- Monitor acquisition costs and ROAS regularly.
- Validate proposed budget changes through incremental testing.

### 12. Project Limitations

- Attributed revenue does not necessarily represent incremental revenue.
- Marketing profit excludes non-advertising costs.
- Cost per conversion is not necessarily unique customer acquisition cost.
- Historical ROAS may not remain constant as budgets change.

### 13. Conclusion

MARKETING_PROFITABILITY demonstrates an end-to-end analytics workflow combining Excel, SQL, and Python.

The project highlights how structured data analysis can support marketing performance measurement, profitability evaluation, and evidence-based budget decisions.