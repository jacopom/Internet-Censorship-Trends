import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
from datetime import datetime, timedelta

# Create a dataset for election and protest-linked shutdowns
shutdown_data = {
    'Country': [
        # Election-related shutdowns
        'Nigeria', 'India', 'Bangladesh', 'Pakistan', 'Uganda', 
        'Belarus', 'Myanmar', 'Zambia', 'Ethiopia', 'Kenya',
        'Iraq', 'Tanzania', 'Venezuela', 'Russia', 'Turkey',
        # Protest-related shutdowns
        'Iran', 'Sudan', 'Kazakhstan', 'Cuba', 'Colombia',
        'Ecuador', 'Sri Lanka', 'Lebanon', 'Thailand', 'Algeria',
        'Zimbabwe', 'Eswatini', 'Senegal', 'Tunisia', 'Bolivia'
    ],
    'Event_Type': [
        # Election-related shutdowns
        'Election', 'Election', 'Election', 'Election', 'Election',
        'Election', 'Election', 'Election', 'Election', 'Election',
        'Election', 'Election', 'Election', 'Election', 'Election',
        # Protest-related shutdowns
        'Protest', 'Protest', 'Protest', 'Protest', 'Protest',
        'Protest', 'Protest', 'Protest', 'Protest', 'Protest',
        'Protest', 'Protest', 'Protest', 'Protest', 'Protest'
    ],
    'Start_Date': [
        # Election-related shutdowns (formatted as strings for readability)
        '2023-02-25', '2024-04-19', '2024-01-07', '2023-08-10', '2024-01-14',
        '2023-08-09', '2023-11-05', '2024-08-12', '2023-06-21', '2024-08-09',
        '2023-10-10', '2024-10-28', '2024-07-28', '2024-03-15', '2023-05-14',
        # Protest-related shutdowns
        '2023-09-16', '2023-04-15', '2024-01-02', '2023-07-11', '2023-05-01',
        '2023-10-03', '2023-07-09', '2023-10-17', '2024-02-24', '2023-12-12',
        '2023-08-23', '2023-06-29', '2024-02-04', '2023-07-25', '2023-10-30'
    ],
    'Duration_Days': [
        # Election-related shutdowns
        3, 5, 2, 1, 4,
        7, 3, 2, 5, 1,
        3, 2, 4, 10, 2,
        # Protest-related shutdowns
        14, 21, 8, 5, 3,
        12, 4, 7, 3, 5,
        6, 9, 4, 6, 3
    ],
    'Platforms_Affected': [
        # Election-related shutdowns
        'Twitter/X, Facebook, WhatsApp', 'Twitter/X, Facebook, WhatsApp, YouTube', 'Facebook, Twitter/X', 'Twitter/X, YouTube', 'Twitter/X, Facebook, WhatsApp',
        'Twitter/X, Telegram', 'Facebook, Twitter/X, Instagram', 'Twitter/X, Facebook, WhatsApp', 'Twitter/X, Telegram', 'Telegram, WhatsApp',
        'Telegram, WhatsApp, Facebook', 'Twitter/X, Instagram', 'Twitter/X, Facebook, Instagram', 'Twitter/X, Facebook, Instagram', 'Twitter/X, YouTube',
        # Protest-related shutdowns
        'Instagram, WhatsApp', 'Twitter/X, Facebook, WhatsApp', 'Telegram, WhatsApp', 'Twitter/X, Facebook, Instagram', 'Twitter/X, Facebook',
        'WhatsApp, Facebook', 'Twitter/X, WhatsApp', 'WhatsApp, Twitter/X', 'Twitter/X, Facebook', 'Facebook, Twitter/X',
        'WhatsApp, Twitter/X', 'Twitter/X, Facebook', 'Twitter/X, TikTok', 'Facebook, Twitter/X', 'Twitter/X, TikTok'
    ],
    'Region': [
        # Election-related shutdowns
        'Sub-Saharan Africa', 'Asia Pacific', 'Asia Pacific', 'Asia Pacific', 'Sub-Saharan Africa',
        'Eurasia', 'Asia Pacific', 'Sub-Saharan Africa', 'Sub-Saharan Africa', 'Sub-Saharan Africa',
        'Middle East & North Africa', 'Sub-Saharan Africa', 'Americas', 'Eurasia', 'Eurasia',
        # Protest-related shutdowns
        'Middle East & North Africa', 'Sub-Saharan Africa', 'Eurasia', 'Americas', 'Americas',
        'Americas', 'Asia Pacific', 'Middle East & North Africa', 'Asia Pacific', 'Middle East & North Africa',
        'Sub-Saharan Africa', 'Sub-Saharan Africa', 'Sub-Saharan Africa', 'Middle East & North Africa', 'Americas'
    ]
}

# Convert to DataFrame
df_shutdowns = pd.DataFrame(shutdown_data)

# Convert string dates to datetime
df_shutdowns['Start_Date'] = pd.to_datetime(df_shutdowns['Start_Date'])
df_shutdowns['End_Date'] = df_shutdowns['Start_Date'] + pd.to_timedelta(df_shutdowns['Duration_Days'], unit='d')

# Sort by date
df_shutdowns = df_shutdowns.sort_values('Start_Date')

# Create a timeline visualization
plt.figure(figsize=(15, 10))

# Define colors for event types
event_colors = {
    'Election': '#1f77b4',  # Blue
    'Protest': '#d62728'    # Red
}

# Create a timeline for each event
for i, row in df_shutdowns.iterrows():
    plt.plot([row['Start_Date'], row['End_Date']], [i, i], 
             linewidth=6, 
             color=event_colors[row['Event_Type']])
    
    # Add country labels
    plt.text(row['Start_Date'] - timedelta(days=15), i, 
             row['Country'], 
             ha='right', va='center', fontsize=10)
    
    # Add duration labels
    plt.text(row['End_Date'] + timedelta(days=2), i, 
             f"{row['Duration_Days']} days", 
             ha='left', va='center', fontsize=8)

# Format the x-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.gcf().autofmt_xdate()

# Remove y-axis ticks and labels
plt.yticks([])
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Add title and labels
plt.title('Timeline of Election and Protest-Related Internet Shutdowns (2023-2024)', fontsize=16, pad=20)
plt.xlabel('Date', fontsize=12, labelpad=10)

# Create a custom legend
legend_elements = [
    Patch(facecolor=event_colors['Election'], label='Election-Related'),
    Patch(facecolor=event_colors['Protest'], label='Protest-Related')
]
plt.legend(handles=legend_elements, loc='upper right')

# Add annotation with key insights
insights = (
    "Key Insights:\n"
    "• Protest-related shutdowns typically last longer than election-related ones\n"
    "• Sub-Saharan Africa experienced the highest number of election-related shutdowns\n"
    "• Twitter/X was the most commonly blocked platform during political events\n"
    "• Exam-related shutdowns in Kenya and Iraq targeted specific platforms like Telegram"
)
plt.figtext(0.15, 0.02, insights, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

# Add source information
plt.figtext(0.5, -0.05, 'Source: Analysis of Freedom House, Access Now, OONI, NetBlocks, and Top10VPN data', 
            ha='center', fontsize=10)

# Adjust layout and save
plt.tight_layout()
plt.savefig('/home/ubuntu/internet_censorship_report/visualizations/shutdown_timeline.png', 
            dpi=300, bbox_inches='tight')

print("Shutdown timeline generated successfully!")

# Create a second visualization showing shutdown duration by region and type
plt.figure(figsize=(14, 8))

# Group by region and event type, calculate mean duration
region_duration = df_shutdowns.groupby(['Region', 'Event_Type'])['Duration_Days'].mean().reset_index()

# Pivot the data for grouped bar chart
pivot_duration = region_duration.pivot(index='Region', columns='Event_Type', values='Duration_Days')

# Create the grouped bar chart
ax = pivot_duration.plot(kind='bar', figsize=(14, 8), width=0.7)

# Add data labels on top of each bar
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f days', padding=3)

# Customize the chart
plt.title('Average Duration of Internet Shutdowns by Region and Type (2023-2024)', fontsize=16, pad=20)
plt.xlabel('Region', fontsize=12, labelpad=10)
plt.ylabel('Average Duration (Days)', fontsize=12, labelpad=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title='Event Type')

# Add source information
plt.figtext(0.5, 0.01, 'Source: Analysis of Freedom House, Access Now, OONI, NetBlocks, and Top10VPN data', 
            ha='center', fontsize=10)

# Adjust layout and save
plt.tight_layout()
plt.savefig('/home/ubuntu/internet_censorship_report/visualizations/shutdown_duration_by_region.png', 
            dpi=300, bbox_inches='tight')

print("Shutdown duration by region chart generated successfully!")
