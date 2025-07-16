# Project: India Air Quality Analysis and Mapping Dashboard

# Description:
# This project analyzes air pollution levels in major Indian cities,
# visualizes trends using Matplotlib, and builds an interactive map using Folium
# to highlight pollution severity across locations.

# ====================
# STEP 1: Import Libraries
# =================
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt

# ====================
# STEP 2: Load Dataset
# ====================
# For demonstration, we'll use a sample CSV.
# Structure: City, State, Latitude, Longitude, PM2.5, PM10, AQI, Date

df = pd.read_csv("air_quality_india_sample.csv")  # You should replace this with actual dataset

# ====================
# STEP 3: Data Cleaning
# ====================
# Drop rows with missing coordinates or AQI

df.dropna(subset=['Latitude', 'Longitude', 'AQI'], inplace=True)

# ====================
# STEP 4: Basic Analysis with Matplotlib
# ====================
# Average AQI by city
city_avg_aqi = df.groupby('City')['AQI'].mean().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
city_avg_aqi.head(10).plot(kind='bar', color='tomato')
plt.title('Top 10 Most Polluted Cities in India (Average AQI)')
plt.ylabel('Average AQI')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('top_polluted_cities.png')
plt.show()

# ====================
# STEP 5: Folium Map Creation
# ====================
# Create a base map centered on India
map_india = folium.Map(location=[22.5937, 78.9629], zoom_start=5, tiles='CartoDB positron')

# Add clustered markers with AQI level coloring
marker_cluster = MarkerCluster().add_to(map_india)

for i, row in df.iterrows():
    aqi = row['AQI']
    color = 'green' if aqi <= 50 else 'orange' if aqi <= 100 else 'red' if aqi <= 200 else 'darkred'
    popup_text = f"City: {row['City']}<br>AQI: {aqi}<br>PM2.5: {row['PM2.5']}<br>PM10: {row['PM10']}"
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=7,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(marker_cluster)

# Save the map
map_india.save('india_air_quality_map.html')

# ====================
# STEP 6: Summary Output
# ====================
print("Map saved as 'india_air_quality_map.html'")
print("Chart saved as 'top_polluted_cities.png'")
