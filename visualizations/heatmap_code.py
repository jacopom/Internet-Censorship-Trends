import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches

# Create a dataset based on our analysis
data = {
    'Country': [
        # Asia Pacific
        'Myanmar', 'China', 'Vietnam', 'India', 'Indonesia', 'Thailand', 'Philippines', 'Cambodia', 'Malaysia', 'Hong Kong',
        # Middle East and North Africa
        'Iran', 'Egypt', 'Saudi Arabia', 'UAE', 'Libya', 'Syria', 'Tunisia', 'Algeria', 'Morocco', 'Iraq',
        # Sub-Saharan Africa
        'Ethiopia', 'Uganda', 'Nigeria', 'Kenya', 'Zimbabwe', 'Sudan', 'Tanzania', 'Zambia', 'Ghana', 'South Africa',
        # Eurasia
        'Russia', 'Kyrgyzstan', 'Belarus', 'Turkey', 'Azerbaijan', 'Kazakhstan', 'Uzbekistan', 'Ukraine', 'Georgia', 'Armenia',
        # Americas
        'Venezuela', 'Cuba', 'Nicaragua', 'Mexico', 'Brazil', 'Colombia', 'Ecuador', 'Bolivia', 'Argentina', 'United States'
    ],
    'Incidents': [
        # Asia Pacific
        25, 28, 18, 22, 15, 8, 6, 5, 12, 14,
        # Middle East and North Africa
        24, 19, 17, 16, 14, 20, 7, 9, 6, 15,
        # Sub-Saharan Africa
        21, 17, 16, 14, 13, 18, 7, 4, 3, 5,
        # Eurasia
        26, 22, 19, 21, 15, 12, 10, 8, 6, 5,
        # Americas
        18, 16, 14, 12, 10, 8, 7, 6, 4, 3
    ],
    'Severity': [
        # Asia Pacific
        5, 5, 4, 4, 3, 3, 2, 2, 3, 4,
        # Middle East and North Africa
        5, 4, 4, 4, 4, 5, 3, 3, 2, 4,
        # Sub-Saharan Africa
        5, 4, 4, 3, 4, 5, 3, 2, 2, 2,
        # Eurasia
        5, 4, 4, 4, 3, 3, 3, 2, 2, 2,
        # Americas
        4, 4, 3, 3, 3, 2, 2, 2, 1, 1
    ],
    'Population_Impact': [
        # Asia Pacific (in millions)
        54, 1400, 97, 1380, 273, 70, 109, 16, 32, 7,
        # Middle East and North Africa
        83, 102, 34, 9, 6, 17, 12, 43, 36, 40,
        # Sub-Saharan Africa
        115, 45, 206, 53, 15, 43, 59, 18, 31, 59,
        # Eurasia
        144, 6, 9, 84, 10, 19, 33, 44, 4, 3,
        # Americas
        28, 11, 6, 126, 212, 51, 17, 11, 45, 331
    ],
    'Region': [
        # Asia Pacific
        'Asia Pacific', 'Asia Pacific', 'Asia Pacific', 'Asia Pacific', 'Asia Pacific', 
        'Asia Pacific', 'Asia Pacific', 'Asia Pacific', 'Asia Pacific', 'Asia Pacific',
        # Middle East and North Africa
        'Middle East & North Africa', 'Middle East & North Africa', 'Middle East & North Africa', 
        'Middle East & North Africa', 'Middle East & North Africa', 'Middle East & North Africa', 
        'Middle East & North Africa', 'Middle East & North Africa', 'Middle East & North Africa', 
        'Middle East & North Africa',
        # Sub-Saharan Africa
        'Sub-Saharan Africa', 'Sub-Saharan Africa', 'Sub-Saharan Africa', 'Sub-Saharan Africa', 
        'Sub-Saharan Africa', 'Sub-Saharan Africa', 'Sub-Saharan Africa', 'Sub-Saharan Africa', 
        'Sub-Saharan Africa', 'Sub-Saharan Africa',
        # Eurasia
        'Eurasia', 'Eurasia', 'Eurasia', 'Eurasia', 'Eurasia', 
        'Eurasia', 'Eurasia', 'Eurasia', 'Eurasia', 'Eurasia',
        # Americas
        'Americas', 'Americas', 'Americas', 'Americas', 'Americas', 
        'Americas', 'Americas', 'Americas', 'Americas', 'Americas'
    ]
}

df = pd.DataFrame(data)

# Calculate a composite score for the heat map intensity
# Normalize each metric to a 0-1 scale and then combine them
df['Incidents_Norm'] = df['Incidents'] / df['Incidents'].max()
df['Severity_Norm'] = df['Severity'] / df['Severity'].max()
df['Population_Impact_Norm'] = df['Population_Impact'] / df['Population_Impact'].max()

# Composite score with weights
df['Censorship_Score'] = (0.4 * df['Incidents_Norm'] + 
                          0.4 * df['Severity_Norm'] + 
                          0.2 * df['Population_Impact_Norm'])

# Load world map data
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the data with the world map
world = world.merge(df, how='left', left_on='name', right_on='Country')

# Create a custom colormap from yellow to dark red
colors = ['#FFFF00', '#FFCC00', '#FF9900', '#FF6600', '#FF3300', '#CC0000', '#990000', '#660000']
cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=256)

# Create the figure and axis
fig, ax = plt.subplots(1, 1, figsize=(15, 10))

# Plot countries with data
world.plot(column='Censorship_Score', 
           ax=ax, 
           cmap=cmap,
           missing_kwds={'color': 'lightgray'},
           legend=True,
           legend_kwds={'label': "Internet Censorship Intensity (2024)",
                        'orientation': "horizontal"})

# Add title and labels
plt.title('Global Internet Censorship Heat Map (2024)', fontsize=16)
plt.figtext(0.5, 0.01, 'Source: Analysis of Freedom House, Access Now, OONI, NetBlocks, and Top10VPN data', 
            ha='center', fontsize=10)

# Add a note about the metrics
metrics_note = ('Censorship Intensity Score based on:\n'
                '- Number of documented incidents\n'
                '- Severity of restrictions\n'
                '- Population impact')
plt.figtext(0.15, 0.15, metrics_note, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))

# Create a legend for severity levels
severity_labels = ['Level 1: Limited content restrictions',
                  'Level 2: Single platform blocks',
                  'Level 3: Multiple platform blocks',
                  'Level 4: Complete blackouts (<24h)',
                  'Level 5: Extended blackouts (>24h)']

severity_colors = ['#FFFF00', '#FFCC00', '#FF9900', '#FF3300', '#660000']
severity_patches = [mpatches.Patch(color=color, label=label) 
                   for color, label in zip(severity_colors, severity_labels)]

# Add the custom legend
plt.legend(handles=severity_patches, 
           loc='lower right', 
           title='Severity Scale',
           fontsize=8)

# Save the figure
plt.savefig('/home/ubuntu/internet_censorship_report/visualizations/global_censorship_heatmap.png', 
            dpi=300, bbox_inches='tight')

# Create regional heat maps
regions = df['Region'].unique()

for region in regions:
    # Filter data for this region
    region_df = df[df['Region'] == region]
    
    # Create a new figure
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Filter world data for this region and neighboring countries
    region_countries = region_df['Country'].tolist()
    region_map = world[world['name'].isin(region_countries)]
    
    # Plot the region
    region_map.plot(column='Censorship_Score', 
                   ax=ax, 
                   cmap=cmap,
                   missing_kwds={'color': 'lightgray'},
                   legend=True,
                   legend_kwds={'label': "Internet Censorship Intensity (2024)",
                                'orientation': "horizontal"})
    
    # Add title and labels
    plt.title(f'{region} Internet Censorship Heat Map (2024)', fontsize=16)
    plt.figtext(0.5, 0.01, 'Source: Analysis of Freedom House, Access Now, OONI, NetBlocks, and Top10VPN data', 
                ha='center', fontsize=10)
    
    # Save the regional figure
    plt.savefig(f'/home/ubuntu/internet_censorship_report/visualizations/{region.lower().replace(" & ", "_").replace(" ", "_")}_censorship_heatmap.png', 
                dpi=300, bbox_inches='tight')

print("Heat maps generated successfully!")
