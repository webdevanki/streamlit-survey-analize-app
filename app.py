import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('survey_data.csv',sep=';')


st.write("Dane:")
st.write(df.head())

# st.write("Sprawdzenie brakujących wartości:")
# st.write(df.isnull().sum())

# st.write("Informacje o danych:")
# st.write(df.info())

# Dodanie niestandardowego CSS
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




# Sidebar z filtrami
age_filter = st.sidebar.selectbox("Wybierz przedział wiekowy:", ['Wszystkie'] + list(df['age'].unique()))
gender_filter = st.sidebar.selectbox("Wybierz płeć:", ['Wszystkie'] + list(df['gender'].unique()))
edu_filter = st.sidebar.multiselect("Wybierz wykształcenie:", options=list(df['edu_level'].unique()), default=[])
industry_filter = st.sidebar.multiselect("Wybierz branżę:", options=list(df['industry'].unique()), default=[])
years_of_experience_filter = st.sidebar.multiselect("Wybierz lata doświadczenia:", options=list(df['years_of_experience'].unique()), default=[])
animal_filter = st.sidebar.multiselect("Wybierz ulubione zwierzę:", options=list(df['fav_animals'].unique()), default=[])
fav_place_filter = st.sidebar.multiselect("Wybierz ulubione miejsce do relaksu:", options=list(df['fav_place'].unique()), default=[])
sweet_salty_filter = st.sidebar.selectbox("Wybierz preferencję smakową:", ['Wszystkie'] + list(df['sweet_or_salty'].unique()))

# Filtrowanie danych na podstawie wybranych filtrów
filtered_data = df.copy()

if age_filter != 'Wszystkie':
    filtered_data = filtered_data[filtered_data['age'] == age_filter]

if gender_filter != 'Wszystkie':
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

if sweet_salty_filter != 'Wszystkie':
    filtered_data = filtered_data[filtered_data['sweet_or_salty'] == sweet_salty_filter]

# Wyświetlenie przefiltrowanych danych
st.write("Przefiltrowane dane:")
st.write(filtered_data)

