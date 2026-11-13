
-- =====================================================
-- MARKETING_PROFITABILITY PROJECT
-- PHASE 19: REVENUE AND PROFITABILITY ANALYSIS
-- File: 05_revenue_profitability.sql
-- MySQL 8.0+
-- =====================================================

USE marketing_profitability_db;


-- =====================================================
-- 1. OVERALL REVENUE
-- =====================================================

SELECT
    COUNT(*) AS total_conversions,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS average_revenue_per_conversion
FROM conversions;


-- =====================================================
-- 2. OVERALL MARKETING PROFITABILITY
-- =====================================================

WITH spend_summary AS (
    SELECT SUM(spend) AS total_spend
    FROM daily_spend
),
revenue_summary AS (
    SELECT SUM(revenue) AS total_revenue
    FROM conversions
)
SELECT
    ROUND(s.total_spend, 2) AS total_spend,
    ROUND(r.total_revenue, 2) AS total_revenue,
    ROUND(r.total_revenue - s.total_spend, 2)
        AS marketing_profit,
    ROUND(
        r.total_revenue / NULLIF(s.total_spend, 0), 2
    ) AS roas,
    ROUND(
        (r.total_revenue - s.total_spend) * 100.0 /
        NULLIF(s.total_spend, 0), 2
    ) AS marketing_roi_percentage,
    ROUND(
        (r.total_revenue - s.total_spend) * 100.0 /
        NULLIF(r.total_revenue, 0), 2
    ) AS marketing_profit_margin_percentage
FROM spend_summary s
CROSS JOIN revenue_summary r;


-- =====================================================
-- 3. REVENUE BY CHANNEL
-- =====================================================

SELECT
    c.channel,
    COUNT(v.conversion_id) AS total_conversions,
    ROUND(COALESCE(SUM(v.revenue), 0), 2)
        AS total_revenue
FROM campaigns c
LEFT JOIN leads l
    ON c.campaign_id = l.campaign_id
LEFT JOIN conversions v
    ON l.lead_id = v.lead_id
GROUP BY c.channel
ORDER BY total_revenue DESC;


-- =====================================================
-- 4. CHANNEL-WISE PROFIT, ROAS AND ROI
-- Separate spend and revenue aggregations prevent
-- duplicate spend caused by joining raw fact tables.
-- =====================================================

WITH channel_spend AS (
    SELECT
        c.channel,
        SUM(d.spend) AS total_spend
    FROM campaigns c
    JOIN daily_spend d
        ON c.campaign_id = d.campaign_id
    GROUP BY c.channel
),
channel_revenue AS (
    SELECT
        c.channel,
        SUM(v.revenue) AS total_revenue
    FROM campaigns c
    JOIN leads l
        ON c.campaign_id = l.campaign_id
    JOIN conversions v
        ON l.lead_id = v.lead_id
    GROUP BY c.channel
)
SELECT
    c.channel,
    ROUND(COALESCE(s.total_spend, 0), 2) AS total_spend,
    ROUND(COALESCE(r.total_revenue, 0), 2)
        AS total_revenue,
    ROUND(
        COALESCE(r.total_revenue, 0)
        - COALESCE(s.total_spend, 0), 2
    ) AS marketing_profit,
    ROUND(
        r.total_revenue /
        NULLIF(s.total_spend, 0), 2
    ) AS roas,
    ROUND(
        (COALESCE(r.total_revenue, 0)
        - COALESCE(s.total_spend, 0)) * 100.0 /
        NULLIF(s.total_spend, 0), 2
    ) AS roi_percentage
FROM (SELECT DISTINCT channel FROM campaigns) c
LEFT JOIN channel_spend s ON c.channel = s.channel
LEFT JOIN channel_revenue r ON c.channel = r.channel
ORDER BY marketing_profit DESC;


-- =====================================================
-- 5. CAMPAIGN-WISE REVENUE
-- =====================================================

SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    COUNT(v.conversion_id) AS total_conversions,
    ROUND(COALESCE(SUM(v.revenue), 0), 2)
        AS total_revenue
FROM campaigns c
LEFT JOIN leads l
    ON c.campaign_id = l.campaign_id
LEFT JOIN conversions v
    ON l.lead_id = v.lead_id
GROUP BY
    c.campaign_id,
    c.campaign_name,
    c.channel
ORDER BY total_revenue DESC;


-- =====================================================
-- 6. CAMPAIGN-LEVEL PROFITABILITY
-- =====================================================

WITH campaign_spend AS (
    SELECT
        campaign_id,
        SUM(spend) AS total_spend
    FROM daily_spend
    GROUP BY campaign_id
),
campaign_revenue AS (
    SELECT
        l.campaign_id,
        COUNT(v.conversion_id) AS total_conversions,
        SUM(v.revenue) AS total_revenue
    FROM leads l
    JOIN conversions v
        ON l.lead_id = v.lead_id
    GROUP BY l.campaign_id
)
SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    ROUND(COALESCE(s.total_spend, 0), 2)
        AS total_spend,
    COALESCE(r.total_conversions, 0)
        AS total_conversions,
    ROUND(COALESCE(r.total_revenue, 0), 2)
        AS total_revenue,
    ROUND(
        COALESCE(r.total_revenue, 0)
        - COALESCE(s.total_spend, 0), 2
    ) AS marketing_profit,
    ROUND(
        r.total_revenue /
        NULLIF(s.total_spend, 0), 2
    ) AS roas
FROM campaigns c
LEFT JOIN campaign_spend s
    ON c.campaign_id = s.campaign_id
LEFT JOIN campaign_revenue r
    ON c.campaign_id = r.campaign_id
ORDER BY marketing_profit DESC;


-- =====================================================
-- 7. TOP 10 MOST PROFITABLE CAMPAIGNS
-- =====================================================

WITH campaign_spend AS (
    SELECT campaign_id, SUM(spend) AS spend
    FROM daily_spend
    GROUP BY campaign_id
),
campaign_revenue AS (
    SELECT l.campaign_id, SUM(v.revenue) AS revenue
    FROM leads l
    JOIN conversions v ON l.lead_id = v.lead_id
    GROUP BY l.campaign_id
)
SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    ROUND(COALESCE(s.spend, 0), 2) AS total_spend,
    ROUND(COALESCE(r.revenue, 0), 2) AS total_revenue,
    ROUND(
        COALESCE(r.revenue, 0) - COALESCE(s.spend, 0), 2
    ) AS marketing_profit
FROM campaigns c
LEFT JOIN campaign_spend s ON c.campaign_id = s.campaign_id
LEFT JOIN campaign_revenue r ON c.campaign_id = r.campaign_id
ORDER BY marketing_profit DESC
LIMIT 10;


-- =====================================================
-- 8. BOTTOM 10 CAMPAIGNS BY PROFIT
-- =====================================================

WITH campaign_spend AS (
    SELECT campaign_id, SUM(spend) AS spend
    FROM daily_spend
    GROUP BY campaign_id
),
campaign_revenue AS (
    SELECT l.campaign_id, SUM(v.revenue) AS revenue
    FROM leads l
    JOIN conversions v ON l.lead_id = v.lead_id
    GROUP BY l.campaign_id
)
SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    ROUND(COALESCE(s.spend, 0), 2) AS total_spend,
    ROUND(COALESCE(r.revenue, 0), 2) AS total_revenue,
    ROUND(
        COALESCE(r.revenue, 0) - COALESCE(s.spend, 0), 2
    ) AS marketing_profit
FROM campaigns c
LEFT JOIN campaign_spend s ON c.campaign_id = s.campaign_id
LEFT JOIN campaign_revenue r ON c.campaign_id = r.campaign_id
ORDER BY marketing_profit ASC
LIMIT 10;


-- =====================================================
-- 9. TOP 10 CAMPAIGNS BY ROAS
-- =====================================================

WITH campaign_spend AS (
    SELECT campaign_id, SUM(spend) AS spend
    FROM daily_spend
    GROUP BY campaign_id
),
campaign_revenue AS (
    SELECT l.campaign_id, SUM(v.revenue) AS revenue
    FROM leads l
    JOIN conversions v ON l.lead_id = v.lead_id
    GROUP BY l.campaign_id
)
SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    ROUND(s.spend, 2) AS total_spend,
    ROUND(COALESCE(r.revenue, 0), 2) AS total_revenue,
    ROUND(
        COALESCE(r.revenue, 0) /
        NULLIF(s.spend, 0), 2
    ) AS roas
FROM campaigns c
JOIN campaign_spend s ON c.campaign_id = s.campaign_id
LEFT JOIN campaign_revenue r ON c.campaign_id = r.campaign_id
WHERE s.spend > 0
ORDER BY roas DESC
LIMIT 10;


-- =====================================================
-- 10. REVENUE BY CONVERSION TYPE
-- =====================================================

SELECT
    conversion_type,
    COUNT(*) AS total_conversions,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS average_revenue
FROM conversions
GROUP BY conversion_type
ORDER BY total_revenue DESC;


-- =====================================================
-- 11. MONTHLY CONVERSION REVENUE
-- Revenue is grouped by conversion month.
-- Spend is not compared here because the
-- conversion and spend dates may differ.
-- =====================================================

SELECT
    DATE_FORMAT(converted_at, '%Y-%m') AS month,
    COUNT(*) AS total_conversions,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM conversions
GROUP BY DATE_FORMAT(converted_at, '%Y-%m')
ORDER BY month;


-- =====================================================
-- 12. CHANNEL PROFITABILITY RANKING
-- =====================================================

WITH channel_spend AS (
    SELECT
        c.channel,
        SUM(d.spend) AS spend
    FROM campaigns c
    JOIN daily_spend d
        ON c.campaign_id = d.campaign_id
    GROUP BY c.channel
),
channel_revenue AS (
    SELECT
        c.channel,
        SUM(v.revenue) AS revenue
    FROM campaigns c
    JOIN leads l
        ON c.campaign_id = l.campaign_id
    JOIN conversions v
        ON l.lead_id = v.lead_id
    GROUP BY c.channel
),
metrics AS (
    SELECT
        c.channel,
        COALESCE(s.spend, 0) AS spend,
        COALESCE(r.revenue, 0) AS revenue
    FROM (SELECT DISTINCT channel FROM campaigns) c
    LEFT JOIN channel_spend s ON c.channel = s.channel
    LEFT JOIN channel_revenue r ON c.channel = r.channel
)
SELECT
    channel,
    ROUND(spend, 2) AS total_spend,
    ROUND(revenue, 2) AS total_revenue,
    ROUND(revenue - spend, 2) AS marketing_profit,
    ROUND(
        revenue / NULLIF(spend, 0), 2
    ) AS roas,
    RANK() OVER (
        ORDER BY revenue - spend DESC
    ) AS profit_rank,
    RANK() OVER (
        ORDER BY revenue / NULLIF(spend, 0) DESC
    ) AS roas_rank
FROM metrics
ORDER BY profit_rank;


-- =====================================================
-- END OF REVENUE AND PROFITABILITY ANALYSIS
-- =====================================================
