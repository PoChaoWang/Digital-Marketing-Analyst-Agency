-- Build table_360 from Google Ads, Meta Ads, and GA4 raw CSV views using DuckDB.

CREATE TABLE table_360 AS
WITH google_ads AS (
    SELECT
        CAST(date AS DATE) AS date,
        'google_ads' AS platform,
        campaign_name,
        ad_group AS ad_group_name,
        ad_name,
        CAST(impressions AS BIGINT) AS impressions,
        CAST(clicks AS BIGINT) AS clicks,
        CAST(spend AS DOUBLE) AS spend,
        CAST(conversions AS DOUBLE) AS conversions,
        CAST(conversion_value AS DOUBLE) AS revenue,
        'google_ads' AS source,
        CASE
            WHEN LOWER(campaign_name) LIKE '%dynamic%' THEN 'dynamic'
            WHEN LOWER(campaign_name) LIKE '%retargeting%' THEN 'retargeting'
            WHEN LOWER(campaign_name) LIKE '%prospecting%' THEN 'prospecting'
            ELSE 'unknown'
        END AS campaign_type,
        CASE
            WHEN LOWER(campaign_name) LIKE '%pmax%' THEN 'Performance Max'
            WHEN LOWER(campaign_name) LIKE '%performance%' THEN 'Performance Max'
            WHEN LOWER(campaign_name) LIKE '%sho%' THEN 'Shopping'
            WHEN LOWER(campaign_name) LIKE '%shopping%' THEN 'Shopping'
            WHEN LOWER(campaign_name) LIKE '%gdn%' THEN 'Display'
            WHEN LOWER(campaign_name) LIKE '%display%' THEN 'Display'
            WHEN LOWER(campaign_name) LIKE '%youtube%' THEN 'YouTube'
            ELSE 'unknown'
        END AS ad_type
    FROM google_ads_raw
),
meta_ads AS (
    SELECT
        CAST(date AS DATE) AS date,
        'meta_ads' AS platform,
        campaign_name,
        ad_set AS ad_group_name,
        ad_name,
        CAST(impressions AS BIGINT) AS impressions,
        CAST(clicks AS BIGINT) AS clicks,
        CAST(spend AS DOUBLE) AS spend,
        CAST(conversions AS DOUBLE) AS conversions,
        CAST(conversion_value AS DOUBLE) AS revenue,
        'meta_ads' AS source,
        CASE
            WHEN LOWER(campaign_name) LIKE '%dynamic%' THEN 'dynamic'
            WHEN LOWER(campaign_name) LIKE '%retargeting%' THEN 'retargeting'
            WHEN LOWER(campaign_name) LIKE '%prospecting%' THEN 'prospecting'
            ELSE 'unknown'
        END AS campaign_type,
        CASE
            WHEN LOWER(ad_set) LIKE '%image%' THEN 'Single Image'
            WHEN LOWER(ad_set) LIKE '%img%' THEN 'Single Image'
            WHEN LOWER(ad_set) LIKE '%video%' THEN 'Video'
            WHEN LOWER(ad_set) LIKE '%vid%' THEN 'Video'
            WHEN LOWER(ad_set) LIKE '%collection%' THEN 'Collection'
            WHEN LOWER(ad_set) LIKE '%col%' THEN 'Collection'
            WHEN LOWER(ad_set) LIKE '%carousel%' THEN 'Carousel'
            WHEN LOWER(ad_set) LIKE '%car%' THEN 'Carousel'
            WHEN LOWER(ad_set) LIKE '%dynamic%' THEN 'Dynamic'
            ELSE 'unknown'
        END AS ad_type
    FROM meta_ads_raw
),
ads_unified AS (
    SELECT * FROM google_ads
    UNION ALL
    SELECT * FROM meta_ads
),
ga4 AS (
    SELECT
        utm_campaign,
        utm_id,
        utm_content,
        SUM(CAST(users AS BIGINT)) AS ga4_users,
        SUM(CAST(new_users AS BIGINT)) AS ga4_new_users,
        SUM(CAST(conversions AS DOUBLE)) AS ga4_conversions,
        SUM(CAST(revenue AS DOUBLE)) AS ga4_revenue
    FROM ga4_raw
    GROUP BY
        utm_campaign,
        utm_id,
        utm_content
)
SELECT
    ads_unified.date,
    -- ads_unified.platform,
    ads_unified.source,
    ads_unified.campaign_name,
    ads_unified.ad_group_name,
    ads_unified.ad_name,
    ads_unified.campaign_type, 
    ads_unified.ad_type,       
    ads_unified.impressions,
    ads_unified.clicks,
    ads_unified.spend,
    ads_unified.conversions,
    ads_unified.revenue,
    COALESCE(ga4.ga4_users, 0) AS ga4_users,
    COALESCE(ga4.ga4_new_users, 0) AS ga4_new_users,
    COALESCE(ga4.ga4_conversions, 0) AS ga4_conversions,
    COALESCE(ga4.ga4_revenue, 0) AS ga4_revenue,
    'csv' AS source_type,
    -- ads_unified.platform AS platform_name,
    -- '' AS source_file,
    'default_csv' AS source_priority,
    now() AS loaded_at
FROM ads_unified
LEFT JOIN ga4
    ON ads_unified.campaign_name = ga4.utm_campaign
   AND ads_unified.ad_group_name = ga4.utm_id
   AND ads_unified.ad_name = ga4.utm_content;
