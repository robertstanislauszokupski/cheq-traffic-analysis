import sqlite3

conn = sqlite3.connect(r'data\cheq.db')
cursor = conn.cursor()

# Check total vs flagged
cursor.execute('''
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN reason_threat_group IS NOT NULL AND reason_threat_group != '' THEN 1 ELSE 0 END) as flagged,
    SUM(CASE WHEN reason_threat_group IS NULL OR reason_threat_group = '' THEN 1 ELSE 0 END) as clean
FROM cheq
''')

result = cursor.fetchone()
print(f"Total events: {result[0]:,}")
print(f"Flagged events: {result[1]:,} ({100*result[1]/result[0]:.2f}%)")
print(f"Clean events: {result[2]:,} ({100*result[2]/result[0]:.2f}%)")

# Check distinct threat groups
print("\n" + "="*50)
print("Distinct threat groups:")
cursor.execute('''
SELECT DISTINCT reason_threat_group, COUNT(*) as count
FROM cheq
GROUP BY reason_threat_group
ORDER BY count DESC
''')
for row in cursor.fetchall():
    threat = row[0] if row[0] else '(NULL/Empty)'
    print(f"  {threat}: {row[1]:,}")

# Sample clean records
print("\n" + "="*50)
print("Sample of clean records (no threat):")
cursor.execute('''
SELECT url_path, gclid, msclkid, reason_threat_group
FROM cheq
WHERE reason_threat_group IS NULL OR reason_threat_group = ''
LIMIT 5
''')
for i, row in enumerate(cursor.fetchall(), 1):
    print(f"  {i}. URL: {row[0][:50]}... | gclid: {row[1][:10] if row[1] else 'None'} | threat: {row[3]}")

conn.close()
