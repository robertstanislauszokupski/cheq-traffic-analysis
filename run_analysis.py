"""
Core Analysis Runner
Executes all 5 core analysis queries and displays results
"""

from db_manager import DatabaseManager
import queries
import config

def main():
    db = DatabaseManager()
    
    print("="*80)
    print("CHEQ TRIAL DATA ANALYSIS - RESULTS")
    print("="*80)
    
    # Query 1: Overall Traffic Health
    print("\n" + "="*80)
    print("1. OVERALL TRAFFIC HEALTH")
    print("="*80)
    row = db.execute_query_single(queries.OVERALL_HEALTH)
    print(f"Total Events: {row[0]:,}")
    print(f"Invalid Events: {row[1]:,}")
    print(f"Invalid %: {row[2]}%")
    
    # Query 2: Funnel Exposure (Top 10)
    print("\n" + "="*80)
    print("2. FUNNEL EXPOSURE BY PAGE (Top 10)")
    print("="*80)
    rows = db.execute_query(queries.FUNNEL_EXPOSURE + f" LIMIT {config.TOP_N_RESULTS}")
    print(f"{'URL Path':<50} {'Total':<10} {'Invalid':<10} {'%':<8}")
    print("-"*80)
    for row in rows:
        url = row[0][:47] + '...' if len(row[0]) > 50 else row[0]
        print(f"{url:<50} {row[1]:<10,} {row[2]:<10,} {row[3]:<8}%")
    
    # Query 3: Paid Traffic Risk
    print("\n" + "="*80)
    print("3. PAID TRAFFIC RISK (Wasted Ad Spend)")
    print("="*80)
    rows = db.execute_query(queries.PAID_TRAFFIC_RISK)
    print(f"{'Source':<20} {'Total':<12} {'Invalid':<12} {'%':<8}")
    print("-"*80)
    for row in rows:
        print(f"{row[0]:<20} {row[1]:<12,} {row[2]:<12,} {row[3]:<8}%")
    
    # Query 4: Threat Taxonomy (Top 10)
    print("\n" + "="*80)
    print("4. THREAT TAXONOMY (Top 10)")
    print("="*80)
    rows = db.execute_query(queries.THREAT_TAXONOMY + f" LIMIT {config.TOP_N_RESULTS}")
    print(f"{'Threat Group':<25} {'Threat Type':<30} {'Events':<10} {'%':<8}")
    print("-"*80)
    for row in rows:
        group = row[0] if row[0] else 'N/A'
        type_ = row[1] if row[1] else 'N/A'
        print(f"{group:<25} {type_:<30} {row[2]:<10,} {row[3]:<8}%")
    
    # Query 5: Geo/Device Mismatch (Top 10)
    print("\n" + "="*80)
    print("5. GEO/DEVICE TIMEZONE MISMATCHES (Top 10)")
    print("="*80)
    rows = db.execute_query(queries.GEO_DEVICE_MISMATCH)
    print(f"{'IP Timezone':<25} {'Device Timezone':<25} {'Events':<10} {'Invalid':<10} {'%':<8}")
    print("-"*80)
    for row in rows:
        print(f"{row[0]:<25} {row[1]:<25} {row[2]:<10,} {row[3]:<10,} {row[4]:<8}%")
    
    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)

if __name__ == '__main__':
    main()
