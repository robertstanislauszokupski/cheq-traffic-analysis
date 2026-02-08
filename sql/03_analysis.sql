-- ============================================================================
-- CHEQ TRIAL DATA ANALYSIS
-- 126,959 events analyzed
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 1: Overall Traffic Health
-- Baseline risk level during trial period
-- ----------------------------------------------------------------------------
SELECT
  COUNT(*) AS total_events,
  SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq;

-- ----------------------------------------------------------------------------
-- Query 2: Funnel Exposure by Page
-- Shows where abuse concentrates in the customer journey
-- ----------------------------------------------------------------------------
SELECT
  url_path,
  COUNT(*) AS total_events,
  SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
GROUP BY url_path
ORDER BY invalid_events DESC;

-- ----------------------------------------------------------------------------
-- Query 3: Paid Traffic Risk Analysis
-- Critical for understanding wasted ad spend
-- ----------------------------------------------------------------------------
SELECT
  CASE
    WHEN gclid IS NOT NULL AND gclid != '' THEN 'Google Ads'
    WHEN msclkid IS NOT NULL AND msclkid != '' THEN 'Bing Ads'
    ELSE 'Organic / Direct'
  END AS traffic_source,
  COUNT(*) AS total_events,
  SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
GROUP BY traffic_source
ORDER BY invalid_events DESC;

-- ----------------------------------------------------------------------------
-- Query 4: Threat Taxonomy
-- What kind of bad traffic is actually hitting the site
-- ----------------------------------------------------------------------------
SELECT
  reason_threat_group,
  reason_threat_type,
  COUNT(*) AS events,
  ROUND(
    100.0 * COUNT(*) / (SELECT COUNT(*) FROM cheq WHERE reason_threat_group IS NOT NULL AND reason_threat_group != ''),
    2
  ) AS pct_of_invalid
FROM cheq
WHERE reason_threat_group IS NOT NULL AND reason_threat_group != ''
GROUP BY reason_threat_group, reason_threat_type
ORDER BY events DESC;

-- ----------------------------------------------------------------------------
-- Query 5: Geo/Device Mismatch Signal
-- Detects VPNs, emulators, automation patterns
-- ----------------------------------------------------------------------------
SELECT
  ip_timezone,
  device_timezone,
  COUNT(*) AS events,
  SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
WHERE ip_timezone != device_timezone 
  AND ip_timezone IS NOT NULL 
  AND device_timezone IS NOT NULL
GROUP BY ip_timezone, device_timezone
ORDER BY events DESC
LIMIT 20;

-- ============================================================================
-- ADVANCED ANALYSIS QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 6: ASN/ISP Analysis
-- Identifies which hosting providers and ISPs generate the most invalid traffic
-- Critical for IP blocking and firewall rules
-- ----------------------------------------------------------------------------
SELECT
  ASN,
  COUNT(*) AS total_events,
  SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
WHERE ASN IS NOT NULL AND ASN != ''
GROUP BY ASN
ORDER BY invalid_events DESC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- Query 7: User Agent Analysis
-- Detects automation tools, scrapers, and suspicious browser patterns
-- ----------------------------------------------------------------------------
SELECT
  CASE
    WHEN Useragent LIKE '%HeadlessChrome%' THEN 'Headless Chrome (Bot)'
    WHEN Useragent LIKE '%Phantom%' THEN 'PhantomJS (Bot)'
    WHEN Useragent LIKE '%Selenium%' THEN 'Selenium (Automation)'
    WHEN Useragent LIKE '%bot%' OR Useragent LIKE '%Bot%' THEN 'Known Bot'
    WHEN Useragent LIKE '%curl%' OR Useragent LIKE '%wget%' THEN 'CLI Tool'
    WHEN Useragent LIKE '%Python%' THEN 'Python Script'
    WHEN Useragent LIKE '%Chrome%' THEN 'Chrome Browser'
    WHEN Useragent LIKE '%Firefox%' THEN 'Firefox Browser'
    WHEN Useragent LIKE '%Safari%' AND Useragent NOT LIKE '%Chrome%' THEN 'Safari Browser'
    WHEN Useragent LIKE '%Edge%' THEN 'Edge Browser'
    WHEN Useragent IS NULL OR Useragent = '' THEN 'Missing UA'
    ELSE 'Other'
  END AS user_agent_type,
  COUNT(*) AS total_events,
  SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
GROUP BY user_agent_type
ORDER BY invalid_events DESC;

-- ----------------------------------------------------------------------------
-- Query 8: Time-Based Pattern Analysis (Hourly)
-- Identifies attack waves and unusual traffic patterns by hour of day
-- ----------------------------------------------------------------------------
SELECT
  CAST(substr(timestamp, instr(timestamp, ' ') + 1, 2) AS INTEGER) AS hour_of_day,
  COUNT(*) AS total_events,
  SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
WHERE instr(timestamp, ' ') > 0
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- ----------------------------------------------------------------------------
-- Query 9: Time-Based Pattern Analysis (Daily)
-- Shows day-over-day trends in attack volume
-- ----------------------------------------------------------------------------
SELECT
  substr(timestamp, 1, instr(timestamp, ' ') - 1) AS date,
  COUNT(*) AS total_events,
  SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
WHERE instr(timestamp, ' ') > 0
GROUP BY date
ORDER BY date;
