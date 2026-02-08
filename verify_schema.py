"""
Schema Verification Script
Verifies the database schema is correctly set up
"""

from db_manager import DatabaseManager
import config

def main():
    db = DatabaseManager()
    
    # Check if table exists
    if not db.table_exists():
        print(f"Table '{config.TABLE_NAME}' does not exist!")
        return
    
    print('Tables in database:')
    tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
    tables = db.execute_query(tables_query)
    for table in tables:
        print(f"  - {table[0]}")
    
    print(f'\nSchema for {config.TABLE_NAME} table:')
    schema = db.get_table_info()
    print(f"{'ID':<5} {'Column Name':<25} {'Type':<15} {'Not Null':<10} {'Default':<10} {'PK':<5}")
    print('-' * 70)
    for col in schema:
        print(f"{col[0]:<5} {col[1]:<25} {col[2]:<15} {col[3]:<10} {str(col[4]):<10} {col[5]:<5}")
    
    print(f'\nTotal columns: {len(schema)}')
    
    if len(schema) == config.EXPECTED_COLUMNS:
        print(f"Schema is correct ({config.EXPECTED_COLUMNS} columns)")
    else:
        print(f"Expected {config.EXPECTED_COLUMNS} columns, found {len(schema)}")

if __name__ == '__main__':
    main()
