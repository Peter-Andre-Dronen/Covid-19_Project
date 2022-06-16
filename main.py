import csv
import requests
from datetime import datetime

"""
Data pull from EDCD, filter the data of interest, and save the new data lists.
We have two list; Europe and Scandinavian data list.
"""

# The data source link
CSV_FILE = "https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv"

# Initialization of lists with titles
euro_data_list = [['Date', 'Country', 'Cases', 'Deaths', 'Population']]
scandinavia_data_list = [['Date', 'Country', 'Cases', 'Deaths', 'Population']]

# Pull the data
with requests.get(CSV_FILE) as response:
    # Split text of data
    reader = csv.DictReader(response.text.splitlines())
    for row in reader:
        # Append the rows that are interesting
        euro_data_list.append(
            [datetime.strptime(row['dateRep'], '%d/%m/%Y').date(), row['countriesAndTerritories'], row['cases'],
             row['deaths'], row['popData2020']])
        # Filter the countries of interest for scandinavia data list
        if row['countriesAndTerritories'] == 'Norway' or row['countriesAndTerritories'] == 'Denmark' or row[
            'countriesAndTerritories'] == 'Sweden':
            scandinavia_data_list.append(
                [datetime.strptime(row['dateRep'], '%d/%m/%Y').date(), row['countriesAndTerritories'], row['cases'],
                 row['deaths'], row['popData2020']])

# Save the new european list
with open("euro_data.csv", "w", encoding="utf-8", newline="") as other_file:
    csv.writer(other_file).writerows(euro_data_list)

# Save the new scandinavian list
with open("scandinavian_data.csv", "w", encoding="utf-8", newline="") as other_file:
    csv.writer(other_file).writerows(scandinavia_data_list)
