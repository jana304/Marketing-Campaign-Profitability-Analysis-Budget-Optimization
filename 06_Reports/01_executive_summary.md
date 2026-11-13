# MARKETING_PROFITABILITY
## Marketing Campaign Profitability Analysis & Budget Optimization

### 1. Executive Summary

This project analyzes marketing campaign performance to evaluate advertising efficiency, customer acquisition, attributed revenue, profitability, and opportunities for budget optimization.

The analysis uses campaign, advertising spend, lead, and conversion datasets to understand which marketing channels deliver the strongest financial returns and where marketing budgets may be used more effectively.

The project combines **Microsoft Excel, MySQL, Python, Pandas, Matplotlib, and Seaborn** to perform data validation, exploratory analysis, KPI calculations, business reporting, and data visualization.

The findings are based on the project's campaign datasets and represent a portfolio case study rather than verified performance for a named real-world company.

### 2. Business Problem

Marketing teams invest across multiple advertising channels, but higher spending does not necessarily generate higher returns.

Without integrated campaign and conversion analysis, businesses may struggle to:

- Identify the most profitable advertising channels.
- Measure customer acquisition efficiency.
- Compare campaign spending against attributed revenue.
- Detect inefficient marketing investments.
- Develop evidence-based budget allocation strategies.

**Primary business question:**

How can marketing performance data be used to improve advertising profitability and inform budget allocation decisions?

### 3. Dataset Overview

The project analyzes four related datasets.

| Dataset | Records | Description |
|---|---:|---|
| Campaigns | 120 | Campaign information, channels, objectives, and budgets |
| Daily Spend | 11,240 | Advertising spending, impressions, and clicks |
| Leads | 261,684 | Lead generation and acquisition information |
| Conversions | 39,696 | Conversion events and attributed revenue |

The datasets are connected using campaign IDs and lead IDs.

### 4. Key Performance Indicators

| KPI | Result |
|---|---:|
| Total Marketing Spend | 4,523,050.02 |
| Total Attributed Revenue | 21,561,839.01 |
| Marketing Profit | 17,038,788.99 |
| Return on Ad Spend (ROAS) | 4.77x |
| Marketing ROI | 376.71% |
| Marketing Profit Margin | 79.02% |
| Total Leads | 261,684 |
| Total Conversions | 39,696 |
| Lead Conversion Rate | 15.17% |
| Advertising Cost per Conversion | 113.94 |

*Marketing profit is calculated as attributed revenue minus advertising spend. It does not represent accounting net profit because other business costs are excluded.*

### 5. Marketing Channel Performance

| Channel | Marketing Spend | Attributed Revenue | Marketing Profit | ROAS |
|---|---:|---:|---:|---:|
| Affiliate | 857,835.07 | 5,610,700.73 | 4,752,865.66 | 6.54x |
| Paid Search | 897,091.53 | 5,439,329.35 | 4,542,237.82 | 6.06x |
| Paid Social | 984,731.88 | 4,690,137.28 | 3,705,405.40 | 4.76x |
| Display | 955,297.00 | 3,734,117.43 | 2,778,820.43 | 3.91x |
| Video | 828,094.54 | 2,087,554.22 | 1,259,459.68 | 2.52x |

### 6. Key Business Findings

**Finding 1: Affiliate marketing generated the strongest advertising returns.**

Affiliate achieved the highest ROAS at 6.54x and generated approximately 4.75 million in marketing profit. Its advertising cost per conversion was also the lowest among the five channels.

**Finding 2: Paid Search demonstrated strong acquisition efficiency.**

Paid Search achieved 6.06x ROAS and the highest lead conversion rate at approximately 15.35%. It is a promising candidate for controlled budget expansion.

**Finding 3: Paid Social generated substantial revenue but had lower efficiency than the two leading channels.**

Paid Social produced approximately 4.69 million in attributed revenue and 3.71 million in marketing profit, with ROAS of 4.76x. Campaign-level optimization may improve performance.

**Finding 4: Display advertising requires efficiency improvements.**

Display generated positive marketing profit but achieved a lower ROAS of 3.91x and a higher advertising cost per conversion than Affiliate, Paid Search, and Paid Social.

**Finding 5: Video advertising recorded the weakest financial efficiency.**

Video achieved the lowest ROAS at 2.52x and the highest advertising cost per conversion at approximately 210.55. This makes it a priority for further investigation.

**Finding 6: Acquisition efficiency differs substantially across channels.**

Affiliate's advertising cost per conversion was approximately 82.87, compared with 210.55 for Video. This indicates significant differences in acquisition efficiency across the channel mix.

### 7. Budget Optimization Opportunity

The project evaluates an illustrative scenario involving a 10% reduction in Video advertising spend.

The released budget of approximately 82,809.45 is redistributed as follows:

| Destination | Allocation | Amount |
|---|---:|---:|
| Affiliate | 60% | 49,685.67 |
| Paid Search | 40% | 33,123.78 |
| Total | 100% | 82,809.45 |

The scenario maintains the same total advertising spend.

The estimated impact is calculated using historical channel ROAS, assuming returns remain constant as budgets change.

This assumption is a modeling simplification. The scenario is not a guaranteed financial outcome or causal prediction.

### 8. Business Recommendations

1. Evaluate controlled budget increases for Affiliate and Paid Search, subject to capacity and incremental-return testing.
2. Improve Paid Social targeting, creative performance, and campaign-level conversion efficiency.
3. Review underperforming Display campaigns and investigate audience, placement, and conversion quality.
4. Investigate Video campaign objectives and attribution before reducing spend, especially where brand awareness may be a goal.
5. Monitor ROAS, cost per conversion, conversion rates, and marketing profit regularly.
6. Test budget reallocations incrementally rather than assuming historical ROAS will remain unchanged.

### 9. Tools and Technologies

| Tool | Purpose |
|---|---|
| Microsoft Excel | Data analysis, KPI calculations, and charts |
| MySQL | Relational database, validation, joins, and advanced SQL analysis |
| Python | Data processing and analytical automation |
| Pandas and NumPy | Data manipulation and metric calculations |
| Matplotlib and Seaborn | Marketing performance visualizations |
| Visual Studio Code | Project development and file organization |

### 10. Project Deliverables

The project includes:

- Four source datasets and cleaned data outputs.
- An Excel marketing profitability analysis workbook.
- Seven SQL scripts covering validation, performance, acquisition, profitability, advanced analysis, and budget optimization.
- Python scripts for data loading, cleaning, exploratory analysis, KPI calculations, acquisition, profitability, optimization, and visualizations.
- Eight marketing analytics charts.
- Business reports, recommendations, and project documentation.

### 11. Conclusion

The analysis identifies Affiliate and Paid Search as the strongest channels based on historical ROAS and acquisition efficiency, while Video and Display offer opportunities for further investigation.

The project demonstrates how integrated Excel, SQL, and Python analysis can support marketing performance measurement and structured budget decision-making.

Future optimization should use controlled experiments, incremental performance measurement, and business constraints before implementing substantial budget changes.done'