# NPI Data Importer & Database

The following solution uses SQLite and local storage to facilitate the development of the exercise and the understanding of the result. In a production scenario, aiming at the robustness and reliability of the system, it is recommended that the solution be built, when in an AWS ecosystem, using S3 and Redshift, or even DynamoDB.

## Dependencies
- Python 3.6+, to run the Importer;
- [DB Browser](https://sqlitebrowser.org/dl/) (or equivalent), to access the Database.

## Installation
Extract all the downloaded files into a folder. The final result looks like this:
```prompt
YOUR_FOLDER
 ╘ raw
 └ npi_import.py
 └ readme.md
 └ tb_records_create.sql
 └ tb_records_insert.sql
 └ to_import.csv
 └ to_import.json
 └ to_import.xlsx
```

## Usage
In your folder, execute the ***npi_import.py***.
```prompt
YOUR_FOLDER
 └ npi_import.py
```
You have 4 options to provide the NPI numbers that will be imported. Input the option that best suits your needs (A, B, C or D).
```prompt
Welcome to NPI Importer v1.0.

Please select the option that best suits your import needs:
#A | Manually input NPI number
#B | Import numbers from CSV
#C | Import numbers from Excel
#D | Import numbers from JSON
```
In case of a manual input, enter the NPI number, in it's raw format, without any other character. Example:
```prompt
NPI number: 1396266011
```
In case you need to import a list of NPI numbers, use the CSV, Excel, or JSON options, filling all your NPI numbers into one of the files:
```prompt
YOUR_FOLDER
 └ to_import.csv
 └ to_import.json
 └ to_import.xlsx
```

## Accessing the Database

After importing at least one NPI number, run the DB Browser and open the ***npi.db*** file that will be in the main folder.
```prompt
YOUR_FOLDER
 └ npi.db
```