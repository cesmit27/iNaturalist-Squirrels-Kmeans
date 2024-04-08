import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

Eastern = pd.read_csv('EasternWithDate.csv')
Fox = pd.read_csv('FoxWithDate.csv')
Western = pd.read_csv('WesternWithDate.csv')

Eastern['species'] = 'Eastern Gray Squirrel'
Fox['species'] = 'Fox Squirrel'
Western['species'] = 'Western Gray Squirrel'

# Combine dataframes
data = pd.concat([Eastern, Fox, Western])

# Selecting columns (lat and long)
X = data[['latitude', 'longitude']]

# Perform K-means clustering
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
data['cluster'] = kmeans.labels_

# Counting Species Observations
species_cluster_counts = data.groupby(['cluster', 'species']).size().reset_index(name='count')

# Load shapefile
california_shapefile = gpd.read_file(r'D:\Spring 2024\iNat Project\California_State_Boundary-shp\f067d2f7-7950-4e16-beba-8972d811599c2020329-1-18infjv.25og.shp')

fig, ax = plt.subplots(figsize=(10, 10))
california_shapefile.plot(ax=ax, color='lightgray', edgecolor='black')

# Define colors and markers
colors = ['red', 'green', 'blue', 'orange']
species_markers = {'Eastern Gray Squirrel': 'o', 'Fox Squirrel': 's', 'Western Gray Squirrel': 'D'}

# Plot each species in each cluster with a custom label
for cluster in range(3):
    cluster_data = data[data['cluster'] == cluster]
    for species, marker in species_markers.items():
        species_data = cluster_data[cluster_data['species'] == species]
        count = species_cluster_counts.loc[(species_cluster_counts['cluster'] == cluster) & (species_cluster_counts['species'] == species), 'count'].iloc[0]
        label = f"{species} (Cluster {cluster+1}, Observations={count})"
        ax.scatter(species_data['longitude'], species_data['latitude'], color=colors[cluster], marker=marker, label=label, alpha=0.5)

#Title/Axis stuff
ax.set_title('K-means Clustering of Squirrel Observations')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.legend(loc='best', bbox_to_anchor=(1,1))

plt.show()
