"""
Data Import Script
Imports CSV data into SQLite database
"""

from db_manager import DatabaseManager
import config

def main():
    db = DatabaseManager()
    
    print(f"Importing data from {config.CSV_PATH}...")
    print(f"Target database: {config.DB_PATH}")
    
    # Import CSV data
    rows_imported = db.import_csv(config.CSV_PATH)
    
    # Validate import
    total_rows = db.get_row_count()
    print(f'Total rows in database: {total_rows:,}')
    
    # Show sample data
    print('\nSample data (first 3 rows):')
    sample_query = "SELECT * FROM cheq LIMIT 3"
    rows = db.execute_query(sample_query)
    for i, row in enumerate(rows, 1):
        print(f'  Row {i}: IP={row[0][:20]}..., URL={row[1][:30]}...')

if __name__ == '__main__':
    main()
