
-- MARKETING PROFITABILITY PROJECT
-- Phase 17: Marketing Performance Analysis
-- Step 291: Overall Marketing Performance

USE marketing_profitability_db;

SELECT
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    ROUND(SUM(spend), 2) AS total_spend,

    ROUND(
        SUM(clicks) * 100.0 /
        NULLIF(SUM(impressions), 0), 2
    ) AS ctr_percentage,

    ROUND(
        SUM(spend) /
        NULLIF(SUM(clicks), 0), 2
    ) AS average_cpc

FROM daily_spend;


-- Step 292: Marketing Performance by Channel

SELECT
    c.channel,
    SUM(d.impressions) AS total_impressions,
    SUM(d.clicks) AS total_clicks,
    ROUND(SUM(d.spend), 2) AS total_spend,
    ROUND(
        SUM(d.clicks) * 100.0 /
        NULLIF(SUM(d.impressions), 0), 2
    ) AS ctr_percentage,
    ROUND(
        SUM(d.spend) /
        NULLIF(SUM(d.clicks), 0), 2
    ) AS average_cpc
FROM campaigns c
JOIN daily_spend d
    ON c.campaign_id = d.campaign_id
GROUP BY c.channel
ORDER BY total_spend DESC;


-- Step 293: Top 10 Campaigns by Marketing Spend

SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    SUM(d.impressions) AS total_impressions,
    SUM(d.clicks) AS total_clicks,
    ROUND(SUM(d.spend), 2) AS total_spend,
    ROUND(
        SUM(d.clicks) * 100.0 /
        NULLIF(SUM(d.impressions), 0), 2
    ) AS ctr_percentage,
    ROUND(
        SUM(d.spend) /
        NULLIF(SUM(d.clicks), 0), 2
    ) AS average_cpc
FROM campaigns c
JOIN daily_spend d
    ON c.campaign_id = d.campaign_id
GROUP BY
    c.campaign_id,
    c.campaign_name,
    c.channel
ORDER BY total_spend DESC
LIMIT 10;


-- Step 294: Monthly Marketing Performance

SELECT
    DATE_FORMAT(spend_date, '%Y-%m') AS month,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    ROUND(SUM(spend), 2) AS total_spend,
    ROUND(
        SUM(clicks) * 100.0 /
        NULLIF(SUM(impressions), 0), 2
    ) AS ctr_percentage,
    ROUND(
        SUM(spend) /
        NULLIF(SUM(clicks), 0), 2
    ) AS average_cpc
FROM daily_spend
GROUP BY DATE_FORMAT(spend_date, '%Y-%m')
ORDER BY month;


-- =====================================================
-- MARKETING_PROFITABILITY
-- Phase 17: Marketing Performance Analysis
-- File: 03_marketing_performance.sql
-- Database: marketing_profitability_db
-- =====================================================

USE marketing_profitability_db;


-- =====================================================
-- 1. OVERALL MARKETING PERFORMANCE
-- =====================================================

SELECT
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    ROUND(SUM(spend), 2) AS total_spend,
    ROUND(
        SUM(clicks) * 100.0 /
        NULLIF(SUM(impressions), 0), 2
    ) AS ctr_percentage,
    ROUND(
        SUM(spend) /
        NULLIF(SUM(clicks), 0), 2
    ) AS average_cpc
FROM daily_spend;


-- =====================================================
-- 2. MARKETING PERFORMANCE BY CHANNEL
-- =====================================================

SELECT
    c.channel,
    SUM(d.impressions) AS total_impressions,
    SUM(d.clicks) AS total_clicks,
    ROUND(SUM(d.spend), 2) AS total_spend,
    ROUND(
        SUM(d.clicks) * 100.0 /
        NULLIF(SUM(d.impressions), 0), 2
    ) AS ctr_percentage,
    ROUND(
        SUM(d.spend) /
        NULLIF(SUM(d.clicks), 0), 2
    ) AS average_cpc
FROM campaigns c
JOIN daily_spend d
    ON c.campaign_id = d.campaign_id
GROUP BY c.channel
ORDER BY total_spend DESC;


-- =====================================================
-- 3. TOP 10 CAMPAIGNS BY MARKETING SPEND
-- =====================================================

SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    SUM(d.impressions) AS total_impressions,
    SUM(d.clicks) AS total_clicks,
    ROUND(SUM(d.spend), 2) AS total_spend,
    ROUND(
        SUM(d.clicks) * 100.0 /
        NULLIF(SUM(d.impressions), 0), 2
    ) AS ctr_percentage,
    ROUND(
        SUM(d.spend) /
        NULLIF(SUM(d.clicks), 0), 2
    ) AS average_cpc
FROM campaigns c
JOIN daily_spend d
    ON c.campaign_id = d.campaign_id
GROUP BY
    c.campaign_id,
    c.campaign_name,
    c.channel
ORDER BY total_spend DESC
LIMIT 10;


-- =====================================================
-- 4. MONTHLY MARKETING PERFORMANCE
-- =====================================================

SELECT
    DATE_FORMAT(spend_date, '%Y-%m') AS month,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    ROUND(SUM(spend), 2) AS total_spend,
    ROUND(
        SUM(clicks) * 100.0 /
        NULLIF(SUM(impressions), 0), 2
    ) AS ctr_percentage,
    ROUND(
        SUM(spend) /
        NULLIF(SUM(clicks), 0), 2
    ) AS average_cpc
FROM daily_spend
GROUP BY DATE_FORMAT(spend_date, '%Y-%m')
ORDER BY month;


-- =====================================================
-- 5. CHANNEL-WISE CAMPAIGN COUNT AND BUDGET
-- =====================================================

SELECT
    channel,
    COUNT(*) AS total_campaigns,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND(AVG(budget), 2) AS average_budget
FROM campaigns
GROUP BY channel
ORDER BY total_budget DESC;


-- =====================================================
-- 6. TOP 10 CAMPAIGNS BY CTR
-- =====================================================

SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    SUM(d.impressions) AS total_impressions,
    SUM(d.clicks) AS total_clicks,
    ROUND(
        SUM(d.clicks) * 100.0 /
        NULLIF(SUM(d.impressions), 0), 2
    ) AS ctr_percentage
FROM campaigns c
JOIN daily_spend d
    ON c.campaign_id = d.campaign_id
GROUP BY
    c.campaign_id,
    c.campaign_name,
    c.channel
HAVING SUM(d.impressions) > 0
ORDER BY ctr_percentage DESC
LIMIT 10;


-- =====================================================
-- 7. TOP 10 CAMPAIGNS WITH LOWEST CPC
-- =====================================================

SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    SUM(d.clicks) AS total_clicks,
    ROUND(SUM(d.spend), 2) AS total_spend,
    ROUND(
        SUM(d.spend) /
        NULLIF(SUM(d.clicks), 0), 2
    ) AS average_cpc
FROM campaigns c
JOIN daily_spend d
    ON c.campaign_id = d.campaign_id
GROUP BY
    c.campaign_id,
    c.campaign_name,
    c.channel
HAVING SUM(d.clicks) > 0
ORDER BY
    SUM(d.spend) / NULLIF(SUM(d.clicks), 0) ASC
LIMIT 10;


-- =====================================================
-- 8. YEARLY MARKETING PERFORMANCE
-- =====================================================

SELECT
    YEAR(spend_date) AS marketing_year,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    ROUND(SUM(spend), 2) AS total_spend,
    ROUND(
        SUM(clicks) * 100.0 /
        NULLIF(SUM(impressions), 0), 2
    ) AS ctr_percentage,
    ROUND(
        SUM(spend) /
        NULLIF(SUM(clicks), 0), 2
    ) AS average_cpc
FROM daily_spend
GROUP BY YEAR(spend_date)
ORDER BY marketing_year;


-- =====================================================
-- 9. MONTHLY SPEND BY CHANNEL
-- =====================================================

SELECT
    DATE_FORMAT(d.spend_date, '%Y-%m') AS month,
    c.channel,
    ROUND(SUM(d.spend), 2) AS total_spend,
    SUM(d.clicks) AS total_clicks,
    SUM(d.impressions) AS total_impressions
FROM daily_spend d
JOIN campaigns c
    ON d.campaign_id = c.campaign_id
GROUP BY
    DATE_FORMAT(d.spend_date, '%Y-%m'),
    c.channel
ORDER BY month, c.channel;


-- =====================================================
-- 10. CAMPAIGN BUDGET UTILIZATION
-- =====================================================

SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    c.budget,
    ROUND(
        COALESCE(SUM(d.spend), 0), 2
    ) AS actual_spend,
    ROUND(
        c.budget - COALESCE(SUM(d.spend), 0), 2
    ) AS remaining_budget,
    ROUND(
        COALESCE(SUM(d.spend), 0) * 100.0 /
        NULLIF(c.budget, 0), 2
    ) AS budget_utilization_percentage
FROM campaigns c
LEFT JOIN daily_spend d
    ON c.campaign_id = d.campaign_id
GROUP BY
    c.campaign_id,
    c.campaign_name,
    c.channel,
    c.budget
ORDER BY budget_utilization_percentage DESC;


-- =====================================================
-- 11. DAILY MARKETING SPEND TREND
-- =====================================================

SELECT
    spend_date,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    ROUND(SUM(spend), 2) AS total_spend
FROM daily_spend
GROUP BY spend_date
ORDER BY spend_date;


-- =====================================================
-- 12. CHANNEL PERFORMANCE RANKING
-- =====================================================

WITH channel_metrics AS (
    SELECT
        c.channel,
        SUM(d.impressions) AS impressions,
        SUM(d.clicks) AS clicks,
        SUM(d.spend) AS spend
    FROM campaigns c
    JOIN daily_spend d
        ON c.campaign_id = d.campaign_id
    GROUP BY c.channel
)

SELECT
    channel,
    ROUND(spend, 2) AS total_spend,
    ROUND(
        clicks * 100.0 /
        NULLIF(impressions, 0), 2
    ) AS ctr_percentage,
    ROUND(
        spend /
        NULLIF(clicks, 0), 2
    ) AS average_cpc,
    RANK() OVER (
        ORDER BY
            clicks * 1.0 /
            NULLIF(impressions, 0) DESC
    ) AS ctr_rank,
    RANK() OVER (
        ORDER BY
            spend /
            NULLIF(clicks, 0) ASC
    ) AS cpc_rank
FROM channel_metrics
ORDER BY ctr_rank;


-- =====================================================
-- END OF MARKETING PERFORMANCE ANALYSIS
-- =====================================================
