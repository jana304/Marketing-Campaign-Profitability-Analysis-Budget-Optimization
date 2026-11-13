
CREATE DATABASE IF NOT EXISTS marketing_profitability_db;

USE marketing_profitability_db;

-- Table 1: Marketing Campaigns
CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id VARCHAR(20) PRIMARY KEY,
    campaign_name VARCHAR(150),
    channel VARCHAR(50),
    objective VARCHAR(50),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12,2)
);


-- Table 2: Daily Marketing Spend
CREATE TABLE IF NOT EXISTS daily_spend (
    spend_id VARCHAR(20) PRIMARY KEY,
    campaign_id VARCHAR(20),
    spend_date DATE,
    impressions INT,
    clicks INT,
    spend DECIMAL(12,2),
    FOREIGN KEY (campaign_id)
        REFERENCES campaigns(campaign_id)
);


-- Table 3: Marketing Conversions
CREATE TABLE IF NOT EXISTS conversions (
    conversion_id VARCHAR(20) PRIMARY KEY,
    lead_id VARCHAR(20),
    converted_at DATE,
    conversion_type VARCHAR(50),
    revenue DECIMAL(12,2)
);


-- Table 4: Marketing Leads
CREATE TABLE IF NOT EXISTS leads (
    lead_id VARCHAR(20) PRIMARY KEY,
    campaign_id VARCHAR(20),
    created_at DATE,
    lead_source VARCHAR(50),
    lead_score INT,
    FOREIGN KEY (campaign_id)
        REFERENCES campaigns(campaign_id)
);


-- Final Relationship: Conversions to Leads
ALTER TABLE conversions
ADD CONSTRAINT fk_conversions_leads
FOREIGN KEY (lead_id)
REFERENCES leads(lead_id);
