import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style='dark')


all_df = pd.read_csv("dashboard/all_data.csv")

with st.sidebar:
    st.title("Bike Rentals Dashboard")
    st.markdown("## Visualisasi Data Penyewaan Sepeda")

    start_date = pd.to_datetime("2011-01-01")
    end_date = pd.to_datetime("2012-12-31")
    selected_date = st.date_input("Pilih Tanggal", value=start_date, min_value=start_date, max_value=end_date)
    st.write("Tanggal yang dipilih:", selected_date)


grouped_weekday_all = all_df.groupby(['weekday_x']).agg({
    'casual_x': 'sum',
    'registered_x': 'sum',
    'cnt_x': 'sum'
}).reset_index()

correlation_all = all_df[['cnt_x', 'season_x', 'temp_x', 'hum_x', 'windspeed_x', 'weathersit_x']].corr()
season_rentals_all = all_df.groupby(by="season_x").instant.nunique().sort_values(ascending=False)
weather_rentals_all = all_df.groupby(by="weathersit_x").instant.nunique().sort_values(ascending=False)
monthly_rentals_all = all_df.groupby(by="mnth_x")['cnt_x'].sum().reset_index()
grouped_month_all = all_df.groupby(['mnth_x']).agg({
    'casual_x': 'sum',
    'registered_x': 'sum',
    'cnt_x': 'sum'
}).reset_index()
hourly_rent_df = all_df.groupby(by="hr")['cnt_y'].sum().reset_index()

st.title("Bike Rentals Dashboard")

# Daily Rentals by User Type
st.subheader("Daily Rentals by User Type")
fig1, ax1 = plt.subplots(figsize=(16, 8))
daily_rent_df = grouped_weekday_all
day_names = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 
             4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
daily_rent_df['weekday_x'] = daily_rent_df['weekday_x'].map(day_names)

bar_width = 0.4  
x = np.arange(len(daily_rent_df['weekday_x'])) 

ax1.bar(x + bar_width/2, daily_rent_df['registered_x'], width=bar_width, label='Registered', color='blue', align='center')
ax1.bar(x - bar_width/2, daily_rent_df['casual_x'], width=bar_width, label='Casual', color='orange', align='center')

ax1.set_xlabel('Days')
ax1.set_ylabel('Total Rent')
ax1.set_title('Bike Rentals by Casual and Registered Users')
ax1.set_xticks(x)  
ax1.set_xticklabels(daily_rent_df['weekday_x'])  
ax1.legend()
st.pyplot(fig1)

# Weather and season Rentals
st.subheader("Distribution Rentals by Weather and Season")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))

colors_weather = ["#72BCD4", "#D3D3D3", "#D3D3D3"]
colors_season = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="weathersit_x", y='cnt_x', data=all_df, hue='weathersit_x', ax=ax[0], palette=colors_weather)
ax[0].set_ylabel('Total Rentals')
ax[0].set_xlabel('Weather Situation (1: Clear, 2: Mist, 3: Rain, 4: Heavy Rain)')
ax[0].set_title('Distribution Rentals by Weather', loc="center", fontsize=15)
ax[0].tick_params(axis='y', labelsize=12)
sns.barplot(x="season_x", y='cnt_x', data=all_df, hue='season_x', ax=ax[1], palette=colors_season)
ax[1].set_ylabel('Total Rentals')
ax[1].set_xlabel('Season (1: Spring, 2: Summer, 3: Fall, 4: Winter)')
ax[1].set_title('Distribution Rentals by Season', loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)
plt.suptitle("Distribution Rentals by Season and Weather", fontsize=20)
plt.tight_layout(rect=[0, 0, 1, 0.96])
st.pyplot(fig)

# Hourly Rentals
st.subheader("Number of Rentals per Hour")
fig3, ax3 = plt.subplots()
ax3.plot(hourly_rent_df['hr'], hourly_rent_df['cnt_y'], marker='o', color="pink")
ax3.set_title("Number of Rentals per Hour")
ax3.set_xlabel('Hour of the Day')
ax3.set_ylabel('Total Rentals')
st.pyplot(fig3)

# Monthly Rentals vs Average Temperature
st.subheader("Bike Rentals vs Average Temperature per Month")
monthly_summary_df = all_df.groupby('mnth_x').agg({
    'cnt_x': 'sum',
    'atemp_x': 'mean'  
}).reset_index()

month_names = {
    1: 'January', 2: 'February', 3: 'March',
    4: 'April', 5: 'May', 6: 'June',
    7: 'July', 8: 'August', 9: 'September',
    10: 'October', 11: 'November', 12: 'December'
}

monthly_summary_df['month_name'] = monthly_summary_df['mnth_x'].map(month_names)
fig4, ax4 = plt.subplots(figsize=(16, 8))
ax4.scatter(monthly_summary_df['month_name'], monthly_summary_df['atemp_x'], color='red')
ax4.set_title("Bike Rentals vs Average Temperature per Month", fontsize=20)
ax4.set_xlabel("Month", fontsize=14)
ax4.set_ylabel("Average Temperature (°C)", fontsize=14)
for i, row in monthly_summary_df.iterrows():
    ax4.annotate(row['cnt_x'], (row['month_name'], row['atemp_x']), textcoords="offset points", xytext=(0,10), ha='center')
st.pyplot(fig4)

# correlation matrix
st.subheader("Correlation Matrix")
st.dataframe(correlation_all)

# Temperature Binning
st.subheader("Bike Rentals by Temperature Range")
bins = [0, 10, 20, 30, 40]
labels = ['0-10°C', '11-20°C', '21-30°C', '31-40°C']
monthly_summary_df['temp_bin'] = pd.cut(monthly_summary_df['atemp_x']* 50, bins=bins, labels=labels)
binned_rentals = monthly_summary_df.groupby('temp_bin')['cnt_x'].sum().reset_index()
fig5, ax5 = plt.subplots(figsize=(16, 8))
ax5.bar(binned_rentals['temp_bin'], binned_rentals['cnt_x'], color='skyblue')
ax5.set_title('Bike Rentals by Temperature')
ax5.set_xlabel('Temperature Range')
ax5.set_ylabel('Total Rentals')
st.pyplot(fig5)


if st.checkbox('Show Raw Data'):
    st.subheader('Raw Data')
    st.write(all_df)

