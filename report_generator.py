import logging
import mysql.connector
import csv
from datetime import datetime


"""
This code connects to a MySQL database, extracts data, and exports it to a CSV file.
"""

log_filename = 'app.log'
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'admin',
    'database': 'reports',
}

try:
    # Connecting and extracting data to the MySQL database
    with mysql.connector.connect(**db_config) as conn, conn.cursor() as cursor:
        select_query = """
        SELECT UnitID, SUM(Quantity) AS TotalItems, SUM(TotalAmount) AS TotalSum, COUNT(*) AS TotalReceipts
        FROM receipts
        GROUP BY UnitID
        """
        cursor.execute(select_query)
        data = cursor.fetchall()

        """Create a dictionary to store the total  amount of receipts received from 
         the store and get date of the report."""

        unit_totals = {}
        current_date = datetime.now()

        # Write data to the CSV file
        csv_file_path = 'report.csv'
        with open(csv_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            csv_writer.writerow(['Report Date:', current_date])

            csv_writer.writerow(['UnitID', 'TotalItems', 'TotalSum', 'TotalReceipts'])

            for row in data:
                unit_id, total_receipts, total_items, total_sum = row
                unit_totals[unit_id] = unit_totals.get(unit_id, 0) + total_sum
                csv_writer.writerow([unit_id, total_receipts, total_items, unit_totals[unit_id]])

        logging.info(f"Data exported to {csv_file_path}")
except mysql.connector.Error as err:
    logging.error(f"Error connecting to the database: {err}")
except Exception as e:
    logging.error(f"An error occurred: {e}")
