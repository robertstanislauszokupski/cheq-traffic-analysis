"""
CHEQ Cost Calculator - ROI Analysis Tool
Interactive calculator for estimating wasted ad spend and CHEQ ROI
"""

from db_manager import DatabaseManager
import queries
import config
import sys
import csv

def get_traffic_data():
    """Fetch invalid traffic data from database"""
    db = DatabaseManager()
    results_list = db.execute_query(queries.PAID_TRAFFIC_RISK)
    results = {row[0]: {'total': row[1], 'invalid': row[2]} for row in results_list}
    return results

def calculate_costs(traffic_data, google_cpc, bing_cpc):
    """Calculate wasted ad spend based on CPC rates"""
    google_waste = traffic_data.get('Google Ads', {}).get('invalid', 0) * google_cpc
    bing_waste = traffic_data.get('Bing Ads', {}).get('invalid', 0) * bing_cpc
    total_waste = google_waste + bing_waste
    
    return {
        'google_waste': google_waste,
        'bing_waste': bing_waste,
        'total_waste': total_waste,
        'google_clicks': traffic_data.get('Google Ads', {}).get('invalid', 0),
        'bing_clicks': traffic_data.get('Bing Ads', {}).get('invalid', 0)
    }

def calculate_roi(total_waste, cheq_monthly_cost, trial_days=31):
    """Calculate ROI of CHEQ deployment"""
    monthly_savings = (total_waste / trial_days) * 30
    annual_savings = monthly_savings * 12
    monthly_roi = ((monthly_savings - cheq_monthly_cost) / cheq_monthly_cost) * 100 if cheq_monthly_cost > 0 else 0
    payback_days = (cheq_monthly_cost / (total_waste / trial_days)) if total_waste > 0 else 0
    
    return {
        'monthly_savings': monthly_savings,
        'annual_savings': annual_savings,
        'monthly_roi': monthly_roi,
        'payback_days': payback_days
    }

def main():
    print("="*80)
    print("CHEQ COST CALCULATOR - ROI ANALYSIS")
    print("="*80)
    
    # Fetch data
    print("\nLoading trial data from database...")
    traffic_data = get_traffic_data()
    
    print(f"\nTrial Period Invalid Traffic Summary:")
    print(f"  Google Ads: {traffic_data.get('Google Ads', {}).get('invalid', 0):,} invalid clicks")
    print(f"  Bing Ads: {traffic_data.get('Bing Ads', {}).get('invalid', 0):,} invalid clicks")
    
    # Interactive mode
    print("\n" + "="*80)
    print("COST CALCULATION")
    print("="*80)
    
    try:
        # Get CPC rates
        google_cpc = float(input("\nEnter your average Google Ads CPC (e.g., 2.50): $"))
        bing_cpc = float(input("Enter your average Bing Ads CPC (e.g., 1.80): $"))
        
        # Calculate wasted spend
        costs = calculate_costs(traffic_data, google_cpc, bing_cpc)
        
        print("\n" + "="*80)
        print("WASTED AD SPEND (Trial Period)")
        print("="*80)
        print(f"Google Ads:  {costs['google_clicks']:,} invalid clicks × ${google_cpc:.2f} = ${costs['google_waste']:,.2f}")
        print(f"Bing Ads:    {costs['bing_clicks']:,} invalid clicks × ${bing_cpc:.2f} = ${costs['bing_waste']:,.2f}")
        print(f"\n{'TOTAL WASTE:':<13} ${costs['total_waste']:,.2f}")
        
        # ROI Analysis
        print("\n" + "="*80)
        print("ROI ANALYSIS")
        print("="*80)
        
        cheq_cost = float(input("\nEnter estimated monthly CHEQ cost (e.g., 2500): $"))
        trial_days = int(input("Enter trial period length in days (default 31): ") or "31")
        
        roi = calculate_roi(costs['total_waste'], cheq_cost, trial_days)
        
        print("\n" + "-"*80)
        print("PROJECTED SAVINGS:")
        print("-"*80)
        print(f"Monthly Savings:   ${roi['monthly_savings']:,.2f}")
        print(f"Annual Savings:    ${roi['annual_savings']:,.2f}")
        print(f"\nMonthly ROI:       {roi['monthly_roi']:,.1f}%")
        print(f"Payback Period:    {roi['payback_days']:.1f} days")
        
        # Summary
        print("\n" + "="*80)
        print("RECOMMENDATION")
        print("="*80)
        
        if roi['monthly_roi'] > 100:
            print("STRONG CASE: CHEQ pays for itself and generates significant savings")
            print(f"  You save ${roi['monthly_savings'] - cheq_cost:,.2f}/month after CHEQ costs")
        elif roi['monthly_roi'] > 0:
            print("POSITIVE ROI: CHEQ provides value")
        else:
            print("Current CPC rates may not justify CHEQ deployment")
            print("  Consider: Higher CPC campaigns, or additional CHEQ benefits (analytics, security)")
        
        # Export option
        print("\n" + "="*80)
        export = input("\nExport results to CSV? (y/n): ").lower()
        if export == 'y':
            with open(config.ROI_ANALYSIS_CSV, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Metric', 'Value'])
                writer.writerow(['Google Ads Invalid Clicks', costs['google_clicks']])
                writer.writerow(['Google Ads CPC', f"${google_cpc:.2f}"])
                writer.writerow(['Google Ads Waste', f"${costs['google_waste']:,.2f}"])
                writer.writerow(['Bing Ads Invalid Clicks', costs['bing_clicks']])
                writer.writerow(['Bing Ads CPC', f"${bing_cpc:.2f}"])
                writer.writerow(['Bing Ads Waste', f"${costs['bing_waste']:,.2f}"])
                writer.writerow(['Total Waste (Trial Period)', f"${costs['total_waste']:,.2f}"])
                writer.writerow([''])
                writer.writerow(['Monthly Savings (Projected)', f"${roi['monthly_savings']:,.2f}"])
                writer.writerow(['Annual Savings (Projected)', f"${roi['annual_savings']:,.2f}"])
                writer.writerow(['CHEQ Monthly Cost', f"${cheq_cost:.2f}"])
                writer.writerow(['Monthly ROI', f"{roi['monthly_roi']:.1f}%"])
                writer.writerow(['Payback Period (Days)', f"{roi['payback_days']:.1f}"])
            print("Exported to outputs/roi_analysis.csv")
        
    except ValueError as e:
        print(f"\nError: Invalid input. Please enter numeric values.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nCalculation cancelled.")
        sys.exit(0)

if __name__ == '__main__':
    main()
