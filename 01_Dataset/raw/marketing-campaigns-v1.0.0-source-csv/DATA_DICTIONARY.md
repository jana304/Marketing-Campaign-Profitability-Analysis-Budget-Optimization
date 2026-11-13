# Marketing Campaigns & Conversions Dataset data dictionary

Version: 1.0.0  
Coverage: 2023-01-01 through 2025-12-31  
Source type: synthetic

## `campaigns`

Grain: One row per campaign.
| Column | Type | Nullable | Description |
|---|---|---:|---|
| `campaign_id` | text | no | Stable campaign key. |
| `campaign_name` | text | no | Display name. |
| `channel` | text | no | Paid media channel. |
| `objective` | text | no | Awareness, lead_gen, or acquisition. |
| `start_date` | date | no | First active date. |
| `end_date` | date | no | Last active date. |
| `budget` | decimal | no | Planned campaign budget. |

## `daily_spend`

Grain: One row per campaign active date.
| Column | Type | Nullable | Description |
|---|---|---:|---|
| `spend_id` | text | no | Stable delivery key. |
| `campaign_id` | text | no | Delivered campaign. |
| `spend_date` | date | no | Delivery date. |
| `impressions` | integer | no | Served impressions. |
| `clicks` | integer | no | Recorded clicks. |
| `spend` | decimal | no | Media cost. |

## `leads`

Grain: One row per lead.
| Column | Type | Nullable | Description |
|---|---|---:|---|
| `lead_id` | text | no | Stable lead key. |
| `campaign_id` | text | no | Attributed campaign. |
| `created_at` | date | no | Lead creation date. |
| `lead_source` | text | no | Attributed source channel. |
| `lead_score` | integer | no | Qualification score from 1 to 100. |

## `conversions`

Grain: One row per converted lead.
| Column | Type | Nullable | Description |
|---|---|---:|---|
| `conversion_id` | text | no | Stable conversion key. |
| `lead_id` | text | no | Converted lead. |
| `converted_at` | date | no | Conversion date. |
| `conversion_type` | text | no | trial or purchase. |
| `revenue` | decimal | no | Attributed revenue. |

## Relationships

- `daily_spend.campaign_id` → `campaigns.campaign_id` (many-to-one)
- `leads.campaign_id` → `campaigns.campaign_id` (many-to-one)
- `conversions.lead_id` → `leads.lead_id` (one-to-one)
