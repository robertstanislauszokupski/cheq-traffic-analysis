"""
Database Manager for CHEQ Analysis
Handles all database connections and query execution
"""

import sqlite3
import csv
import logging
from pathlib import Path
from typing import List, Tuple, Optional
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite database connections and operations"""
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize the database manager
        
        Args:
            db_path: Path to the SQLite database (default: from config)
        """
        self.db_path = db_path or config.DB_PATH
        logger.info(f"Database manager initialized with path: {self.db_path}")
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Get a database connection
        
        Returns:
            sqlite3.Connection: Active database connection
        """
        try:
            return sqlite3.connect(str(self.db_path))
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def execute_query(self, query: str) -> List[Tuple]:
        """
        Execute a query and return all results
        
        Args:
            query: SQL query string
            
        Returns:
            List of tuples containing query results
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            logger.debug(f"Query executed successfully, returned {len(results)} rows")
            return results
        except sqlite3.Error as e:
            logger.error(f"Query execution failed: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_query_single(self, query: str) -> Optional[Tuple]:
        """
        Execute a query and return the first result
        
        Args:
            query: SQL query string
            
        Returns:
            Single tuple or None
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            logger.error(f"Query execution failed: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_to_csv(self, query: str, output_path: Path, headers: List[str]) -> None:
        """
        Execute query and write results to CSV
        
        Args:
            query: SQL query string
            output_path: Path to output CSV file
            headers: List of column headers
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(cursor.fetchall())
            
            logger.info(f"Created {output_path}")
        except sqlite3.Error as e:
            logger.error(f"Failed to export query results to CSV: {e}")
            raise
        except IOError as e:
            logger.error(f"Failed to write CSV file: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def get_table_info(self, table_name: str = config.TABLE_NAME) -> List[Tuple]:
        """
        Get schema information for a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of tuples with column information
        """
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
    
    def get_row_count(self, table_name: str = config.TABLE_NAME) -> int:
        """
        Get the number of rows in a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            Number of rows
        """
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = self.execute_query_single(query)
        return result[0] if result else 0
    
    def table_exists(self, table_name: str = config.TABLE_NAME) -> bool:
        """
        Check if a table exists
        
        Args:
            table_name: Name of the table
            
        Returns:
            True if table exists, False otherwise
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (table_name,))
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logger.error(f"Failed to check table existence: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def import_csv(self, csv_path: Path, table_name: str = config.TABLE_NAME) -> int:
        """
        Import data from CSV into the database
        
        Args:
            csv_path: Path to CSV file
            table_name: Target table name
            
        Returns:
            Number of rows imported
        """
        conn = None
        rows_imported = 0
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                
                for row in csv_reader:
                    cursor.execute(f'''
                        INSERT INTO {table_name} (
                            ipv6_string, url_path, ASN, Useragent, 
                            ip_timezone, device_timezone, 
                            parsed_source, parsed_campaign, 
                            gclid, msclkid, 
                            reason_threat_group, reason_threat_type, 
                            timestamp
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row['IP'], row['URL'], row['ASN'], row['Useragent'],
                        row['ip_timezone'], row['device_timezone'],
                        row['utm_source'], row['utm_campaign'],
                        row['gclid'], row['msclkid'],
                        row['threat_group'], row['threat_type'],
                        row['timestamp']
                    ))
                    rows_imported += 1
            
            conn.commit()
            logger.info(f"Successfully imported {rows_imported:,} rows")
            return rows_imported
            
        except sqlite3.Error as e:
            logger.error(f"Database import failed: {e}")
            if conn:
                conn.rollback()
            raise
        except IOError as e:
            logger.error(f"Failed to read CSV file: {e}")
            raise
        finally:
            if conn:
                conn.close()
