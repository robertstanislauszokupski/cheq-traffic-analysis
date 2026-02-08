"""
Advanced Analysis Exporter
Generates CSV reports for ASN, User Agent, and Time-based analyses
"""

from db_manager import DatabaseManager
import queries
import config

def main():
    db = DatabaseManager()
    
    print("="*80)
    print("ADVANCED ANALYSIS EXPORTS")
    print("="*80)
    
    # Export 1: ASN/ISP Analysis
    print("\n1. Generating asn_analysis.csv...")
    db.execute_to_csv(
        queries.ASN_ANALYSIS,
        config.ASN_ANALYSIS_CSV,
        queries.QUERY_HEADERS['asn_analysis']
    )
    
    # Export 2: User Agent Analysis
    print("\n2. Generating user_agent_analysis.csv...")
    db.execute_to_csv(
        queries.USER_AGENT_ANALYSIS,
        config.USER_AGENT_CSV,
        queries.QUERY_HEADERS['user_agent']
    )
    
    # Export 3: Hourly Pattern Analysis
    print("\n3. Generating hourly_patterns.csv...")
    db.execute_to_csv(
        queries.HOURLY_PATTERNS,
        config.HOURLY_PATTERNS_CSV,
        queries.QUERY_HEADERS['hourly_patterns']
    )
    
    # Export 4: Daily Pattern Analysis
    print("\n4. Generating daily_patterns.csv...")
    db.execute_to_csv(
        queries.DAILY_PATTERNS,
        config.DAILY_PATTERNS_CSV,
        queries.QUERY_HEADERS['daily_patterns']
    )
    
    # Summary stats
    print("\n" + "="*80)
    print("ADVANCED ANALYSIS SUMMARY")
    print("="*80)
    
    # Top ASN
    top_asn_query = f"""
    SELECT ASN, COUNT(*) as cnt 
    FROM cheq 
    WHERE {queries.invalid_condition()}
      AND ASN IS NOT NULL AND ASN != ''
    GROUP BY ASN 
    ORDER BY cnt DESC 
    LIMIT 1
    """
    top_asn = db.execute_query_single(top_asn_query)
    if top_asn:
        print(f"\nTop Threat ASN: {top_asn[0]} ({top_asn[1]:,} invalid events)")
    
    # Most suspicious UA
    top_ua_query = f"""
    SELECT 
      CASE
        WHEN Useragent LIKE '%HeadlessChrome%' THEN 'Headless Chrome'
        WHEN Useragent LIKE '%Phantom%' THEN 'PhantomJS'
        WHEN Useragent LIKE '%Selenium%' THEN 'Selenium'
        WHEN Useragent LIKE '%bot%' OR Useragent LIKE '%Bot%' THEN 'Known Bot'
        ELSE 'Other'
      END AS ua_type,
      COUNT(*) as cnt
    FROM cheq
    WHERE {queries.invalid_condition()}
      AND (Useragent LIKE '%Headless%' OR Useragent LIKE '%Phantom%' 
           OR Useragent LIKE '%Selenium%' OR Useragent LIKE '%bot%')
    GROUP BY ua_type
    ORDER BY cnt DESC
    LIMIT 1
    """
    top_ua = db.execute_query_single(top_ua_query)
    if top_ua:
        print(f"Most Common Automation Tool: {top_ua[0]} ({top_ua[1]:,} events)")
    
    # Peak attack hour
    peak_hour_query = f"""
    SELECT CAST(substr(timestamp, instr(timestamp, ' ') + 1, 2) AS INTEGER) as hr, COUNT(*) as cnt
    FROM cheq
    WHERE {queries.invalid_condition()}
      AND instr(timestamp, ' ') > 0
    GROUP BY hr
    ORDER BY cnt DESC
    LIMIT 1
    """
    peak_hour = db.execute_query_single(peak_hour_query)
    if peak_hour:
        print(f"⏰ Peak Attack Hour: {peak_hour[0]}:00 UTC ({peak_hour[1]:,} invalid events)")
    
    print("\n" + "="*80)
    print("All advanced exports complete!")
    print("="*80)

if __name__ == '__main__':
    main()
