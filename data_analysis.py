import numpy as np
import pandas as pd

""" Data analysis by using pandas """

# Load data, indexed by date, as pandas dataframe
df = pd.read_csv("euro_data.csv", parse_dates=['Date'], index_col=0)

# Remove negative cases
df = df[df['Cases'] > 0]

# Check head, tail, and describe of dataframe
# print(df.head())
# print(df.tail())
# print(df.describe())

# Dataframe is grouped by country, from these groups gets the max value
grouped_df = df.groupby('Country').max()
print(grouped_df)

# Shows the max value of cases in the top 10 countries sorted with the highest case first
print(grouped_df.sort_values('Cases', ascending=False)['Cases'][:10])

# Shows the max value of deaths in the top 10 countries sorted with the highest deaths first
print(grouped_df.sort_values('Deaths', ascending=False)['Deaths'][:10])

# Shows the max value of population in the top 10 countries sorted with the highest population first
print(grouped_df.sort_values('Population', ascending=False)['Population'][:10])

# Choosing a field and resampling and summing daily
field = 'Deaths'
resampled_df = df.resample("D").sum()

# Add new column for diff calculation and calculate
resampled_df["Difference in deaths"] = resampled_df[field].diff()

# Add new column for percentage change calculations and calculate
resampled_df["% change in difference in deaths"] = resampled_df["Difference in deaths"].pct_change()

# Get rid of NaN
resampled_df.dropna(inplace=True)

# Convert diff in death to int
resampled_df["Difference in deaths"] = resampled_df["Difference in deaths"].apply(int)

# Round up, convert to str and add %-sign
resampled_df["% change in difference in deaths"] = resampled_df["% change in difference in deaths"].apply(
    lambda x: str(np.round(x * 100, 2)) + "%")


# Choose a country and calculate similar fields as in between line 33-46
country = "Norway"
# Create a new dataframe with filtered data
filtered_df = df[df['Country'] == country].copy()
filtered_df["Difference in deaths"] = filtered_df[field].diff()
filtered_df["% change in difference in deaths"] = filtered_df["Difference in deaths"].pct_change()
filtered_df.dropna(inplace=True)
filtered_df["Difference in deaths"] = filtered_df["Difference in deaths"].apply(int)

filtered_df["% change in difference in deaths"] = filtered_df["% change in difference in deaths"].apply(
    lambda x: str(np.round(x * 100, 2)) + "%")
print(filtered_df[[field, "Difference in deaths", "% change in difference in deaths"]][-10:])

# Analyse the data with intervals
df = df[df['Cases'] >= 100] # eliminate the casenumber less then 0

bins = [(100, 199), (200, 399), (400, 799), (800, 1599), (1600, 3200)]
labels = ["100-199", "200-399", "400-799", "800-1599", "1600-3200"]

# Create a country list
all_countries = sorted(df['Country'].unique().tolist())
print(all_countries)

# Initialize empty list for country and data
valid_countries = list()
data_list = list()

for country in all_countries:

    temp_df = df[df['Country'] == country]

    # Only process countries if their confirmed cases are equal or greater than 3,200.
    if temp_df['Cases'].max() >= 3200:
        temp_list = list()

        # We iterate over our bins and count how many days each one has.
        for item in bins:
            temp_list.append(temp_df[(temp_df['Cases'] >= item[0]) & (
                    temp_df['Cases'] <= item[1])]['Cases'].count())

        data_list.append(temp_list)
        valid_countries.append(country)
# Create a new dataframe from list
final_df = pd.DataFrame(data_list, index=valid_countries, columns=labels)
# Add a new column for total values and calculate
final_df["total"] = final_df.sum(axis=1)
print(final_df)
