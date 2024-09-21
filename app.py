import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('survey_data.csv',sep=';')


# st.write("Sprawdzenie brakujących wartości:")
# st.write(df.isnull().sum())

# st.write("Informacje o danych:")
# st.write(df.info())

# add non standard CSS
st.markdown("""
    <style>
    [data-testid='stSidebar']{
        position: relative;
        margin-left: 0;
        z-index: 0;
    }

    .main {
        margin-left: 300px; /* Dopasuj szerokość sidebar, np. 250px */
    }
    </style>
    """, unsafe_allow_html=True)

# Map gender values
gender_mapping = {0: "Man", 1: "Woman"}
df['gender'] = df['gender'].map(gender_mapping)

# replace null and unknown value by text info
df = df.fillna('Not specified')
df['age'] = df['age'].replace('unknown', 'No data')
df['years_of_experience'] = df['years_of_experience'].replace('NaN', 'Brak danych')

# set order for years of experience 

experience_order = ['0-2', '3-5', '6-10', '11-15', '>=16', 'Brak danych']
df['years_of_experience'] = pd.Categorical(df['years_of_experience'], categories=experience_order, ordered=True)

st.write("Data:")
st.write(df.head())

# Sidebar with filters
age_filter = st.sidebar.selectbox("Choose age range:", ['Show all'] + list(df['age'].unique()))
gender_filter = st.sidebar.selectbox("Choose gender:", ['Show all'] + list(df['gender'].unique()))
edu_filter = st.sidebar.multiselect("Select education:", options=list(df['edu_level'].unique()), default=[])
industry_filter = st.sidebar.multiselect("Select industry:", options=list(df['industry'].unique()), default=[])
years_of_experience_filter = st.sidebar.multiselect("Select years of experience:", options=list(df['years_of_experience'].unique()), default=[])
animal_filter = st.sidebar.multiselect("Select fav animal:", options=list(df['fav_animals'].unique()), default=[])
fav_place_filter = st.sidebar.multiselect("Select fav place to relax:", options=list(df['fav_place'].unique()), default=[])
sweet_salty_filter = st.sidebar.selectbox("Choose taste preference:", ['Show all'] + list(df['sweet_or_salty'].unique()))

# filter data if option is choosen
filtered_data = df.copy()

if age_filter != 'Show all':
    filtered_data = filtered_data[filtered_data['age'] == age_filter]

if gender_filter != 'Show all':
    filtered_data = filtered_data[filtered_data['gender'] == gender_filter]

if edu_filter:
    filtered_data = filtered_data[filtered_data['edu_level'].isin(edu_filter)]

if industry_filter:
    filtered_data = filtered_data[filtered_data['industry'].isin(industry_filter)]

if years_of_experience_filter:
    filtered_data = filtered_data[filtered_data['years_of_experience'].isin(years_of_experience_filter)]

if animal_filter:
    filtered_data = filtered_data[filtered_data['fav_animals'].isin(animal_filter)]

if fav_place_filter:
    filtered_data = filtered_data[filtered_data['fav_place'].isin(fav_place_filter)]

if sweet_salty_filter != 'Show all':
    filtered_data = filtered_data[filtered_data['sweet_or_salty'] == sweet_salty_filter]

# show filtered data
st.write("Filtered data:")
st.write(filtered_data)

# Show number of rows
num_rows = filtered_data.shape[0]
st.write(f"Number of results: {num_rows}")
