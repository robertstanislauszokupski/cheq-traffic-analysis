"""
CHEQ Data Visualizations
Generates charts for presentation and analysis
"""

from db_manager import DatabaseManager
import queries
import config
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# Set style
plt.style.use(config.CHART_STYLE)
colors = config.COLOR_PALETTE

db = DatabaseManager()

print("="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

# ============================================================================
# Chart 1: Threat Type Distribution (Pie Chart)
# ============================================================================
print("\n1. Creating threat_distribution.png...")
data = db.execute_query(queries.THREAT_TYPE_DISTRIBUTION)
labels = [row[0] if row[0] else 'Unknown' for row in data]
sizes = [row[1] for row in data]

# Calculate "Other" category
total_invalid_query = f"SELECT COUNT(*) FROM cheq WHERE {queries.invalid_condition()}"
total_invalid = db.execute_query_single(total_invalid_query)[0]
other = total_invalid - sum(sizes)
if other > 0:
    labels.append('Other')
    sizes.append(other)

fig, ax = plt.subplots(figsize=(12, 8))
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                    colors=colors, startangle=90,
                                    textprops={'fontsize': 10})
ax.set_title('Invalid Traffic Distribution by Threat Type\n(32,014 total invalid events)', 
             fontsize=16, fontweight='bold', pad=20)

# Make percentage text bold
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(9)

plt.tight_layout()
plt.savefig(config.THREAT_DIST_PNG, dpi=config.CHART_DPI, bbox_inches='tight')
plt.close()
print(f"   Saved {config.THREAT_DIST_PNG}")

# ============================================================================
# Chart 2: Top 10 Pages by Invalid Traffic (Bar Chart)
# ============================================================================
print("\n2. Creating funnel_analysis.png...")
data = db.execute_query(queries.FUNNEL_EXPOSURE + " LIMIT 10")
pages = [row[0].replace('https://www.worker.com', '').replace('https://team.worker.com', '/team')[:40] for row in data]
total_vals = [row[1] for row in data]
invalid_vals = [row[2] for row in data]

fig, ax = plt.subplots(figsize=(12, 8))
y_pos = range(len(pages))

# Create bars
bars1 = ax.barh(y_pos, total_vals, color='#45B7D1', alpha=0.6, label='Total Events')
bars2 = ax.barh(y_pos, invalid_vals, color='#FF6B6B', alpha=0.9, label='Invalid Events')

ax.set_yticks(y_pos)
ax.set_yticklabels(pages)
ax.invert_yaxis()
ax.set_xlabel('Number of Events', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Pages by Invalid Traffic Volume', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='lower right', fontsize=10)

# Add value labels
for i, (total, invalid) in enumerate(zip(total_vals, invalid_vals)):
    pct = (invalid / total * 100) if total > 0 else 0
    ax.text(invalid + 100, i, f'{invalid:,} ({pct:.1f}%)', 
            va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(config.FUNNEL_ANALYSIS_PNG, dpi=config.CHART_DPI, bbox_inches='tight')
plt.close()
print(f"   Saved {config.FUNNEL_ANALYSIS_PNG}")

# ============================================================================
# Chart 3: Hourly Traffic Pattern (Line Chart)
# ============================================================================
print("\n3. Creating hourly_patterns.png...")
data = db.execute_query(queries.HOURLY_PATTERNS)
hours = [row[0] for row in data]
total_events = [row[1] for row in data]
invalid_events = [row[2] for row in data]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# Total traffic
ax1.plot(hours, total_events, marker='o', linewidth=2, color='#45B7D1', markersize=6)
ax1.fill_between(hours, total_events, alpha=0.3, color='#45B7D1')
ax1.set_ylabel('Total Events', fontsize=12, fontweight='bold')
ax1.set_title('Traffic Patterns by Hour of Day (UTC)', fontsize=16, fontweight='bold', pad=20)
ax1.grid(True, alpha=0.3)

# Highlight attack window (hours 20-23)
ax1.axvspan(20, 23, alpha=0.2, color='red', label='Attack Window')
ax1.legend(loc='upper left')

# Invalid traffic
ax2.plot(hours, invalid_events, marker='o', linewidth=2, color='#FF6B6B', markersize=6)
ax2.fill_between(hours, invalid_events, alpha=0.3, color='#FF6B6B')
ax2.set_xlabel('Hour of Day (UTC)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Invalid Events', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.axvspan(20, 23, alpha=0.2, color='red')

plt.tight_layout()
plt.savefig(config.HOURLY_PATTERNS_PNG, dpi=config.CHART_DPI, bbox_inches='tight')
plt.close()
print(f"   Saved {config.HOURLY_PATTERNS_PNG}")

# ============================================================================
# Chart 4: Daily Trends (Bar Chart)
# ============================================================================
print("\n4. Creating daily_trends.png...")
data = db.execute_query(queries.DAILY_PATTERNS)
dates = [row[0] for row in data]
total_events = [row[1] for row in data]
invalid_events = [row[2] for row in data]
invalid_pct = [(inv/tot*100) if tot > 0 else 0 for inv, tot in zip(invalid_events, total_events)]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# Event volumes
x_pos = range(len(dates))
ax1.bar(x_pos, total_events, color='#45B7D1', alpha=0.6, label='Total Events')
ax1.bar(x_pos, invalid_events, color='#FF6B6B', alpha=0.9, label='Invalid Events')
ax1.set_ylabel('Number of Events', fontsize=12, fontweight='bold')
ax1.set_title('Daily Traffic Trends - July 2024', fontsize=16, fontweight='bold', pad=20)
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3, axis='y')

# Invalid percentage
ax2.bar(x_pos, invalid_pct, color='#FF6B6B', alpha=0.8)
ax2.axhline(y=25.22, color='orange', linestyle='--', linewidth=2, label='Average (25.22%)')
ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
ax2.set_ylabel('Invalid Traffic %', fontsize=12, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(dates, rotation=45, ha='right')
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(config.DAILY_TRENDS_PNG, dpi=config.CHART_DPI, bbox_inches='tight')
plt.close()
print(f"   Saved {config.DAILY_TRENDS_PNG}")

# ============================================================================
# Chart 5: Paid Traffic Comparison (Bar Chart)
# ============================================================================
print("\n5. Creating paid_traffic_comparison.png...")
data = db.execute_query(queries.PAID_TRAFFIC_RISK)
sources = [row[0] for row in data]
total_vals = [row[1] for row in data]
invalid_vals = [row[2] for row in data]
invalid_pct = [(inv/tot*100) if tot > 0 else 0 for inv, tot in zip(invalid_vals, total_vals)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Event volumes
x_pos = range(len(sources))
width = 0.35
bars1 = ax1.bar([x - width/2 for x in x_pos], total_vals, width, 
                label='Total Events', color='#45B7D1', alpha=0.8)
bars2 = ax1.bar([x + width/2 for x in x_pos], invalid_vals, width,
                label='Invalid Events', color='#FF6B6B', alpha=0.8)
ax1.set_ylabel('Number of Events', fontsize=12, fontweight='bold')
ax1.set_title('Traffic Volume by Source', fontsize=14, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(sources, rotation=15, ha='right')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}',
            ha='center', va='bottom', fontsize=9)

for bar in bars2:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}',
            ha='center', va='bottom', fontsize=9)

# Invalid percentage
colors_pct = ['#FF6B6B' if 'Ads' in s else '#45B7D1' for s in sources]
bars = ax2.bar(x_pos, invalid_pct, color=colors_pct, alpha=0.8)
ax2.set_ylabel('Invalid Traffic %', fontsize=12, fontweight='bold')
ax2.set_title('Invalid Rate by Source', fontsize=14, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(sources, rotation=15, ha='right')
ax2.axhline(y=25.22, color='orange', linestyle='--', linewidth=2, alpha=0.7)
ax2.grid(True, alpha=0.3, axis='y')

# Add percentage labels
for i, (bar, pct) in enumerate(zip(bars, invalid_pct)):
    ax2.text(bar.get_x() + bar.get_width()/2., pct + 1,
            f'{pct:.1f}%',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(config.PAID_TRAFFIC_PNG, dpi=config.CHART_DPI, bbox_inches='tight')
plt.close()
print(f"   Saved {config.PAID_TRAFFIC_PNG}")

# ============================================================================
# Chart 6: Top ASNs/ISPs (Horizontal Bar)
# ============================================================================
print("\n6. Creating top_asns.png...")
data = db.execute_query(queries.TOP_ASNS)
asns = [row[0] for row in data]
invalid_vals = [row[1] for row in data]

fig, ax = plt.subplots(figsize=(12, 8))
y_pos = range(len(asns))

bars = ax.barh(y_pos, invalid_vals, color='#FF6B6B', alpha=0.8)
ax.set_yticks(y_pos)
ax.set_yticklabels(asns)
ax.invert_yaxis()
ax.set_xlabel('Invalid Events', fontsize=12, fontweight='bold')
ax.set_title('Top 10 ASNs/ISPs by Invalid Traffic', fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (bar, val) in enumerate(zip(bars, invalid_vals)):
    ax.text(val + 20, i, f'{val:,}', 
            va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(config.TOP_ASNS_PNG, dpi=config.CHART_DPI, bbox_inches='tight')
plt.close()
print(f"   Saved {config.TOP_ASNS_PNG}")

print("\n" + "="*80)
print("VISUALIZATION SUMMARY")
print("="*80)
print("\nGenerated 6 visualizations:")
print("  1. threat_distribution.png      - Pie chart of threat types")
print("  2. funnel_analysis.png           - Top 10 pages with invalid traffic")
print("  3. hourly_patterns.png           - Traffic patterns by hour (shows attack window)")
print("  4. daily_trends.png              - Day-by-day volume and invalid %")
print("  5. paid_traffic_comparison.png   - Paid vs organic/direct traffic analysis")
print("  6. top_asns.png                  - Top ISPs generating invalid traffic")
print(f"\nAll saved to: {config.VIZ_DIR}")
print("="*80)
