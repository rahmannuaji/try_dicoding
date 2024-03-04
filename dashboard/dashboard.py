import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import Dataset
# day dataset
day_df = pd.read_csv("dashboard/day_df.csv")
#print(day_df.head())
# hour dataset
hour_df = pd.read_csv("dashboard/hour_df.csv")
#print(hour_df.head())

sns.set(style='dark')

def get_total_count_by_hour_df(hour_df):
    hour_count_df = hour_df.groupby(by="hours").agg({"count_cr": ["sum"]})
    return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="dteday").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df

def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order (hour_df):
    sum_order_items_df = hour_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def jen_season (day_df):
    season_df = day_df.groupby(by="season").count_cr.sum().reset_index()
    return season_df

days_df = pd.read_csv("dashboard/day_df.csv")
hours_df = pd.read_csv("dashboard/hour_df.csv")

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

with (st.sidebar):
    # Menambahkan logo sepeda
    st.image("https://media.istockphoto.com/id/1329906434/vector/city-bicycle-sharing-system-isolated-on-white.jpg?s=612x612&w=0&k=20&c=weiMZhJoWWzNGtx7khfXPbE3s2Lpw5n6M7iWoxCsBPU=")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Date',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])

main_df_days = days_df[(days_df["dteday"] >= str(start_date)) &
                       (days_df["dteday"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) &
                        (hours_df["dteday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = jen_season(main_df_hour)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('🚲Bike Sharing Together🚲')

st.subheader('Description')

# Description
description = """
Bike sharing systems are a new generation of traditional bike rentals where the whole process from membership, rental, 
and return back has become automatic. Through these systems, users are able to easily rent a bike from a particular position and return it back at another position. 
Currently, there are over 500 bike-sharing programs around the world which are composed of over 500,000 bicycles. 
Today, there exists great interest in these systems due to their important role in traffic, environmental, and health issues.
"""
st.write(f'<div style="text-align: justify">{description}</div>', unsafe_allow_html=True)

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = day_df_count_2011.count_cr.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("Trend Bike Rentals")

days_df['month'] = pd.Categorical(days_df['month'], categories=
    ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    ordered=True)

monthly_counts = days_df.groupby(by=["month","year"]).agg({
    "count_cr": "sum"
}).reset_index()

fig3, ax3 = plt.subplots()
sns.lineplot(
    data=monthly_counts,
    x="month",
    y="count_cr",
    hue="year",
    palette="icefire",
    marker="o")

plt.title("Total number of bicycles rented by Month and year")
plt.xlabel(None)
plt.ylabel(None)
plt.legend(title="Year", loc="upper left", bbox_to_anchor=(1, 0.5))
plt.tight_layout()
st.pyplot(fig3)

st.subheader("Bike rental performance in recent years")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_df["dteday"],
    days_df["count_cr"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Most and Least Time for Bike Rentals")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.head(5),
            palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Most Time for Bike Rentals", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.sort_values(by="hours", ascending=True).head(5),
            palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)", fontsize=30)
ax[1].set_title("Least Time for Bike Rentals", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Most Bike Rental Seasons")

colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"]
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="count_cr",
    x="season",
    data=season_df.sort_values(by="season", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Rental Bike Each Season", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader("Rental Bike by Condition")

fig1, ax1 = plt.subplots(figsize=(20, 10))
sns.barplot(
    x='weather_situation',
    y='count_cr',
    hue='weather_situation',
    data=days_df,
    palette='icefire',
    order=days_df.groupby("weather_situation")["count_cr"].sum().sort_values(ascending=False).index)

plt.title('Number of Bike Rentals by weather condition', fontsize=20, weight='bold', color='green')
plt.xlabel('Weather', fontsize=15, weight='bold', color='green')
plt.ylabel('Count', fontsize=15, weight='bold', color='green')
st.pyplot(fig1)

st.subheader("Comparison of Registered Users and Casual Users")

labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1)

fig2, ax2 = plt.subplots()
ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', colors=['#FF9999', '#66B2FF'],
        shadow=True, startangle=90)
ax2.axis('equal')
st.pyplot(fig2)

