
-- =====================================================
-- MARKETING_PROFITABILITY PROJECT
-- PHASE 21: BUDGET OPTIMIZATION ANALYSIS
-- File: 07_budget_optimization.sql
-- MySQL 8.0+
-- =====================================================

USE marketing_profitability_db;


-- =====================================================
-- 1. OVERALL BUDGET UTILIZATION
-- =====================================================

SELECT
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND(SUM(spend), 2) AS actual_spend,
    ROUND(SUM(budget - spend), 2) AS remaining_budget,
    ROUND(
        SUM(spend) * 100.0 /
        NULLIF(SUM(budget), 0), 2
    ) AS budget_utilization_percentage
FROM vw_campaign_performance;


-- =====================================================
-- 2. CHANNEL-WISE BUDGET UTILIZATION
-- =====================================================

SELECT
    channel,
    COUNT(*) AS total_campaigns,
    ROUND(SUM(budget), 2) AS allocated_budget,
    ROUND(SUM(spend), 2) AS actual_spend,
    ROUND(SUM(budget - spend), 2) AS remaining_budget,
    ROUND(
        SUM(spend) * 100.0 /
        NULLIF(SUM(budget), 0), 2
    ) AS budget_utilization_percentage
FROM vw_campaign_performance
GROUP BY channel
ORDER BY budget_utilization_percentage DESC;


-- =====================================================
-- 3. HIGH-ROAS CAMPAIGNS WITH AVAILABLE BUDGET
-- =====================================================

SELECT
    campaign_id,
    campaign_name,
    channel,
    ROUND(budget, 2) AS budget,
    ROUND(spend, 2) AS spend,
    ROUND(budget - spend, 2) AS remaining_budget,
    ROUND(revenue / NULLIF(spend, 0), 2) AS roas
FROM vw_campaign_performance
WHERE spend > 0
  AND spend < budget
  AND revenue / NULLIF(spend, 0) >= 6
ORDER BY roas DESC;


-- =====================================================
-- 4. LOW-ROAS CAMPAIGNS REQUIRING REVIEW
-- Threshold is illustrative, not a universal rule.
-- =====================================================

SELECT
    campaign_id,
    campaign_name,
    channel,
    ROUND(spend, 2) AS spend,
    ROUND(revenue, 2) AS revenue,
    ROUND(revenue - spend, 2) AS marketing_profit,
    ROUND(revenue / NULLIF(spend, 0), 2) AS roas
FROM vw_campaign_performance
WHERE spend > 0
  AND revenue / NULLIF(spend, 0) < 3
ORDER BY roas ASC;


-- =====================================================
-- 5. CHANNEL BUDGET AND PERFORMANCE SUMMARY
-- =====================================================

SELECT
    channel,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND(SUM(spend), 2) AS total_spend,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue - spend), 2) AS marketing_profit,
    ROUND(
        SUM(revenue) / NULLIF(SUM(spend), 0), 2
    ) AS roas,
    ROUND(
        SUM(spend) / NULLIF(SUM(conversions), 0), 2
    ) AS cost_per_conversion
FROM vw_campaign_performance
GROUP BY channel
ORDER BY roas DESC;


-- =====================================================
-- 6. CURRENT CHANNEL SPEND DISTRIBUTION
-- =====================================================

WITH channel_spend AS (
    SELECT
        channel,
        SUM(spend) AS total_spend
    FROM vw_campaign_performance
    GROUP BY channel
)
SELECT
    channel,
    ROUND(total_spend, 2) AS total_spend,
    ROUND(
        total_spend * 100.0 /
        NULLIF(SUM(total_spend) OVER (), 0), 2
    ) AS spend_share_percentage
FROM channel_spend
ORDER BY spend_share_percentage DESC;


-- =====================================================
-- 7. CAMPAIGN OPTIMIZATION PRIORITY
-- These are screening recommendations.
-- =====================================================

WITH metrics AS (
    SELECT
        campaign_id,
        campaign_name,
        channel,
        budget,
        spend,
        revenue,
        revenue / NULLIF(spend, 0) AS roas
    FROM vw_campaign_performance
)
SELECT
    campaign_id,
    campaign_name,
    channel,
    ROUND(spend, 2) AS spend,
    ROUND(roas, 2) AS roas,
    CASE
        WHEN spend = 0 THEN 'Review No Spend'
        WHEN roas >= 6 AND spend < budget
            THEN 'Consider Scaling'
        WHEN roas < 3
            THEN 'Review or Reduce'
        WHEN roas >= 4
            THEN 'Maintain and Monitor'
        ELSE 'Investigate Performance'
    END AS optimization_recommendation
FROM metrics
ORDER BY
    CASE
        WHEN roas >= 6 AND spend < budget THEN 1
        WHEN roas < 3 THEN 2
        ELSE 3
    END,
    roas DESC;


-- =====================================================
-- 8. CHANNEL REALLOCATION SCENARIO
-- Move 10% of Video spend:
-- 60% to Affiliate and 40% to Paid Search.
-- Total spend stays unchanged.
-- Assumes historical ROAS remains constant;
-- this is NOT a causal forecast.
-- =====================================================

WITH channel_metrics AS (
    SELECT
        channel,
        SUM(spend) AS current_spend,
        SUM(revenue) AS current_revenue,
        SUM(revenue) /
            NULLIF(SUM(spend), 0) AS historical_roas
    FROM vw_campaign_performance
    GROUP BY channel
),
transfer AS (
    SELECT
        COALESCE(
            MAX(CASE
                WHEN channel = 'video'
                THEN current_spend
            END), 0
        ) * 0.10 AS transfer_amount
    FROM channel_metrics
),
scenario AS (
    SELECT
        m.channel,
        m.current_spend,
        m.current_revenue,
        m.historical_roas,
        CASE
            WHEN m.channel = 'video'
                THEN -t.transfer_amount
            WHEN m.channel = 'affiliate'
                THEN t.transfer_amount * 0.60
            WHEN m.channel = 'paid_search'
                THEN t.transfer_amount * 0.40
            ELSE 0
        END AS budget_change
    FROM channel_metrics m
    CROSS JOIN transfer t
)
SELECT
    channel,
    ROUND(current_spend, 2) AS current_spend,
    ROUND(budget_change, 2) AS budget_change,
    ROUND(
        current_spend + budget_change, 2
    ) AS proposed_spend,
    ROUND(historical_roas, 2) AS historical_roas,
    ROUND(
        (current_spend + budget_change)
        * historical_roas, 2
    ) AS illustrative_revenue
FROM scenario
ORDER BY channel;


-- =====================================================
-- 9. SCENARIO IMPACT SUMMARY
-- Constant historical ROAS assumption.
-- =====================================================

WITH channel_metrics AS (
    SELECT
        channel,
        SUM(spend) AS spend,
        SUM(revenue) AS revenue,
        SUM(revenue) /
            NULLIF(SUM(spend), 0) AS roas
    FROM vw_campaign_performance
    GROUP BY channel
),
transfer AS (
    SELECT
        COALESCE(
            MAX(CASE WHEN channel = 'video'
                THEN spend END), 0
        ) * 0.10 AS amount
    FROM channel_metrics
),
scenario AS (
    SELECT
        m.spend,
        m.revenue,
        m.roas,
        m.spend +
        CASE
            WHEN m.channel = 'video'
                THEN -t.amount
            WHEN m.channel = 'affiliate'
                THEN t.amount * 0.60
            WHEN m.channel = 'paid_search'
                THEN t.amount * 0.40
            ELSE 0
        END AS proposed_spend
    FROM channel_metrics m
    CROSS JOIN transfer t
)
SELECT
    ROUND(SUM(spend), 2) AS current_total_spend,
    ROUND(SUM(proposed_spend), 2)
        AS proposed_total_spend,
    ROUND(SUM(revenue), 2) AS current_revenue,
    ROUND(SUM(proposed_spend * roas), 2)
        AS illustrative_revenue,
    ROUND(
        SUM(proposed_spend * roas)
        - SUM(revenue), 2
    ) AS illustrative_revenue_change,
    ROUND(
        SUM(revenue) / NULLIF(SUM(spend), 0), 2
    ) AS current_roas,
    ROUND(
        SUM(proposed_spend * roas) /
        NULLIF(SUM(proposed_spend), 0), 2
    ) AS illustrative_roas
FROM scenario;


-- =====================================================
-- 10. FINAL CHANNEL OPTIMIZATION SCORECARD
-- =====================================================

WITH channel_summary AS (
    SELECT
        channel,
        SUM(spend) AS spend,
        SUM(revenue) AS revenue,
        SUM(conversions) AS conversions,
        SUM(revenue) /
            NULLIF(SUM(spend), 0) AS roas,
        SUM(spend) /
            NULLIF(SUM(conversions), 0) AS cac
    FROM vw_campaign_performance
    GROUP BY channel
)
SELECT
    channel,
    ROUND(spend, 2) AS spend,
    ROUND(revenue, 2) AS revenue,
    ROUND(revenue - spend, 2) AS marketing_profit,
    ROUND(roas, 2) AS roas,
    ROUND(cac, 2) AS cost_per_conversion,
    RANK() OVER (
        ORDER BY roas DESC
    ) AS roas_rank,
    RANK() OVER (
        ORDER BY cac ASC
    ) AS acquisition_cost_rank,
    CASE
        WHEN roas >= 6
            THEN 'Evaluate for Expansion'
        WHEN roas >= 4
            THEN 'Maintain and Optimize'
        ELSE 'Review Budget Efficiency'
    END AS budget_strategy
FROM channel_summary
ORDER BY roas_rank;


-- =====================================================
-- END OF BUDGET OPTIMIZATION ANALYSIS
-- =====================================================
