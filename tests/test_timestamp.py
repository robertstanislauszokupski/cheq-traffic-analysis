import sqlite3

conn = sqlite3.connect(r'data\cheq.db')
cursor = conn.cursor()

# Test timestamp parsing
print("Testing timestamp parsing:")
cursor.execute("SELECT timestamp FROM cheq LIMIT 5")
for row in cursor.fetchall():
    ts = row[0]
    print(f"  Original: {ts}")
    
# Test hour extraction
cursor.execute("""
SELECT 
    timestamp,
    substr(timestamp, instr(timestamp, ' ') + 1, 2) AS hour_str,
    CAST(substr(timestamp, instr(timestamp, ' ') + 1, 2) AS INTEGER) AS hour_int
FROM cheq 
WHERE instr(timestamp, ' ') > 0
LIMIT 10
""")

print("\nHour extraction test:")
for row in cursor.fetchall():
    print(f"  {row[0]} -> '{row[1]}' -> {row[2]}")

# Test grouping
cursor.execute("""
SELECT 
    CAST(substr(timestamp, instr(timestamp, ' ') + 1, 2) AS INTEGER) AS hour,
    COUNT(*) as cnt
FROM cheq 
WHERE instr(timestamp, ' ') > 0
GROUP BY hour
ORDER BY hour
LIMIT 5
""")

print("\nHourly counts:")
for row in cursor.fetchall():
    print(f"  Hour {row[0]}: {row[1]:,} events")

conn.close()
