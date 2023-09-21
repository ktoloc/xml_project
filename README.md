# XML to MySQL

Repository involves connecting to a MySQL(Ver 8.1.0) database using Python,
importing XML data from a directory, parsing it, and inserting elements
into the database. There's a separate report script that 
retrieves data from the database, 
calculates totals, and exports the results to a CSV file.


## Get started

Clone the repository:

```
git clone https://github.com/ktoloc/xml_project.git
```

Install requirements file:
```
pip install -r requirements.txt
```

Download MySQL Community Server: [MySQL Downloads](https://dev.mysql.com/downloads/mysql/) and follow the installation instructions for your operating system.
## Setting Up the MySQL Database

1. Open a terminal or command prompt.

2. Log in to MySQL as the root user using the following command: ```mysql -u root -p```

3. Enter the root password when prompted.

4. Create a new database for your project (replace `your_database_name` with your desired database name): ```CREATE DATABASE your_database_name;``` 

5. Install MySQL Connector for Python:
```
pip install mysql-connector-python

```
6. Replace the placeholders with your MySQL credentials:

```
db = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database'
)
```
7. Run the project using the command (`python xml-parser.py`).

## Generating report from MySQL DB to csv file

Replace the placeholders with your MySQL credentials:

```
db = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database'
)
```

Run the report-generator using the command (`python report_generator.py`).
