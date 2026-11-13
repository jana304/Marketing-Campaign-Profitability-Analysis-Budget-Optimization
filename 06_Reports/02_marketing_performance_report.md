# MARKETING_PROFITABILITY
## Marketing Performance & Customer Acquisition Analysis Report

### 1. Report Overview

This report evaluates marketing performance across five advertising channels: Affiliate, Paid Search, Paid Social, Display, and Video.

The analysis focuses on advertising efficiency, lead generation, customer acquisition, attributed revenue, and marketing profitability.

The results were developed using Microsoft Excel, MySQL, and Python as part of the Marketing Campaign Profitability Analysis & Budget Optimization portfolio project.

### 2. Analysis Objectives

The primary objectives are to:

1. Compare advertising expenditure across marketing channels.
2. Evaluate campaign engagement using click-through rate (CTR) and cost per click (CPC).
3. Measure lead generation and conversion performance.
4. Compare acquisition costs across channels.
5. Identify the highest-performing channels based on revenue, profit, and ROAS.
6. Highlight opportunities for campaign-level improvement.

### 3. Dataset Summary

| Dataset | Total Records | Purpose |
|---|---:|---|
| Campaigns | 120 | Campaign configuration, channel, objective, and budget |
| Daily Spend | 11,240 | Impressions, clicks, and advertising spend |
| Leads | 261,684 | Lead acquisition and scoring |
| Conversions | 39,696 | Conversion events and attributed revenue |

The datasets are linked through campaign IDs and lead IDs.

### 4. Overall Marketing Performance

| Metric | Value |
|---|---:|
| Total Marketing Spend | 4,523,050.02 |
| Total Attributed Revenue | 21,561,839.01 |
| Marketing Profit | 17,038,788.99 |
| Overall ROAS | 4.77x |
| Marketing ROI | 376.71% |
| Marketing Profit Margin | 79.02% |
| Total Leads | 261,684 |
| Total Conversions | 39,696 |
| Lead Conversion Rate | 15.17% |
| Advertising Cost per Conversion | 113.94 |

Marketing profit represents attributed revenue less advertising spend, not accounting net profit.

### 5. Advertising Engagement Analysis

| Marketing Channel | Advertising Spend | CTR (%) | CPC |
|---|---:|---:|---:|
| Paid Search | 897,091.53 | 3.49 | 0.52 |
| Affiliate | 857,835.07 | 2.50 | 0.36 |
| Paid Social | 984,731.88 | 1.79 | 0.61 |
| Video | 828,094.54 | 0.89 | 1.68 |
| Display | 955,297.00 | 0.60 | 1.09 |

**Key observations**

- Paid Search achieved the highest CTR at 3.49%, indicating the strongest click engagement relative to impressions.
- Affiliate recorded the lowest CPC at 0.36, demonstrating efficient traffic acquisition.
- Paid Social achieved a moderate CTR of 1.79% and CPC of 0.61.
- Display had the lowest CTR at 0.60%.
- Video had the highest CPC at 1.68, indicating relatively expensive traffic acquisition.

CTR and CPC should be interpreted alongside campaign objectives, conversion quality, and profitability rather than in isolation.

### 6. Customer Acquisition Performance

| Channel | Leads | Conversions | Conversion Rate (%) | Cost per Conversion |
|---|---:|---:|---:|---:|
| Affiliate | 67,849 | 10,352 | 15.26 | 82.87 |
| Paid Search | 65,268 | 10,019 | 15.35 | 89.54 |
| Paid Social | 57,619 | 8,648 | 15.01 | 113.87 |
| Display | 45,149 | 6,744 | 14.94 | 141.65 |
| Video | 25,799 | 3,933 | 15.24 | 210.55 |

**Key observations**

Affiliate generated the highest lead and conversion volumes while maintaining the lowest advertising cost per conversion.

Paid Search achieved the highest lead conversion rate at 15.35%, narrowly outperforming the other channels.

Paid Social ranked third in conversion volume and cost efficiency.

Display and Video incurred higher advertising costs per conversion, particularly Video at 210.55.

The cost-per-conversion metric is used as a customer acquisition cost proxy. It should not be interpreted as the cost of acquiring a unique new customer unless the conversion events represent distinct new customers.

### 7. Revenue and Profitability Analysis

| Channel | Revenue | Marketing Profit | ROAS |
|---|---:|---:|---:|
| Affiliate | 5,610,700.73 | 4,752,865.66 | 6.54x |
| Paid Search | 5,439,329.35 | 4,542,237.82 | 6.06x |
| Paid Social | 4,690,137.28 | 3,705,405.40 | 4.76x |
| Display | 3,734,117.43 | 2,778,820.43 | 3.91x |
| Video | 2,087,554.22 | 1,259,459.68 | 2.52x |

All five channels generated positive marketing profit under the project's attributed-revenue-minus-ad-spend definition.

Affiliate ranked first in revenue, marketing profit, and ROAS.

Paid Search ranked second in these profitability measures.

Paid Social generated substantial revenue and profit, although its ROAS was below Affiliate and Paid Search.

Display and Video produced lower advertising returns and warrant further efficiency analysis.

### 8. Channel Performance Rankings

| Channel | CTR Rank | CPC Rank | ROAS Rank | Acquisition Cost Rank |
|---|---:|---:|---:|---:|
| Affiliate | 2 | 1 | 1 | 1 |
| Paid Search | 1 | 2 | 2 | 2 |
| Paid Social | 3 | 3 | 3 | 3 |
| Display | 5 | 4 | 4 | 4 |
| Video | 4 | 5 | 5 | 5 |

For CPC and acquisition cost, rank 1 indicates the lowest cost. For CTR and ROAS, rank 1 indicates the highest performance.

Affiliate and Paid Search consistently performed well across multiple efficiency metrics.

### 9. Campaign-Level Analysis

The project includes 120 marketing campaigns.

Campaign-level profitability analysis evaluates:

- Total advertising spend.
- Attributed revenue.
- Marketing profit.
- ROAS.
- Advertising cost per conversion.
- Budget utilization.

The Python analysis generates the following supporting files:

- `campaign_marketing_kpis.csv`
- `campaign_profitability.csv`
- `top_10_profitable_campaigns.csv`
- `bottom_10_profit_campaigns.csv`

These outputs can be used to identify high-performing campaigns and investigate campaigns with weaker financial efficiency.

A campaign with high ROAS may not necessarily generate the highest absolute profit, so both measures should be considered.

### 10. Supporting Visualizations

The following charts are available in the `05_Visualizations` folder:

| Visualization | File |
|---|---|
| Revenue by Marketing Channel | `01_revenue_by_channel.png` |
| ROAS by Marketing Channel | `02_roas_by_channel.png` |
| Monthly Spend vs Revenue | `03_monthly_spend_vs_revenue.png` |
| Cost per Conversion | `04_cost_per_conversion.png` |
| Lead Conversion Rate | `05_conversion_rate_by_channel.png` |
| Marketing Profit by Channel | `06_marketing_profit_by_channel.png` |
| Top 10 Profitable Campaigns | `07_top_10_profitable_campaigns.png` |

The monthly spend and revenue chart presents two trends using their respective transaction dates. It should not be interpreted as a same-cohort return calculation without further attribution analysis.

### 11. Key Business Insights

**Insight 1: Affiliate is the leading efficiency channel.**

Affiliate delivered 6.54x ROAS and the lowest cost per conversion at 82.87. Its combination of revenue generation and acquisition efficiency supports further evaluation for budget expansion.

**Insight 2: Paid Search attracts relatively high-engagement traffic.**

Paid Search achieved the highest CTR and lead conversion rate, while delivering 6.06x ROAS.

**Insight 3: Paid Social offers optimization potential.**

Paid Social generated approximately 4.69 million in attributed revenue. Improvements to targeting, creatives, and campaign structure may increase efficiency.

**Insight 4: Display has weaker engagement and acquisition efficiency.**

Display recorded the lowest CTR and a relatively high cost per conversion, suggesting opportunities to review placement quality, audiences, and campaign objectives.

**Insight 5: Video requires further investigation.**

Video recorded the lowest ROAS and highest advertising cost per conversion. Before changing its budget, the business should examine whether brand awareness or assisted conversions are important objectives.

### 12. Business Recommendations

1. Evaluate incremental budget expansion for Affiliate and Paid Search through controlled tests.
2. Monitor conversion quality and marginal returns rather than relying exclusively on historical ROAS.
3. Optimize Paid Social campaigns through audience segmentation and creative testing.
4. Review Display placements and campaign-level profitability.
5. Assess Video performance using both direct-response and brand-related objectives.
6. Track CTR, CPC, conversion rate, cost per conversion, ROAS, and marketing profit through regular reporting.

### 13. Analysis Limitations

The analysis has several important limitations:

- Revenue is attributed to recorded conversions; it is not necessarily incremental revenue caused by advertising.
- Marketing profit excludes product costs, fulfillment costs, salaries, taxes, and other operating expenses.
- Cost per conversion is not necessarily the cost of acquiring a unique customer.
- Historical channel performance does not guarantee the same returns from future budget changes.
- Channel comparisons may be influenced by campaign objectives, audience characteristics, attribution methods, and seasonality.

### 14. Conclusion

The analysis identifies Affiliate and Paid Search as the strongest marketing channels based on historical ROAS and acquisition efficiency.

Paid Social provides opportunities for continued optimization, while Display and Video should be investigated for improvements in efficiency.

By combining engagement, acquisition, revenue, and profitability metrics, the project demonstrates how marketing analytics can support evidence-based decisions and structured campaign performance management.