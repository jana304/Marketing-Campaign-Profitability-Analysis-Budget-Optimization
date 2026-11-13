# MARKETING_PROFITABILITY
## Marketing Budget Optimization & Scenario Analysis Report

### 1. Executive Overview

This report evaluates advertising budget allocation across five marketing channels and explores opportunities to improve marketing profitability through data-driven budget optimization.

The analysis combines historical marketing spend, attributed revenue, return on ad spend (ROAS), and advertising cost per conversion.

An illustrative scenario examines reallocating 10% of Video advertising spend to Affiliate and Paid Search while maintaining the same total advertising expenditure.

**Important:** The scenario assumes historical channel ROAS remains constant. It is a financial sensitivity analysis, not a causal forecast or a guaranteed business outcome.

### 2. Business Objective

The primary objective is to identify opportunities to improve advertising returns without increasing the total marketing budget.

The analysis addresses three business questions:

1. Which marketing channels currently generate the strongest financial returns?
2. Which channels warrant further investigation for budget efficiency improvements?
3. How might a budget reallocation affect attributed revenue and marketing profit under fixed historical ROAS assumptions?

### 3. Baseline Marketing Performance

| KPI | Historical Result |
|---|---:|
| Total Advertising Spend | 4,523,050.02 |
| Total Attributed Revenue | 21,561,839.01 |
| Marketing Profit | 17,038,788.99 |
| Overall ROAS | 4.77x |
| Marketing ROI | 376.71% |
| Marketing Profit Margin | 79.02% |

Marketing profit is defined as attributed revenue minus advertising spend. It excludes other business operating costs.

### 4. Historical Channel Performance

| Channel | Advertising Spend | Attributed Revenue | Marketing Profit | ROAS |
|---|---:|---:|---:|---:|
| Affiliate | 857,835.07 | 5,610,700.73 | 4,752,865.66 | 6.54x |
| Paid Search | 897,091.53 | 5,439,329.35 | 4,542,237.82 | 6.06x |
| Paid Social | 984,731.88 | 4,690,137.28 | 3,705,405.40 | 4.76x |
| Display | 955,297.00 | 3,734,117.43 | 2,778,820.43 | 3.91x |
| Video | 828,094.54 | 2,087,554.22 | 1,259,459.68 | 2.52x |

Affiliate and Paid Search generated the highest historical ROAS, while Video generated the lowest.

All five channels produced positive marketing profit under the project's calculation method.

### 5. Acquisition Efficiency Comparison

| Channel | Conversions | Advertising Cost per Conversion | Efficiency Rank |
|---|---:|---:|---:|
| Affiliate | 10,352 | 82.87 | 1 |
| Paid Search | 10,019 | 89.54 | 2 |
| Paid Social | 8,648 | 113.87 | 3 |
| Display | 6,744 | 141.65 | 4 |
| Video | 3,933 | 210.55 | 5 |

Affiliate and Paid Search achieved the lowest advertising cost per conversion.

Video had the highest cost per conversion, suggesting that its direct-response efficiency should be investigated before making future budget decisions.

Cost per conversion is used as an acquisition-cost proxy and does not necessarily represent the cost of acquiring a unique new customer.

### 6. Budget Optimization Strategy

The historical performance analysis suggests the following areas for evaluation.

| Channel | Historical ROAS | Proposed Strategy |
|---|---:|---|
| Affiliate | 6.54x | Evaluate for Expansion |
| Paid Search | 6.06x | Evaluate for Expansion |
| Paid Social | 4.76x | Maintain and Optimize |
| Display | 3.91x | Review Budget Efficiency |
| Video | 2.52x | Review Budget Efficiency |

These strategies are based on historical performance and should be validated using incremental-return testing, campaign objectives, and operational constraints.

### 7. Proposed Budget Reallocation Scenario

The scenario reduces Video advertising spend by 10% and reallocates the released amount to Affiliate and Paid Search.

**Step 1: Calculate the Video budget reduction**

Historical Video Spend = 828,094.54

Budget Reduction Percentage = 10%

Reallocated Budget = 828,094.54 × 10%

**Reallocated Budget = 82,809.45**

**Step 2: Redistribute the budget**

| Destination Channel | Allocation Percentage | Additional Budget |
|---|---:|---:|
| Affiliate | 60% | 49,685.67 |
| Paid Search | 40% | 33,123.78 |
| Total | 100% | 82,809.45 |

**Step 3: Calculate scenario spending**

| Channel | Historical Spend | Budget Change | Scenario Spend |
|---|---:|---:|---:|
| Affiliate | 857,835.07 | +49,685.67 | 907,520.74 |
| Paid Search | 897,091.53 | +33,123.78 | 930,215.31 |
| Paid Social | 984,731.88 | 0.00 | 984,731.88 |
| Display | 955,297.00 | 0.00 | 955,297.00 |
| Video | 828,094.54 | -82,809.45 | 745,285.09 |
| **Total** | **4,523,050.02** | **0.00** | **4,523,050.02** |

Displayed amounts are rounded to two decimal places. Calculations should use unrounded values.

The scenario maintains the same total advertising expenditure.

### 8. Scenario Calculation Methodology

The model assumes each channel maintains its historical ROAS after the budget change.

For each channel:

**Scenario Revenue = Scenario Spend × Historical Channel ROAS**

**Scenario Marketing Profit = Scenario Revenue − Scenario Spend**

The overall scenario ROAS is calculated as:

**Scenario ROAS = Total Scenario Revenue ÷ Total Scenario Spend**

For more accurate calculations, the model uses unrounded historical ROAS rather than the two-decimal values shown in the report.

The assumption of constant ROAS is important because actual marginal returns may decline as spending increases.

### 9. Illustrative Financial Impact

Using the historical channel revenue-to-spend ratios, the scenario produces the following approximate results.

| Metric | Baseline | Illustrative Scenario | Change |
|---|---:|---:|---:|
| Total Advertising Spend | 4,523,050.02 | 4,523,050.02 | 0.00 |
| Attributed Revenue | 21,561,839.01 | 21,861,000 (approx.) | +299,000 (approx.) |
| Marketing Profit | 17,038,788.99 | 17,338,000 (approx.) | +299,000 (approx.) |
| Overall ROAS | 4.77x | 4.83x (approx.) | +0.07x (approx.) |

These illustrative estimates are based on unrounded historical channel ROAS. The Python output file `budget_scenario_comparison.csv` is the reference for the executed scenario results.

The scenario's financial improvement is not a validated prediction of incremental revenue or profit.

### 10. Interpretation of Scenario Results

The illustrative model suggests that reallocating advertising spend from a historically lower-ROAS channel to higher-ROAS channels could improve modeled attributed revenue without increasing total expenditure.

However, historical average ROAS may not represent the return on additional advertising investment.

Potential reasons for differences between modeled and actual outcomes include:

- Audience saturation.
- Increasing advertising auction costs.
- Changes in conversion behavior.
- Seasonal demand fluctuations.
- Channel attribution differences.
- Campaign-specific performance variation.
- Brand-awareness and assisted-conversion effects.

Therefore, the modeled improvement should be treated as a hypothesis requiring business validation.

### 11. Implementation Recommendations

**Recommendation 1: Conduct controlled budget experiments**

Test small budget increases for Affiliate and Paid Search before implementing a larger reallocation.

**Recommendation 2: Review Video campaign objectives**

Determine whether Video is intended primarily for direct conversions, awareness, or upper-funnel engagement.

**Recommendation 3: Measure incremental performance**

Use controlled experiments where feasible to estimate the additional conversions and revenue caused by budget changes.

**Recommendation 4: Monitor acquisition costs**

Track cost per conversion alongside ROAS to identify whether additional spending reduces efficiency.

**Recommendation 5: Establish decision thresholds**

Define acceptable ROAS, acquisition costs, and profitability targets before scaling campaigns.

### 12. Supporting Project Files

The budget optimization analysis is supported by:

**SQL Analysis**

`03_SQL/07_budget_optimization.sql`

**Python Analysis**

`04_Python/07_budget_optimization.py`

**Python Outputs**

- `budget_optimization_scorecard.csv`
- `budget_reallocation_scenario.csv`
- `budget_scenario_comparison.csv`

**Visualization**

`05_Visualizations/08_budget_optimization_comparison.png`

### 13. Analysis Limitations

This analysis uses historical campaign data and a simplified financial scenario.

The primary limitations are:

1. Historical ROAS is assumed to remain constant after budget changes.
2. Incremental advertising returns are not directly measured.
3. Revenue attribution may not capture the full contribution of awareness channels.
4. Marketing profit excludes non-advertising business costs.
5. The scenario does not model budget constraints, audience saturation, or changing auction costs.
6. The scenario does not establish a causal relationship between budget reallocation and financial improvement.

### 14. Conclusion

The historical analysis identifies Affiliate and Paid Search as the strongest channels in terms of ROAS and advertising cost per conversion.

The illustrative budget optimization scenario demonstrates how marketing teams can use performance data to evaluate alternative spending allocations while maintaining a fixed overall budget.

The recommended next step is to test potential reallocations incrementally, measure actual incremental returns, and incorporate campaign objectives and business constraints before implementing major budget changes.

This approach supports disciplined, data-driven marketing investment decisions.