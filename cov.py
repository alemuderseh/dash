 number	Diff line number	Diff line change
@@ -9,9 +9,6 @@
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import matplotlib.colors as mcolors
import json

# Load the data
df = pd.read_excel("COVID_worldwide.xlsx")  # Ensure the file is in the same directory
# Data cleaning
df['cases'] = df['cases'].abs()
df['deaths'] = df['deaths'].abs()
df['dateRep'] = pd.to_datetime(df['dateRep'], format='%d/%m/%Y')
df.sort_values(by=['countriesAndTerritories', 'dateRep'], inplace=True)
# Add year column
df['year'] = df['dateRep'].dt.year
def calculate_cumulative_cases_per_100000(group):
    group['Cumulative_number_for_14_days_of_COVID-19_cases_per_100000'] = (
        group['cases'].rolling(window=14, min_periods=1).sum() / group['popData2019'] * 100000
    )
    return group
df = df.groupby('countriesAndTerritories', group_keys=False).apply(calculate_cumulative_cases_per_100000)
df.to_excel("COVID_worldwide.xlsx", index=False)  # Save the updated data back to the Excel file
st.title("Global COVID-19 Data Dashboard")
# Sidebar filters
st.sidebar.header("Filters")
selected_continent = st.sidebar.multiselect('Select Continent', df['continentExp'].unique())
if selected_continent:
    filtered_countries = df[df['continentExp'].isin(selected_continent)]['countriesAndTerritories'].unique()
    selected_country = st.sidebar.multiselect('Select Country', filtered_countries)
else:
    selected_country = st.sidebar.multiselect('Select Country', df['countriesAndTerritories'].unique())
selected_year = st.sidebar.multiselect('Select Year', df['year'].unique())
if selected_year:
    filtered_months = df[df['year'].isin(selected_year)]['dateRep'].dt.strftime('%b-%Y').unique()
    selected_month = st.sidebar.multiselect('Select Month', filtered_months)
else:
    selected_month = st.sidebar.multiselect('Select Month', df['dateRep'].dt.strftime('%b-%Y').unique())
filtered_df = df.copy()
if selected_continent:
    filtered_df = filtered_df[filtered_df['continentExp'].isin(selected_continent)]
if selected_country:
    filtered_df = filtered_df[filtered_df['countriesAndTerritories'].isin(selected_country)]
if selected_year:
    filtered_df = filtered_df[filtered_df['year'].isin(selected_year)]
if selected_month:
    filtered_df = filtered_df[filtered_df['dateRep'].dt.strftime('%b-%Y').isin(selected_month)]
if st.checkbox("Display the raw data"):
    st.subheader("COVID-19 Data")
    st.write(filtered_df)
mean_cases = filtered_df['cases'].mean()
std_cases = filtered_df['cases'].std()
median_cases = filtered_df['cases'].median()
q1_cases = filtered_df['cases'].quantile(0.25)
q3_cases = filtered_df['cases'].quantile(0.75)
total_cases = filtered_df['cases'].sum()
mean_deaths = filtered_df['deaths'].mean()
std_deaths = filtered_df['deaths'].std()
median_deaths = filtered_df['deaths'].median()
q1_deaths = filtered_df['deaths'].quantile(0.25)
q3_deaths = filtered_df['deaths'].quantile(0.75)
total_deaths = filtered_df['deaths'].sum()
cfr = (filtered_df['deaths'] / filtered_df['cases']) * 100
median_cfr = cfr.median()
q1_cfr = cfr.quantile(0.25)
q3_cfr = cfr.quantile(0.75)
def human_format(num, pos=None):
    if num >= 1e6:
        return f'{num*1e-6:.2f}M'
    elif num >= 1e3:
        return f'{num*1e-3:.2f}K'
    else:
        return str(int(num))
st.subheader("Statistics")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Cases")
    st.info(f"**Mean (SD):** {mean_cases:.2f} ({std_cases:.2f})")
    st.info(f"**Median (IQR):** {median_cases:.2f} ({q1_cases:.2f}, {q3_cases:.2f})")
    st.info(f"**Total:** {human_format(total_cases)}")
with col2:
    st.subheader("Deaths")
    st.info(f"**Mean (SD):** {mean_deaths:.2f} ({std_deaths:.2f})")
    st.info(f"**Median (IQR):** {median_deaths:.2f} ({q1_deaths:.2f}, {q3_deaths:.2f})")
    st.info(f"**Total:** {human_format(total_deaths)}")
st.subheader("Number of COVID-19 Cases and Deaths by Country")
top_countries_cases = filtered_df.groupby('countriesAndTerritories')['cases'].sum().nlargest(20)
top_countries_deaths = filtered_df.groupby('countriesAndTerritories')['deaths'].sum().nlargest(20)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
top_countries_cases.plot(kind='bar', ax=ax1, color='skyblue')
top_countries_deaths.plot(kind='bar', ax=ax2, color='salmon')
ax1.set_title("Top 20 Countries by COVID-19 Cases")
ax1.set_ylabel("Total Cases (in 100,000)")
ax1.set_xlabel("Countries")
ax1.set_yticklabels([f'{int(y/1e5):,}' for y in ax1.get_yticks()])
ax2.set_title("Top 20 Countries by COVID-19 Deaths")
ax2.set_ylabel("Total Deaths")
ax2.set_xlabel("Countries")
fig.suptitle("Figure 1: Top 20 Countries by COVID-19 Cases and Deaths", fontsize=16)
st.pyplot(fig)
