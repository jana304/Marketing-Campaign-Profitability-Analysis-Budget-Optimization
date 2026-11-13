"""Starter profile for Marketing Campaigns & Conversions Dataset."""
import sqlite3
from pathlib import Path

database = next(Path(".").glob("*.sqlite"))
with sqlite3.connect(database) as connection:
    query = """WITH campaign_spend AS (
  SELECT campaign_id, SUM(spend) AS spend
  FROM daily_spend
  GROUP BY campaign_id
),
campaign_revenue AS (
  SELECT l.campaign_id, SUM(c.revenue) AS revenue
  FROM conversions c
  JOIN leads l USING (lead_id)
  GROUP BY l.campaign_id
)
SELECT c.channel,
       ROUND(SUM(COALESCE(s.spend, 0)), 2) AS spend,
       ROUND(SUM(COALESCE(r.revenue, 0)), 2) AS attributed_revenue
FROM campaigns c
LEFT JOIN campaign_spend s USING (campaign_id)
LEFT JOIN campaign_revenue r USING (campaign_id)
GROUP BY c.channel
ORDER BY attributed_revenue DESC;"""
    rows = connection.execute(query).fetchall()
    for row in rows:
        print(row)
