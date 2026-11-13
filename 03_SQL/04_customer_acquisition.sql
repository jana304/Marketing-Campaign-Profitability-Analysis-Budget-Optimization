
-- =====================================================
-- MARKETING_PROFITABILITY PROJECT
-- PHASE 18: CUSTOMER ACQUISITION ANALYSIS
-- File: 04_customer_acquisition.sql
-- MySQL 8.0+
-- =====================================================

USE marketing_profitability_db;


-- =====================================================
-- 1. OVERALL LEADS AND CONVERSIONS
-- =====================================================

SELECT
    (SELECT COUNT(*) FROM leads) AS total_leads,
    (SELECT COUNT(*) FROM conversions) AS total_conversions,
    ROUND(
        (SELECT COUNT(*) FROM conversions) * 100.0 /
        NULLIF((SELECT COUNT(*) FROM leads), 0), 2
    ) AS conversion_rate_percentage;


-- =====================================================
-- 2. OVERALL COST PER LEAD AND ACQUISITION COST
-- =====================================================

SELECT
    ROUND((SELECT SUM(spend) FROM daily_spend), 2)
        AS total_marketing_spend,
    (SELECT COUNT(*) FROM leads) AS total_leads,
    (SELECT COUNT(*) FROM conversions) AS total_conversions,
    ROUND(
        (SELECT SUM(spend) FROM daily_spend) /
        NULLIF((SELECT COUNT(*) FROM leads), 0), 2
    ) AS cost_per_lead,
    ROUND(
        (SELECT SUM(spend) FROM daily_spend) /
        NULLIF((SELECT COUNT(*) FROM conversions), 0), 2
    ) AS customer_acquisition_cost;


-- =====================================================
-- 3. LEADS BY MARKETING CHANNEL
-- =====================================================

SELECT
    c.channel,
    COUNT(l.lead_id) AS total_leads
FROM campaigns c
LEFT JOIN leads l
    ON c.campaign_id = l.campaign_id
GROUP BY c.channel
ORDER BY total_leads DESC;


-- =====================================================
-- 4. CONVERSIONS BY MARKETING CHANNEL
-- =====================================================

SELECT
    c.channel,
    COUNT(v.conversion_id) AS total_conversions
FROM campaigns c
LEFT JOIN leads l
    ON c.campaign_id = l.campaign_id
LEFT JOIN conversions v
    ON l.lead_id = v.lead_id
GROUP BY c.channel
ORDER BY total_conversions DESC;


-- =====================================================
-- 5. CHANNEL-WISE CONVERSION RATE
-- =====================================================

SELECT
    c.channel,
    COUNT(DISTINCT l.lead_id) AS total_leads,
    COUNT(v.conversion_id) AS total_conversions,
    ROUND(
        COUNT(v.conversion_id) * 100.0 /
        NULLIF(COUNT(DISTINCT l.lead_id), 0), 2
    ) AS conversion_rate_percentage
FROM campaigns c
LEFT JOIN leads l
    ON c.campaign_id = l.campaign_id
LEFT JOIN conversions v
    ON l.lead_id = v.lead_id
GROUP BY c.channel
ORDER BY conversion_rate_percentage DESC;


-- =====================================================
-- 6. CHANNEL-WISE CPL AND CAC
-- Aggregate each table before joining to avoid
-- multiplying spend by the number of leads.
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
channel_acquisition AS (
    SELECT
        c.channel,
        COUNT(DISTINCT l.lead_id) AS total_leads,
        COUNT(v.conversion_id) AS total_conversions
    FROM campaigns c
    LEFT JOIN leads l
        ON c.campaign_id = l.campaign_id
    LEFT JOIN conversions v
        ON l.lead_id = v.lead_id
    GROUP BY c.channel
)

SELECT
    a.channel,
    ROUND(COALESCE(s.total_spend, 0), 2) AS total_spend,
    a.total_leads,
    a.total_conversions,
    ROUND(
        s.total_spend / NULLIF(a.total_leads, 0), 2
    ) AS cost_per_lead,
    ROUND(
        s.total_spend / NULLIF(a.total_conversions, 0), 2
    ) AS customer_acquisition_cost
FROM channel_acquisition a
LEFT JOIN channel_spend s
    ON a.channel = s.channel
ORDER BY customer_acquisition_cost ASC;


-- =====================================================
-- 7. TOP 10 CAMPAIGNS BY LEAD GENERATION
-- =====================================================

SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    COUNT(l.lead_id) AS total_leads
FROM campaigns c
LEFT JOIN leads l
    ON c.campaign_id = l.campaign_id
GROUP BY
    c.campaign_id,
    c.campaign_name,
    c.channel
ORDER BY total_leads DESC
LIMIT 10;


-- =====================================================
-- 8. TOP 10 CAMPAIGNS BY CONVERSIONS
-- =====================================================

SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    COUNT(v.conversion_id) AS total_conversions
FROM campaigns c
LEFT JOIN leads l
    ON c.campaign_id = l.campaign_id
LEFT JOIN conversions v
    ON l.lead_id = v.lead_id
GROUP BY
    c.campaign_id,
    c.campaign_name,
    c.channel
ORDER BY total_conversions DESC
LIMIT 10;


-- =====================================================
-- 9. CAMPAIGN-LEVEL CONVERSION PERFORMANCE
-- =====================================================

SELECT
    c.campaign_id,
    c.campaign_name,
    c.channel,
    COUNT(DISTINCT l.lead_id) AS total_leads,
    COUNT(v.conversion_id) AS total_conversions,
    ROUND(
        COUNT(v.conversion_id) * 100.0 /
        NULLIF(COUNT(DISTINCT l.lead_id), 0), 2
    ) AS conversion_rate_percentage
FROM campaigns c
LEFT JOIN leads l
    ON c.campaign_id = l.campaign_id
LEFT JOIN conversions v
    ON l.lead_id = v.lead_id
GROUP BY
    c.campaign_id,
    c.campaign_name,
    c.channel
ORDER BY conversion_rate_percentage DESC;


-- =====================================================
-- 10. MONTHLY LEAD GENERATION
-- =====================================================

SELECT
    DATE_FORMAT(created_at, '%Y-%m') AS month,
    COUNT(*) AS total_leads
FROM leads
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY month;


-- =====================================================
-- 11. MONTHLY CONVERSION TREND
-- Uses conversion date, not lead creation date.
-- =====================================================

SELECT
    DATE_FORMAT(converted_at, '%Y-%m') AS month,
    COUNT(*) AS total_conversions,
    ROUND(SUM(revenue), 2) AS conversion_revenue
FROM conversions
GROUP BY DATE_FORMAT(converted_at, '%Y-%m')
ORDER BY month;


-- =====================================================
-- 12. CHANNEL ACQUISITION EFFICIENCY RANKING
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
channel_leads AS (
    SELECT
        c.channel,
        COUNT(l.lead_id) AS leads
    FROM campaigns c
    LEFT JOIN leads l
        ON c.campaign_id = l.campaign_id
    GROUP BY c.channel
),
channel_conversions AS (
    SELECT
        c.channel,
        COUNT(v.conversion_id) AS conversions
    FROM campaigns c
    LEFT JOIN leads l
        ON c.campaign_id = l.campaign_id
    LEFT JOIN conversions v
        ON l.lead_id = v.lead_id
    GROUP BY c.channel
),
metrics AS (
    SELECT
        s.channel,
        s.spend,
        l.leads,
        v.conversions,
        s.spend / NULLIF(v.conversions, 0) AS cac,
        v.conversions * 100.0 /
            NULLIF(l.leads, 0) AS conversion_rate
    FROM channel_spend s
    JOIN channel_leads l ON s.channel = l.channel
    JOIN channel_conversions v ON s.channel = v.channel
)

SELECT
    channel,
    ROUND(spend, 2) AS total_spend,
    leads AS total_leads,
    conversions AS total_conversions,
    ROUND(conversion_rate, 2) AS conversion_rate_percentage,
    ROUND(cac, 2) AS customer_acquisition_cost,
    RANK() OVER (
        ORDER BY cac ASC
    ) AS cac_rank,
    RANK() OVER (
        ORDER BY conversion_rate DESC
    ) AS conversion_rate_rank
FROM metrics
ORDER BY cac_rank;


-- =====================================================
-- END OF CUSTOMER ACQUISITION ANALYSIS
-- =====================================================
