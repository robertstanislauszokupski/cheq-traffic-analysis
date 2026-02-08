"""
Core Analysis Results Exporter
Generates CSV reports for core analysis queries (1-3)
"""

from db_manager import DatabaseManager
import queries
import config

def main():
    db = DatabaseManager()
    
    # Export 1: Paid Traffic Summary
    print("Generating paid_traffic_summary.csv...")
    db.execute_to_csv(
        queries.PAID_TRAFFIC_RISK,
        config.PAID_TRAFFIC_CSV,
        queries.QUERY_HEADERS['paid_traffic']
    )
    
    # Export 2: Funnel Threats
    print("\nGenerating funnel_threats.csv...")
    db.execute_to_csv(
        queries.FUNNEL_EXPOSURE,
        config.FUNNEL_THREATS_CSV,
        queries.QUERY_HEADERS['funnel_exposure']
    )
    
    # Export 3: Threat Taxonomy
    print("\nGenerating threat_taxonomy.csv...")
    db.execute_to_csv(
        queries.THREAT_TAXONOMY,
        config.THREAT_TAXONOMY_CSV,
        queries.QUERY_HEADERS['threat_taxonomy']
    )
    
    print("\n" + "="*60)
    print("All exports complete! Files ready for presentation slides.")
    print("="*60)

if __name__ == '__main__':
    main()
