"""
Configuration settings for CHEQ Analysis Project
Centralizes all file paths and project constants
"""

from pathlib import Path

# ============================================================================
# PROJECT PATHS (Cross-platform compatible)
# ============================================================================

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / 'data'
OUTPUT_DIR = PROJECT_ROOT / 'outputs'
VIZ_DIR = OUTPUT_DIR / 'visualizations'
SQL_DIR = PROJECT_ROOT / 'sql'
TESTS_DIR = PROJECT_ROOT / 'tests'

# Ensure output directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
VIZ_DIR.mkdir(exist_ok=True)

# ============================================================================
# DATA FILES
# ============================================================================

DB_PATH = DATA_DIR / 'cheq.db'
CSV_PATH = DATA_DIR / 'cheq_interview_dataset_2026 - interview_dataset.csv'

# ============================================================================
# OUTPUT FILES
# ============================================================================

# Core exports
PAID_TRAFFIC_CSV = OUTPUT_DIR / 'paid_traffic_summary.csv'
FUNNEL_THREATS_CSV = OUTPUT_DIR / 'funnel_threats.csv'
THREAT_TAXONOMY_CSV = OUTPUT_DIR / 'threat_taxonomy.csv'

# Advanced exports
ASN_ANALYSIS_CSV = OUTPUT_DIR / 'asn_analysis.csv'
USER_AGENT_CSV = OUTPUT_DIR / 'user_agent_analysis.csv'
HOURLY_PATTERNS_CSV = OUTPUT_DIR / 'hourly_patterns.csv'
DAILY_PATTERNS_CSV = OUTPUT_DIR / 'daily_patterns.csv'

# ROI analysis
ROI_ANALYSIS_CSV = OUTPUT_DIR / 'roi_analysis.csv'

# Visualizations
THREAT_DIST_PNG = VIZ_DIR / 'threat_distribution.png'
FUNNEL_ANALYSIS_PNG = VIZ_DIR / 'funnel_analysis.png'
HOURLY_PATTERNS_PNG = VIZ_DIR / 'hourly_patterns.png'
DAILY_TRENDS_PNG = VIZ_DIR / 'daily_trends.png'
PAID_TRAFFIC_PNG = VIZ_DIR / 'paid_traffic_comparison.png'
TOP_ASNS_PNG = VIZ_DIR / 'top_asns.png'

# ============================================================================
# ANALYSIS PARAMETERS
# ============================================================================

TRIAL_DAYS = 31
TOP_N_RESULTS = 10
TOP_ASN_COUNT = 30

# ============================================================================
# VISUALIZATION SETTINGS
# ============================================================================

CHART_DPI = 300
CHART_STYLE = 'seaborn-v0_8-darkgrid'
COLOR_PALETTE = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']

# ============================================================================
# DATABASE SCHEMA
# ============================================================================

EXPECTED_COLUMNS = 13
TABLE_NAME = 'cheq'

CSV_TO_DB_MAPPING = {
    'IP': 'ipv6_string',
    'URL': 'url_path',
    'ASN': 'ASN',
    'Useragent': 'Useragent',
    'ip_timezone': 'ip_timezone',
    'device_timezone': 'device_timezone',
    'utm_source': 'parsed_source',
    'utm_campaign': 'parsed_campaign',
    'gclid': 'gclid',
    'msclkid': 'msclkid',
    'threat_group': 'reason_threat_group',
    'threat_type': 'reason_threat_type',
    'timestamp': 'timestamp',
}
