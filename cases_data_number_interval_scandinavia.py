import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

"""Load the data and calculate the interval data to draw figure, 
the comments for each operation can be found in data_analysis.py"""

df = pd.read_csv("scandinavian_data.csv", parse_dates=['Date'], index_col=0)

# Extract the minimum cases of autumn wave of 2021 (Assuming this represents the beginning of the wave)
time_filtered_df_min = df.loc['2021-08-01':'2022-01-01']
# Extract the maximum cases of autumn wave of 2021 (Assuming this represents the peak of the wave)
time_filtered_df_max = df.loc['2021-10-01':'2022-05-01']

time_filtered_df_period = df.loc['2021-08-01':'2022-01-27']

# index of minimums
print(time_filtered_df_min.groupby('Country')[['Cases']].idxmin())
# value of minimums
print(time_filtered_df_min.groupby('Country')[['Cases']].min())

print(time_filtered_df_max.groupby('Country')[['Cases']].idxmax())
# value of maximums
print(time_filtered_df_max.groupby('Country')[['Cases']].max())
# Value of minimum of the maximums
print(time_filtered_df_max.groupby('Country')[['Cases']].max().min())


bins = [(0, 299), (300, 899), (900, 2699), (2700, 8099), (8100, 24300)]
labels = ["0-299", "300-899", "900-2699", "2700-8099", "8100-24300"]

all_countries = sorted(df['Country'].unique().tolist())

valid_countries = list()
data_list = list()

for country in all_countries:

    temp_df = time_filtered_df_period[time_filtered_df_period['Country'] == country]

    temp_list = list()

    for item in bins:
        temp_list.append(temp_df[(temp_df['Cases'] >= item[0]) & (
                temp_df['Cases'] <= item[1])]['Cases'].count())

    data_list.append(temp_list)
    valid_countries.append(country)

final_df = pd.DataFrame(data_list, index=valid_countries, columns=labels)
final_df["total"] = final_df.sum(axis=1)

# Figure creation

fig, ax = plt.subplots(num=1, figsize=(15, 10), dpi=80)

bars = ax.bar(
    [i - 0.225 for i in range(len(labels))], height=data_list[0], width=0.2, color="red", linewidth=0)

# This loop creates small texts with the absolute values above each bar (first set of bars).
for bar in bars:
    height = bar.get_height()

    plt.text(bar.get_x() + bar.get_width() / 2.0, height * 1.01,
             "{:,}".format(height), ha="center", va="bottom")

bars2 = ax.bar(
    [i + 0 for i in range(len(labels))], height=data_list[1], width=0.2, color="blue", linewidth=0)

for bar2 in bars2:
    height2 = bar2.get_height()

    plt.text(bar2.get_x() + bar2.get_width() / 2.0, height2 * 1.01,
             "{:,}".format(height2), ha="center", va="bottom")

bars3 = ax.bar(
    [i + 0.225 for i in range(len(labels))], height=data_list[2], width=0.2, color="gold", linewidth=0)

for bar3 in bars3:
    height3 = bar3.get_height()

    plt.text(bar3.get_x() + bar3.get_width() / 2.0, height3 * 1.01,
             "{:,}".format(height3), ha="center", va="bottom")

ax.yaxis.set_major_locator(ticker.MaxNLocator())
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))


plt.grid(linewidth=0.5)
plt.legend(["Denmark", "Norway", "Sweden"], loc=2)
plt.xticks(range(len(labels)), labels)
plt.title("Number of Days that the Amount of Daily Cases was in a Specific Range Until Peak", pad=15)
plt.xlabel("Range of Cases", labelpad=5)
plt.ylabel("Days", labelpad=15)

#plt.show()
fig.savefig('figures/cases_data_number_interval_scandinavia.png')
