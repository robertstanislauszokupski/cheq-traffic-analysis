# CHEQ Interview Exercise - Traffic Analysis

**Data Analyst:** Robert Okupski  
**Analysis Period:** Trial dataset from July 2024  
**Total Events Analyzed:** 126,959

---

## Quick Demo

**[View Interactive Analysis Notebook](DEMO.ipynb)** - Explore key findings with visualizations and commentary

*The demo notebook showcases the analysis interactively with charts, ROI calculations, and strategic insights. Perfect for presentations or quick review of findings.*

---

## Executive Summary

This analysis examines trial data from CHEQ's invalid traffic detection system, focusing on identifying patterns of fraudulent activity, quantifying wasted ad spend, and highlighting security vulnerabilities across the customer journey.

### Key Findings

- **Paid Traffic Impact:** 8,661 invalid paid ad clicks detected (19.7% of paid traffic)
  - Bing Ads: 4,777 invalid clicks (29.89% invalid rate)
  - Google Ads: 3,884 invalid clicks (13.83% invalid rate)
  
- **Highest Risk Pages:**
  - Hire landing page: 6,762 invalid events (83.35% invalid rate)
  - Login page: 5,632 invalid events (41.48% invalid rate)
  - Find work page: 4,035 invalid events (56.59% invalid rate)
  
- **Threat Composition:**
  - Malicious Bots: 43.19% (of flagged traffic)
  - Automation Tools: 24.04%
  - VPN Traffic: 11.71%
  
- **Overall Traffic Health:**
  - Total events: 126,959
  - Invalid events: 32,014 (25.22%)
  - Clean events: 94,945 (74.78%)

---

## Project Structure

```
cheq-interview/
├── data/
│   ├── cheq.db                              # SQLite database
│   └── cheq_interview_dataset_2026 - ...    # Source CSV data
├── sql/
│   ├── 01_schema.sql                        # Table schema definition
│   ├── 02_import.sql                        # Import documentation
│   └── 03_analysis.sql                      # 9 analysis queries (5 core + 4 advanced)
├── outputs/
│   ├── paid_traffic_summary.csv             # Paid ad analysis export
│   ├── funnel_threats.csv                   # Page-by-page breakdown
│   ├── threat_taxonomy.csv                  # Threat categorization
│   ├── asn_analysis.csv                     # ISP/hosting provider analysis
│   ├── user_agent_analysis.csv              # Browser/bot detection
│   ├── hourly_patterns.csv                  # Attack timing patterns
│   ├── daily_patterns.csv                   # Day-over-day trends
│   ├── roi_analysis.csv                     # Cost calculator outputs
│   └── visualizations/                      # Charts and graphs (PNG)
│       ├── threat_distribution.png
│   DEMO.ipynb                               # Interactive analysis notebook
├──     ├── funnel_analysis.png
│       ├── hourly_patterns.png
│       ├── daily_trends.png
│       ├── paid_traffic_comparison.png
│       └── top_asns.png
├── tests/                                   # Test and utility scripts
│   ├── check_data.py                        # Data validation utility
│   └── test_timestamp.py                    # Timestamp parsing tests
├── queries.py                               # Centralized SQL queries
├── db_manager.py                            # Database connection manager
├── config.py                                # Project configuration
├── create_visualizations.py                 # Generate charts and graphs
├── verify_schema.py                         # Schema verification script
├── import_data.py                           # CSV import script
├── run_analysis.py                          # Execute core 5 analysis queries
├── export_results.py                        # Generate core CSV outputs
├── export_advanced.py                       # Generate advanced CSV outputs
├── cost_calculator.py                       # Interactive ROI calculator
├── run_all.py                               # Master pipeline runner
├── requirements.txt                         # Python dependencies
├── .gitignore                               # Git ignore file
└── README.md                                # This file
```

**DEMO.ipynb**: Interactive Jupyter notebook with visualizations and insights
- **queries.py**: All SQL queries in one place - eliminates 50+ instances of duplicated query code
- **db_manager.py**: Centralized database operations with error handling and cross-platform paths
- **config.py**: All file paths and settings in one location
- **run_all.py**: Automated pipeline to run entire analysis workflow
- **requirements.txt**: Python package dependencies (pandas, matplotlib, seaborn, jupyter)analysis workflow
- **requirements.txt**: Python package dependencies
- **.gitignore**: Excludes database and output files from version control

---

## Technology Stack

- **Database:** SQLite 3
- **Libraries:** pandas, matplotlib, seaborn (data analysis & visualization)
- **Notebook:** Jupyter (for interactive analysiexport)
- **Libraries:** matplotlib (for visualizations)
- **IDE:** Visual Studio Code
- **SQL Dialect:** SQLite-compatible SQL

---

## Setup & Reproduction

### Prerequisites

- Python 3.11 or higher
- SQLite3 (included with Python)
- VS Code (opti

**Option A: Interactive Notebook (Recommended for Presentations)**

```bash
# Install dependencies
pip install -r requirements.txt

# Launch Jupyter Notebook
jupyter notebook DEMO.ipynb
```

Then run all cells to see the complete analysis with visualizations.

**Option B: Automated Script Pipeline**ended for query execution)

### Quick Start (Automated)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the entire analysis pipeline
python run_all.py
```

The automated pipeline will:
1. Verify database schema
2. Run all 5 core analysis queries
3. Export core results to CSV
4. Export advanced analysis to CSV  
5. Generate all 6 visualizations

### Manual Setup (Step-by-Step)

#### Step 0: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 1: Verify Database Schema

```bash
python verify_schema.py
```

Expected output: 13 columns in the `cheq` table

#### Step 2: Import Data (if needed)

```bash
python import_data.py
```

This imports 126,959 rows from the CSV into the database.

#### Step 3: Run Analysis Queries

```bash
python run_analysis.py
```

This executes all 5 analysis queries and displays results in the terminal.

#### Step 4: Export Results

```bash
python export_results.py
```

This generates the core CSV reports for paid traffic, funnel analysis, and threat taxonomy.

#### Step 5: Advanced Analysis (Optional)

```bash
# Generate advanced analysis exports
python export_advanced.py

# Run interactive ROI calculator
python cost_calculator.py

# Generate visualizations
python create_visualizations.py
```

The advanced analysis includes ASN/ISP patterns, user agent detection, and temporal attack patterns. Visualizations are saved as high-resolution PNG files suitable for presentation.

---

## Code Architecture

This project has been refactored to follow software engineering best practices:

### Centralized Query Management (`queries.py`)
- **All SQL queries in one location** - eliminates 50+ instances of duplicated code
- Reusable query strings for all analysis operations
- Single point of maintenance for query logic
- Includes query metadata (column headers) for CSV exports

### Database Abstraction Layer (`db_manager.py`)
- **Cross-platform path handling** - works on Windows, Mac, and Linux
- Centralized connection management with error handling
- Built-in CSV export functionality
- Logging support for debugging
- Reduces code duplication by ~60%

### Configuration Management (`config.py`)
- All file paths and constants in one place
- Easy modification without touching code
- Automatic directory creation
- Centralized project settings

### Benefits of This Architecture
- **Maintainability**: Change a query once, update everywhere  
- **Portability**: Cross-platform file paths using pathlib  
- **Readability**: Scripts are 40-60% shorter and clearer  
- **Scalability**: Easy to add new queries or outputs  
- **Testing**: Centralized code is easier to test  

### Before & After Example

**Before (run_analysis.py - 130 lines):**
```python
conn = sqlite3.connect(r'data\cheq.db')
cursor.execute('''
  SELECT COUNT(*) ...
  WHERE reason_threat_group IS NOT NULL AND reason_threat_group != ''
  ...
''')
```

**After (run_analysis.py - 70 lines):**
```python
from db_manager import DatabaseManager
import queries

db = DatabaseManager()
row = db.execute_query_single(queries.OVERALL_HEALTH)
```

---

## Analysis Details

### Core Analysis (Queries 1-5)

### Query 1: Overall Traffic Health
Establishes baseline risk metrics for the trial period.

### Query 2: Funnel Exposure by Page
Identifies which pages in the customer journey are most vulnerable to invalid traffic.

### Query 3: Paid Traffic Risk
**Critical for ROI discussions** - quantifies wasted ad spend by channel.

### Query 4: Threat Taxonomy
Breaks down invalid traffic by threat group and type for security prioritization.

### Query 5: Geo/Device Timezone Mismatches
Detects VPN usage, emulators, and automation signals through timezone analysis.

### Advanced Analysis (Queries 6-9)

### Query 6: ASN/ISP Analysis
Identifies which hosting providers and ISPs generate the most invalid traffic. Critical for IP blocking strategies and firewall rules.

**Key Insight:** AS-CHOOPA (Vultr hosting) generated 9,561 invalid events (100% invalid rate), indicating server-based bot attacks.

### Query 7: User Agent Analysis
Detects automation tools, scrapers, and suspicious browser patterns.

**Key Insight:** 
- Firefox has 65.51% invalid rate (likely bot impersonation)
- Chrome has 25.63% invalid rate (close to baseline)
- 67 Headless Chrome instances detected (100% invalid)

### Query 8 & 9: Time-Based Pattern Analysis
Identifies attack waves by hour and day.

**Key Insights:**
- Peak attack hour: 22:00 UTC (2,537 invalid events)
- Hours 20-23 show 3x normal traffic volume (likely coordinated bot attack)
- July 5th had 89.74% invalid rate (5,000 events) - major attack day
- July 14th had 90,816 events but only 5.34% invalid (normal operations day)
---

## Visualizations

Six presentation-ready charts are available in [`outputs/visualizations/`](outputs/visualizations/):

1. **threat_distribution.png** - Pie chart showing breakdown of threat types
2. **funnel_analysis.png** - Top 10 pages ranked by invalid traffic volume
3. **hourly_patterns.png** - Traffic patterns by hour revealing attack window (20-23 UTC)
4. **daily_trends.png** - Day-over-day volume and invalid traffic percentage
5. **paid_traffic_comparison.png** - Paid vs organic traffic analysis with invalid rates
6. **top_asns.png** - Top 10 ISPs/hosting providers generating invalid traffic

To regenerate visualizations:
```bash
python create_visualizations.py
```Infrastructure Threats
- **AS-CHOOPA and AS-BLAZINGSEO** (hosting providers): 17,804 invalid events combined - indicating server-based bot attacks
- **Coordinated attack pattern**: 3x traffic spike during hours 20-23 UTC
- **July 5th attack**: 89.74% invalid rate suggests DDoS or scraping campaign

### Interactive Cost Calculator

Use the cost calculator to quantify ROI with your actual CPC rates:

```bash
python cost_calculator.py
```

The calculator provides:
- Wasted ad spend by channel (Google Ads, Bing Ads)
- Monthly and annual savings projections
- CHEQ ROI percentage
- Payback period in days

### Recommendation
- Deploy CHEQ across all paid campaigns immediately, prioritizing Bing Ads
- Focus protection on hire landing page (83% invalid rate)
- Implement enhanced bot detection for malicious bot traffic (43% of threats)
- Block or rate-limit traffic from AS-CHOOPA and AS-BLAZINGSEO ASNs
- Investigate traffic spikes during 20-23 UTC hours
### Query 3: Paid Traffic Risk
**Critical for ROI discussions** - quantifies wasted ad spend by channel.

### Query 4: Threat Taxonomy
Breaks down invalid traffic by threat group and type for security prioritization.

### Query 5: Geo/Device Timezone Mismatches
Detects VPN usage, emulators, and automation signals through timezone analysis.

---

## Business Impact

### Wasted Ad Spend
- **8,661 invalid paid clicks** detected across both platforms
- **$X per click assumption:** If average CPC is $2.50, this represents **~$21,652** in wasted ad spend during the trial period alone.
- Bing Ads has higher invalid rate (29.89%) compared to Google Ads (13.83%)

### Conversion Impact
- Invalid traffic on high-intent pages (hire landing: 83.35%, login: 41.48%) skews analytics and inflates bounce rates.
- **6,762 invalid events on hire landing page** represent serious ROI exposure for recruitment campaigns.

### Recommendation
- Deploy CHEQ across all paid campaigns immediately, prioritizing Bing Ads
- Focus protection on hire landing page (83% invalid rate)
- Implement enhanced bot detection for malicious bot traffic (43% of threats)

---

## Interview Defense

**Q: Why SQLite instead of a production database?**  
A: SQLite was specified in the assignment and is ideal for this use case - lightweight, portable, and production-ready for analytical workloads of this size. The SQL queries are database-agnostic and easily portable to PostgreSQL, MySQL, or cloud data warehouses.

**Q: Why Python scripts instead of pure SQL?**  
A: Python scripts provide automation and reproducibility. The core analysis is pure SQL (see `03_analysis.sql`), but Python handles CSV imports with proper encoding/error handling and generates clean exports for stakeholder presentations.

**Q: How would you scale this?**  
A: For production scale:
1. Migrate to PostgreSQL/BigQuery for larger datasets
2. Add incremental ETL pipelines (Airflow, dbt)
3. Implement data quality checks and alerting
4. Create automated dashboards (Tableau, Looker)

---

## Contact

**Robert Okupski**  
[robert.okupski@gmail.com] | [https://www.linkedin.com/in/robert-okupski/] | [(908)-391-5858]

---

## Appendix: Data Dictionary

| Column | Description |
|--------|-------------|
| `ipv6_string` | Source IP address (IPv6 format) |
| `url_path` | Full URL of the visited page |
| `ASN` | Autonomous System Number (ISP information) |
| `Useragent` | Browser user agent string |
| `ip_timezone` | Timezone derived from IP geolocation |
| `device_timezone` | Timezone reported by device |
| `parsed_source` | UTM source parameter |
| `parsed_campaign` | UTM campaign parameter |
| `gclid` | Google Click ID (paid search) |
| `msclkid` | Microsoft Click ID (Bing Ads) |
| `reason_threat_group` | CHEQ threat categorization (group) |
| `reason_threat_type` | CHEQ threat categorization (type) |
| `timestamp` | Event timestamp |

---

*This analysis was conducted as part of the CHEQ Solutions Engineer interview process.*
