"""
Centralized SQL Queries for CHEQ Analysis
All analysis queries in one place for maintainability
"""

# Helper function for invalid traffic condition
def invalid_condition():
    """Returns the SQL condition to check if traffic is invalid"""
    return "reason_threat_group IS NOT NULL AND reason_threat_group != ''"


# ============================================================================
# CORE ANALYSIS QUERIES (Queries 1-5)
# ============================================================================

OVERALL_HEALTH = f"""
SELECT
  COUNT(*) AS total_events,
  SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
"""

FUNNEL_EXPOSURE = f"""
SELECT
  url_path,
  COUNT(*) AS total_events,
  SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
GROUP BY url_path
ORDER BY invalid_events DESC
"""

PAID_TRAFFIC_RISK = f"""
SELECT
  CASE
    WHEN gclid IS NOT NULL AND gclid != '' THEN 'Google Ads'
    WHEN msclkid IS NOT NULL AND msclkid != '' THEN 'Bing Ads'
    ELSE 'Organic / Direct'
  END AS traffic_source,
  COUNT(*) AS total_events,
  SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
GROUP BY traffic_source
ORDER BY invalid_events DESC
"""

THREAT_TAXONOMY = f"""
SELECT
  reason_threat_group,
  reason_threat_type,
  COUNT(*) AS events,
  ROUND(
    100.0 * COUNT(*) / (SELECT COUNT(*) FROM cheq WHERE {invalid_condition()}),
    2
  ) AS pct_of_invalid
FROM cheq
WHERE {invalid_condition()}
GROUP BY reason_threat_group, reason_threat_type
ORDER BY events DESC
"""

GEO_DEVICE_MISMATCH = f"""
SELECT
  ip_timezone,
  device_timezone,
  COUNT(*) AS events,
  SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
WHERE ip_timezone != device_timezone 
  AND ip_timezone IS NOT NULL 
  AND device_timezone IS NOT NULL
GROUP BY ip_timezone, device_timezone
ORDER BY events DESC
LIMIT 20
"""

# ============================================================================
# ADVANCED ANALYSIS QUERIES (Queries 6-9)
# ============================================================================

ASN_ANALYSIS = f"""
SELECT
  ASN,
  COUNT(*) AS total_events,
  SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
WHERE ASN IS NOT NULL AND ASN != ''
GROUP BY ASN
ORDER BY invalid_events DESC
LIMIT 30
"""

USER_AGENT_ANALYSIS = f"""
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
  SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
GROUP BY user_agent_type
ORDER BY invalid_events DESC
"""

HOURLY_PATTERNS = f"""
SELECT
  CAST(substr(timestamp, instr(timestamp, ' ') + 1, 2) AS INTEGER) AS hour_of_day,
  COUNT(*) AS total_events,
  SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
WHERE instr(timestamp, ' ') > 0
GROUP BY hour_of_day
ORDER BY hour_of_day
"""

DAILY_PATTERNS = f"""
SELECT
  substr(timestamp, 1, instr(timestamp, ' ') - 1) AS date,
  COUNT(*) AS total_events,
  SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) AS invalid_events,
  ROUND(
    100.0 * SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS invalid_pct
FROM cheq
WHERE instr(timestamp, ' ') > 0
GROUP BY date
ORDER BY date
"""

# ============================================================================
# VISUALIZATION QUERIES
# ============================================================================

THREAT_TYPE_DISTRIBUTION = f"""
SELECT
  reason_threat_type,
  COUNT(*) AS events
FROM cheq
WHERE {invalid_condition()}
GROUP BY reason_threat_type
ORDER BY events DESC
LIMIT 8
"""

TOP_ASNS = f"""
SELECT
  ASN,
  SUM(CASE WHEN {invalid_condition()} THEN 1 ELSE 0 END) AS invalid_events
FROM cheq
WHERE ASN IS NOT NULL AND ASN != ''
GROUP BY ASN
ORDER BY invalid_events DESC
LIMIT 10
"""

# ============================================================================
# QUERY METADATA
# ============================================================================

QUERY_HEADERS = {
    'overall_health': ['Total Events', 'Invalid Events', 'Invalid %'],
    'funnel_exposure': ['URL Path', 'Total Events', 'Invalid Events', 'Invalid %'],
    'paid_traffic': ['Traffic Source', 'Total Events', 'Invalid Events', 'Invalid %'],
    'threat_taxonomy': ['Threat Group', 'Threat Type', 'Events', '% of Invalid'],
    'geo_mismatch': ['IP Timezone', 'Device Timezone', 'Events', 'Invalid Events', 'Invalid %'],
    'asn_analysis': ['ASN', 'Total Events', 'Invalid Events', 'Invalid %'],
    'user_agent': ['User Agent Type', 'Total Events', 'Invalid Events', 'Invalid %'],
    'hourly_patterns': ['Hour (24h)', 'Total Events', 'Invalid Events', 'Invalid %'],
    'daily_patterns': ['Date', 'Total Events', 'Invalid Events', 'Invalid %'],
}
