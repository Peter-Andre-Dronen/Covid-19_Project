import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns

"""
Create figures for Europe Data
"""

# Set figure styles
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
df = pd.read_csv("euro_data.csv", parse_dates=['Date'], index_col=0)
# Eliminate the deaths lower than 0
df = df[df['Deaths'] > 0]
# Resample according to date and sum
resampled_df = df.resample("D").sum()

# Figure creation
fig, (ax1, ax2) = plt.subplots(2)

ax1.plot(resampled_df.index,
        resampled_df['Deaths'], label='Deaths', color="red")



# Add death differences
resampled_df["deaths_difference"] = resampled_df['Deaths'].diff()

# Set axis parameters
ax2.plot(resampled_df.index,
        resampled_df["deaths_difference"], label='Death-differences', color="black")

ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax1.yaxis.set_major_locator(ticker.MaxNLocator(10))
ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

ax2.xaxis.set_major_locator(ticker.MaxNLocator(10))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax2.yaxis.set_major_locator(ticker.MaxNLocator(10))
ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

ax1.grid(linewidth=0.5)
ax1.legend(loc=2)
ax1.set_title("Daily COVID-19 Deaths & Death Differences (Europe)", pad=15)
ax1.set_ylabel("COVID-19 Deaths", labelpad=15)

ax2.grid(linewidth=0.5)
ax2.legend(loc=2)
ax2.set_ylabel("COVID-19 Death Differences", labelpad=15)



#plt.savefig('death_data_europe.png')
#plt.show()
fig.savefig('figures/death_data_europe.png')