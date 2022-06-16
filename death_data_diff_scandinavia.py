import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns


"""
Create figures for Scandinavian Data
"""

#set figure styles
sns.set(style="ticks",
        rc={
            "figure.figsize": [15, 10],
            "text.color": "black",
            "legend.fontsize": "large",
            "xtick.labelsize": "x-large",
            "ytick.labelsize": "x-large",
            "axes.labelsize": "x-large",
            "axes.titlesize": "x-large",
            "axes.labelcolor": "black",
            "axes.edgecolor": "black",
            "xtick.color": "black",
            "ytick.color": "black",
            "axes.facecolor": "lightgray",
            "figure.facecolor": "gray"}
        )

# Load the datasets indexed by datetime
df = pd.read_csv("scandinavian_data.csv", parse_dates=['Date'], index_col=0)


COUNTRIES = [
   ["Norway", "blue"],
    ["Denmark", "red"],
    ["Sweden", "gold"]
]

field = 'Deaths'
df = df[df[field] > 0]

fig, ax = plt.subplots()

for country in COUNTRIES:
    temp_df = df[df['Country'] == country[0]].copy()
    temp_df["difference"] = temp_df[field].diff()

    ax.plot(temp_df.index, temp_df["difference"],
            label=country[0], color=country[1])

ax.xaxis.set_major_locator(mdates.DayLocator(interval=150))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax.yaxis.set_major_locator(ticker.MaxNLocator())
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

ax.grid(linewidth=0.5)
ax.legend(loc=2)
plt.title("Daily Deaths Comparison Between Scandinavian Countries", pad=15)
plt.xlabel("Date", labelpad=15)
plt.ylabel("Daily death differences", labelpad=15)

#plt.show()
#plt.savefig('death_data_diff_scandinavia.png')
fig.savefig('figures/death_data_diff_scandinavia.png')