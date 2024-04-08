import pandas as pd

western = pd.read_csv('WesternWithDate.csv')
eastern = pd.read_csv('EasternWithDate.csv')
fox = pd.read_csv('FoxWithDate.csv')

# Add a species column to Dataframe
western['species'] = 'Western Gray Squirrel'
eastern['species'] = 'Eastern Gray Squirrel'
fox['species'] = 'Fox Squirrel'

# Combine Dataframe
all_squirrels = pd.concat([western, eastern, fox])

# Group by year and species, and count occurrences
counts_over_time = all_squirrels.groupby(['Date', 'species']).size().reset_index(name='counts')
counts_over_time['Date'] = counts_over_time['Date'].astype(str)

# Calculate total counts by year
total_counts_over_time = counts_over_time.groupby('Date')['counts'].transform('sum')

# Calculate proportions
counts_over_time['prop'] = counts_over_time['counts'] / total_counts_over_time
counts_over_time['proportion'] = counts_over_time['prop'] * 100

import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style='darkgrid', palette='tab10')
# Create a lineplot
sns.lineplot(data=counts_over_time, x='Date', y='proportion', hue='species')

plt.title('Proportion of Squirrel Species Over Time')
plt.ylabel('Proportion %')
plt.xlabel('Year')
plt.xticks(rotation=45)
plt.legend(fontsize='small')
plt.savefig('proportion.svg')
plt.tight_layout()
plt.show()