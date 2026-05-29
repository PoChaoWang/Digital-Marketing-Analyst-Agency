-- Build exports/360_table.csv from staged paid media and GA4 rows.
--
-- The runner loads these staging tables before executing this SQL:
-- - paid_raw
-- - ga4_raw
-- - priority_overrides
--
-- Grain:
-- date + platform + campaign_name + ad_group_name + ad_name
--
-- Source priority:
-- - Default: MCP wins over CSV.
-- - Override: priority_overrides can prefer csv or mcp for a specific
--   date + platform.
--
-- GA4 join:
-- - utm_campaign -> campaign_name
-- - utm_id -> ad_group_name
-- - utm_content -> ad_name
-- - GA4 is left joined to paid media rows.

DROP TABLE IF EXISTS paid_ranked;
CREATE TEMP TABLE paid_ranked AS
WITH normalized AS (
  SELECT
    date,
    platform,
    platform AS source,
    campaign_name,
    ad_group_name,
    ad_name,
    SUM(impressions) AS impressions,
    SUM(clicks) AS clicks,
    SUM(spend) AS spend,
    SUM(conversions) AS conversions,
    SUM(revenue) AS revenue,
    source_type,
    platform_name,
    source_file,
    loaded_at
  FROM paid_raw
  GROUP BY
    date,
    platform,
    campaign_name,
    ad_group_name,
    ad_name,
    source_type,
    platform_name,
    source_file,
    loaded_at
),
ranked AS (
  SELECT
    normalized.*,
    CASE
      WHEN priority_overrides.prefer = normalized.source_type THEN
        'user_override_' || normalized.source_type
      WHEN normalized.source_type = 'mcp' THEN
        'default_mcp'
      ELSE
        'default_csv'
    END AS source_priority,
    ROW_NUMBER() OVER (
      PARTITION BY
        normalized.date,
        normalized.platform,
        normalized.campaign_name,
        normalized.ad_group_name,
        normalized.ad_name
      ORDER BY
        CASE
          WHEN priority_overrides.prefer = normalized.source_type THEN 0
          WHEN normalized.source_type = 'mcp' THEN 10
          WHEN normalized.source_type = 'csv' THEN 20
          ELSE 99
        END,
        normalized.loaded_at DESC,
        normalized.source_file ASC
    ) AS source_rank
  FROM normalized
  LEFT JOIN priority_overrides
    ON priority_overrides.date = normalized.date
   AND priority_overrides.platform = normalized.platform
)
SELECT * FROM ranked;

DROP TABLE IF EXISTS paid_deduped;
CREATE TEMP TABLE paid_deduped AS
SELECT
  date,
  source,
  platform,
  campaign_name,
  ad_group_name,
  ad_name,
  impressions,
  clicks,
  spend,
  conversions,
  revenue,
  source_type,
  platform_name,
  source_file,
  source_priority,
  loaded_at
FROM paid_ranked
WHERE source_rank = 1;

DROP TABLE IF EXISTS ga4_agg;
CREATE TEMP TABLE ga4_agg AS
SELECT
  date,
  CASE
    WHEN LOWER(COALESCE(utm_source, source)) IN ('google', 'google_ads', 'google ads') THEN 'google_ads'
    WHEN LOWER(COALESCE(utm_source, source)) IN ('meta', 'facebook', 'instagram', 'meta_ads', 'meta ads') THEN 'meta_ads'
    ELSE LOWER(COALESCE(platform_source, utm_source, source, 'unknown'))
  END AS platform,
  COALESCE(NULLIF(utm_campaign, ''), NULLIF(campaign, ''), 'unknown') AS campaign_name,
  COALESCE(NULLIF(utm_id, ''), 'unknown') AS ad_group_name,
  COALESCE(NULLIF(utm_content, ''), 'unknown') AS ad_name,
  SUM(users) AS ga4_users,
  SUM(new_users) AS ga4_new_users,
  SUM(conversions) AS ga4_conversions,
  SUM(revenue) AS ga4_revenue
FROM ga4_raw
GROUP BY
  date,
  platform,
  campaign_name,
  ad_group_name,
  ad_name;

DROP TABLE IF EXISTS table_360;
CREATE TABLE table_360 AS
SELECT
  paid_deduped.date,
  paid_deduped.source,
  paid_deduped.platform,
  paid_deduped.campaign_name,
  paid_deduped.ad_group_name,
  paid_deduped.ad_name,
  paid_deduped.impressions,
  paid_deduped.clicks,
  paid_deduped.spend,
  paid_deduped.conversions,
  paid_deduped.revenue,
  COALESCE(ga4_agg.ga4_users, 0) AS ga4_users,
  COALESCE(ga4_agg.ga4_new_users, 0) AS ga4_new_users,
  COALESCE(ga4_agg.ga4_conversions, 0) AS ga4_conversions,
  COALESCE(ga4_agg.ga4_revenue, 0) AS ga4_revenue,
  paid_deduped.source_type,
  paid_deduped.platform_name,
  paid_deduped.source_file,
  paid_deduped.source_priority,
  paid_deduped.loaded_at
FROM paid_deduped
LEFT JOIN ga4_agg
  ON ga4_agg.date = paid_deduped.date
 AND ga4_agg.platform = paid_deduped.platform
 AND ga4_agg.campaign_name = paid_deduped.campaign_name
 AND ga4_agg.ad_group_name = paid_deduped.ad_group_name
 AND ga4_agg.ad_name = paid_deduped.ad_name
ORDER BY
  paid_deduped.date,
  paid_deduped.platform,
  paid_deduped.campaign_name,
  paid_deduped.ad_group_name,
  paid_deduped.ad_name;
