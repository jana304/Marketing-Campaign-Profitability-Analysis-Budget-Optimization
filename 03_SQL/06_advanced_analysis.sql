
-- =====================================================
-- MARKETING_PROFITABILITY PROJECT
-- PHASE 20: ADVANCED SQL ANALYSIS
-- File: 06_advanced_analysis.sql
-- Requires MySQL 8.0+
-- =====================================================

USE marketing_profitability_db;


-- =====================================================
-- 1. CAMPAIGN PERFORMANCE MASTER VIEW
-- Aggregates facts separately to avoid duplication.
-- =====================================================

DROP VIEW IF EXISTS vw_campaign_performance;

CREATE VIEW vw_campaign_performance AS
SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    c.objective,
    c.budget,
    COALESCE(s.impressions, 0) AS impressions,
    COALESCE(s.clicks, 0) AS clicks,
    COALESCE(s.spend, 0) AS spend,
    COALESCE(l.leads, 0) AS leads,
    COALESCE(v.conversions, 0) AS conversions,
    COALESCE(v.revenue, 0) AS revenue
FROM campaigns c
LEFT JOIN (
    SELECT
        campaign_id,
        SUM(impressions) AS impressions,
        SUM(clicks) AS clicks,
        SUM(spend) AS spend
    FROM daily_spend
    GROUP BY campaign_id
) s ON c.campaign_id = s.campaign_id
LEFT JOIN (
    SELECT
        campaign_id,
        COUNT(*) AS leads
    FROM leads
    GROUP BY campaign_id
) l ON c.campaign_id = l.campaign_id
LEFT JOIN (
    SELECT
        l.campaign_id,
        COUNT(v.conversion_id) AS conversions,
        SUM(v.revenue) AS revenue
    FROM leads l
    JOIN conversions v ON l.lead_id = v.lead_id
    GROUP BY l.campaign_id
) v ON c.campaign_id = v.campaign_id;


-- =====================================================
-- 2. MASTER CAMPAIGN KPI REPORT
-- =====================================================

SELECT
    campaign_id,
    campaign_name,
    channel,
    ROUND(spend, 2) AS total_spend,
    leads,
    conversions,
    ROUND(revenue, 2) AS revenue,
    ROUND(revenue - spend, 2) AS marketing_profit,
    ROUND(revenue / NULLIF(spend, 0), 2) AS roas,
    ROUND(spend / NULLIF(conversions, 0), 2) AS cac,
    ROUND(conversions * 100.0 /
        NULLIF(leads, 0), 2) AS conversion_rate
FROM vw_campaign_performance
ORDER BY marketing_profit DESC;


-- =====================================================
-- 3. CAMPAIGN PROFIT RANKING BY CHANNEL
-- =====================================================

SELECT
    campaign_id,
    campaign_name,
    channel,
    ROUND(revenue - spend, 2) AS marketing_profit,
    DENSE_RANK() OVER (
        PARTITION BY channel
        ORDER BY revenue - spend DESC
    ) AS profit_rank_in_channel
FROM vw_campaign_performance
ORDER BY channel, profit_rank_in_channel;


-- =====================================================
-- 4. CAMPAIGN REVENUE CONTRIBUTION
-- =====================================================

SELECT
    campaign_id,
    campaign_name,
    channel,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        revenue * 100.0 /
        NULLIF(SUM(revenue) OVER (), 0), 2
    ) AS revenue_contribution_percentage
FROM vw_campaign_performance
ORDER BY revenue DESC;


-- =====================================================
-- 5. CAMPAIGN PERFORMANCE SEGMENTATION
-- =====================================================

WITH performance AS (
    SELECT
        campaign_id,
        campaign_name,
        channel,
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
    ROUND(revenue, 2) AS revenue,
    ROUND(roas, 2) AS roas,
    CASE
        WHEN roas >= 6 THEN 'High Performer'
        WHEN roas >= 4 THEN 'Moderate Performer'
        WHEN roas IS NULL THEN 'No Spend'
        ELSE 'Low Performer'
    END AS performance_segment
FROM performance
ORDER BY roas DESC;


-- =====================================================
-- 6. CHANNEL-WISE PERFORMANCE SUMMARY
-- =====================================================

SELECT
    channel,
    COUNT(*) AS campaigns,
    ROUND(SUM(spend), 2) AS spend,
    SUM(leads) AS leads,
    SUM(conversions) AS conversions,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(revenue - spend), 2) AS profit,
    ROUND(
        SUM(revenue) / NULLIF(SUM(spend), 0), 2
    ) AS roas
FROM vw_campaign_performance
GROUP BY channel
ORDER BY profit DESC;


-- =====================================================
-- 7. ABOVE-AVERAGE ROAS CAMPAIGNS
-- =====================================================

WITH campaign_roas AS (
    SELECT
        campaign_id,
        campaign_name,
        channel,
        revenue / NULLIF(spend, 0) AS roas
    FROM vw_campaign_performance
),
benchmark AS (
    SELECT AVG(roas) AS average_roas
    FROM campaign_roas
)
SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    ROUND(c.roas, 2) AS campaign_roas,
    ROUND(b.average_roas, 2) AS average_campaign_roas
FROM campaign_roas c
CROSS JOIN benchmark b
WHERE c.roas > b.average_roas
ORDER BY c.roas DESC;


-- =====================================================
-- 8. TOP 3 CAMPAIGNS PER CHANNEL
-- =====================================================

WITH ranked AS (
    SELECT
        campaign_id,
        campaign_name,
        channel,
        revenue - spend AS profit,
        ROW_NUMBER() OVER (
            PARTITION BY channel
            ORDER BY revenue - spend DESC, campaign_id
        ) AS rn
    FROM vw_campaign_performance
)
SELECT
    campaign_id,
    campaign_name,
    channel,
    ROUND(profit, 2) AS marketing_profit,
    rn AS channel_rank
FROM ranked
WHERE rn <= 3
ORDER BY channel, channel_rank;


-- =====================================================
-- 9. CUMULATIVE MONTHLY MARKETING SPEND
-- =====================================================

WITH monthly_spend AS (
    SELECT
        DATE_FORMAT(spend_date, '%Y-%m') AS month,
        SUM(spend) AS spend
    FROM daily_spend
    GROUP BY DATE_FORMAT(spend_date, '%Y-%m')
)
SELECT
    month,
    ROUND(spend, 2) AS monthly_spend,
    ROUND(
        SUM(spend) OVER (
            ORDER BY month
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ), 2
    ) AS cumulative_spend
FROM monthly_spend
ORDER BY month;


-- =====================================================
-- 10. MONTH-OVER-MONTH SPEND GROWTH
-- =====================================================

WITH monthly_spend AS (
    SELECT
        DATE_FORMAT(spend_date, '%Y-%m') AS month,
        SUM(spend) AS spend
    FROM daily_spend
    GROUP BY DATE_FORMAT(spend_date, '%Y-%m')
),
growth AS (
    SELECT
        month,
        spend,
        LAG(spend) OVER (ORDER BY month)
            AS previous_month_spend
    FROM monthly_spend
)
SELECT
    month,
    ROUND(spend, 2) AS monthly_spend,
    ROUND(previous_month_spend, 2)
        AS previous_month_spend,
    ROUND(
        (spend - previous_month_spend) * 100.0 /
        NULLIF(previous_month_spend, 0), 2
    ) AS growth_percentage
FROM growth
ORDER BY month;


-- =====================================================
-- 11. CAMPAIGN PROFIT PERCENTILE
-- =====================================================

SELECT
    campaign_id,
    campaign_name,
    channel,
    ROUND(revenue - spend, 2) AS profit,
    ROUND(
        PERCENT_RANK() OVER (
            ORDER BY revenue - spend
        ) * 100, 2
    ) AS profit_percentile
FROM vw_campaign_performance
ORDER BY profit DESC;


-- =====================================================
-- 12. CAMPAIGN BUDGET EFFICIENCY
-- =====================================================

SELECT
    campaign_id,
    campaign_name,
    channel,
    ROUND(budget, 2) AS budget,
    ROUND(spend, 2) AS actual_spend,
    ROUND(budget - spend, 2) AS budget_remaining,
    ROUND(
        spend * 100.0 / NULLIF(budget, 0), 2
    ) AS budget_utilization_percentage,
    ROUND(revenue / NULLIF(spend, 0), 2) AS roas,
    CASE
        WHEN spend > budget THEN 'Over Budget'
        WHEN spend >= budget * 0.9 THEN 'Near Budget'
        ELSE 'Under Budget'
    END AS budget_status
FROM vw_campaign_performance
ORDER BY budget_utilization_percentage DESC;


-- =====================================================
-- END OF ADVANCED SQL ANALYSIS
-- =====================================================
