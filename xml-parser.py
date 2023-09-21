import logging
import mysql.connector
import os
import xml.etree.ElementTree as ET

"""
This code inspects XML files containing receipt data, extracts information, and stores it in a MySQL database.

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
    # Connect to the MySQL database
    with mysql.connector.connect(**db_config) as conn, conn.cursor() as cursor:
        # Create the table if it doesn't exist
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS receipts (
            UnitID VARCHAR(255),
            Quantity INT,
            TotalAmount DECIMAL(10, 2)
        );
        """
        cursor.execute(create_table_sql)
        conn.commit()

        # Loop through XML files in a directory
        xml_directory = 'receipts'

        for filename in os.listdir(xml_directory):
            if filename.endswith('.xml'):
                file_path = os.path.join(xml_directory, filename)
                logging.info(f"Processing file: {file_path}")
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    logging.debug(f"XML structure for {filename}:\n{ET.tostring(root, encoding='utf8').decode('utf8')}")

                    # Extract data from the XML
                    unit_id_element = root.find('.//{http://www.nrf-arts.org/IXRetail/namespace/}UnitID')
                    quantity_element = root.find('.//{http://www.nrf-arts.org/IXRetail/namespace/}Quantity')
                    total_amount_element = root.find(
                        './/{http://www.nrf-arts.org/IXRetail/namespace/}Total[@TotalType="VRExt:TransactionVatRateAmount"]')

                    if unit_id_element is not None and quantity_element is not None and total_amount_element is not None:
                        unit_id = unit_id_element.text
                        quantity = quantity_element.text
                        total_amount = total_amount_element.text

                        # Insert extracted data into the database
                        sql_insert = """
                            INSERT INTO receipts (UnitID, Quantity, TotalAmount)
                            VALUES (%s, %s, %s)
                            """
                        cursor.execute(sql_insert, (unit_id, quantity, total_amount))
                        conn.commit()

                except (ET.ParseError, AttributeError, mysql.connector.Error) as e:
                    logging.error(f"Error processing {filename}: {e}")

except mysql.connector.Error as err:
    logging.error(f"Error connecting to the database: {err}")
