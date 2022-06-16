import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

"""Load the data and calculate the interval data to draw figure, 
the comments for each operation can be found in data_analysis.py"""

df = pd.read_csv("scandinavian_data.csv", parse_dates=['Date'], index_col=0)

df = df[df['Cases'] >= 100]

bins = [(100, 199), (200, 399), (400, 799), (800, 1599), (1600, 3200)]
labels = ["100-199", "200-399", "400-799", "800-1599", "1600-3200"]

all_countries = sorted(df['Country'].unique().tolist())

valid_countries = list()
data_list = list()

for country in all_countries:

    temp_df = df[df['Country'] == country]

    if temp_df['Cases'].max() >= 3200:
        temp_list = list()

        for item in bins:
            temp_list.append(temp_df[(temp_df['Cases'] >= item[0]) & (
                    temp_df['Cases'] <= item[1])]['Cases'].count())

        data_list.append(temp_list)
        valid_countries.append(country)

final_df = pd.DataFrame(data_list, index=valid_countries, columns=labels)
final_df["total"] = final_df.sum(axis=1)

# Figure creation
fig, ax = plt.subplots()

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
plt.title("Number of Days that the Amount of Daily Cases was in a Specific Range", pad=15)
plt.xlabel("Range", labelpad=5)
plt.ylabel("Cases", labelpad=15)

# plt.savefig('cases_data_number_interval_scandinavia.png')
# plt.show()
fig.savefig('figures/cases_data_number_interval_scandinavia.png')
