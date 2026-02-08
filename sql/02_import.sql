-- Data Import from CSV
-- Note: The CSV column names differ slightly from our schema:
--   CSV: IP, URL, utm_source, utm_campaign, threat_group, threat_type
--   Schema: ipv6_string, url_path, parsed_source, parsed_campaign, reason_threat_group, reason_threat_type
--
-- Import executed via Python script (import_data.py) to handle column mapping
-- Result: 126,959 rows imported successfully
--
-- To verify import:
SELECT COUNT(*) FROM cheq;
SELECT * FROM cheq LIMIT 5;
