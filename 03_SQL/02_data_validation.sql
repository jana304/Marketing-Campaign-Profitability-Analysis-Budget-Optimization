
-- MARKETING_PROFITABILITY PROJECT
-- Phase 16: SQL Data Validation
-- Step 263: Verify Dataset Record Counts

USE marketing_profitability_db;

SELECT 'campaigns' AS table_name,
       COUNT(*) AS total_records
FROM campaigns

UNION ALL

SELECT 'daily_spend',
       COUNT(*)
FROM daily_spend

UNION ALL

SELECT 'leads',
       COUNT(*)
FROM leads

UNION ALL

SELECT 'conversions',
       COUNT(*)
FROM conversions;


-- Step 265: Check Missing Values in Campaigns

SELECT
    SUM(CASE WHEN campaign_id IS NULL THEN 1 ELSE 0 END)
        AS missing_campaign_id,
    SUM(CASE WHEN campaign_name IS NULL THEN 1 ELSE 0 END)
        AS missing_campaign_name,
    SUM(CASE WHEN channel IS NULL THEN 1 ELSE 0 END)
        AS missing_channel,
    SUM(CASE WHEN budget IS NULL THEN 1 ELSE 0 END)
        AS missing_budget
FROM campaigns;


-- Step 267: Check Missing Values in Daily Spend

SELECT
    SUM(CASE WHEN spend_id IS NULL THEN 1 ELSE 0 END)
        AS missing_spend_id,
    SUM(CASE WHEN campaign_id IS NULL THEN 1 ELSE 0 END)
        AS missing_campaign_id,
    SUM(CASE WHEN spend_date IS NULL THEN 1 ELSE 0 END)
        AS missing_spend_date,
    SUM(CASE WHEN impressions IS NULL THEN 1 ELSE 0 END)
        AS missing_impressions,
    SUM(CASE WHEN clicks IS NULL THEN 1 ELSE 0 END)
        AS missing_clicks,
    SUM(CASE WHEN spend IS NULL THEN 1 ELSE 0 END)
        AS missing_spend
FROM daily_spend;


-- Step 269: Check Missing Values in Leads

SELECT
    SUM(CASE WHEN lead_id IS NULL THEN 1 ELSE 0 END)
        AS missing_lead_id,
    SUM(CASE WHEN campaign_id IS NULL THEN 1 ELSE 0 END)
        AS missing_campaign_id,
    SUM(CASE WHEN created_at IS NULL THEN 1 ELSE 0 END)
        AS missing_created_at,
    SUM(CASE WHEN lead_source IS NULL THEN 1 ELSE 0 END)
        AS missing_lead_source,
    SUM(CASE WHEN lead_score IS NULL THEN 1 ELSE 0 END)
        AS missing_lead_score
FROM leads;


-- Step 271: Check Missing Values in Conversions

SELECT
    SUM(CASE WHEN conversion_id IS NULL THEN 1 ELSE 0 END)
        AS missing_conversion_id,
    SUM(CASE WHEN lead_id IS NULL THEN 1 ELSE 0 END)
        AS missing_lead_id,
    SUM(CASE WHEN converted_at IS NULL THEN 1 ELSE 0 END)
        AS missing_converted_at,
    SUM(CASE WHEN conversion_type IS NULL THEN 1 ELSE 0 END)
        AS missing_conversion_type,
    SUM(CASE WHEN revenue IS NULL THEN 1 ELSE 0 END)
        AS missing_revenue
FROM conversions;


-- Step 273: Check Duplicate Campaign IDs

SELECT
    campaign_id,
    COUNT(*) AS duplicate_count
FROM campaigns
GROUP BY campaign_id
HAVING COUNT(*) > 1;


-- Step 275: Check Duplicate Spend IDs

SELECT
    spend_id,
    COUNT(*) AS duplicate_count
FROM daily_spend
GROUP BY spend_id
HAVING COUNT(*) > 1;


-- Step 277: Check Duplicate Lead IDs

SELECT
    lead_id,
    COUNT(*) AS duplicate_count
FROM leads
GROUP BY lead_id
HAVING COUNT(*) > 1;


-- Step 279: Check Duplicate Conversion IDs

SELECT
    conversion_id,
    COUNT(*) AS duplicate_count
FROM conversions
GROUP BY conversion_id
HAVING COUNT(*) > 1;


-- Step 281: Check Referential Integrity
-- Verify daily_spend campaign references

SELECT
    COUNT(*) AS orphan_spend_records
FROM daily_spend d
LEFT JOIN campaigns c
    ON d.campaign_id = c.campaign_id
WHERE c.campaign_id IS NULL;


-- Step 283: Check Referential Integrity
-- Verify leads campaign references

SELECT
    COUNT(*) AS orphan_lead_records
FROM leads l
LEFT JOIN campaigns c
    ON l.campaign_id = c.campaign_id
WHERE c.campaign_id IS NULL;


-- Step 285: Check Referential Integrity
-- Verify conversions reference valid leads

SELECT
    COUNT(*) AS orphan_conversion_records
FROM conversions c
LEFT JOIN leads l
    ON c.lead_id = l.lead_id
WHERE l.lead_id IS NULL;


-- Step 287: Check Negative Marketing Spend

SELECT
    COUNT(*) AS negative_spend_records
FROM daily_spend
WHERE spend < 0;


USE marketing_profitability_db;

SELECT
    (SELECT COUNT(*) FROM daily_spend
     WHERE spend = 0) AS zero_spend,

    (SELECT COUNT(*) FROM daily_spend
     WHERE impressions < 0 OR clicks < 0)
     AS negative_traffic,

    (SELECT COUNT(*) FROM daily_spend
     WHERE clicks > impressions)
     AS invalid_clicks,

    (SELECT COUNT(*) FROM conversions
     WHERE revenue < 0)
     AS negative_revenue,

    (SELECT COUNT(*) FROM campaigns
     WHERE budget < 0)
     AS negative_budget,

    (SELECT COUNT(*) FROM leads
     WHERE lead_score < 0 OR lead_score > 100)
     AS invalid_lead_scores;
