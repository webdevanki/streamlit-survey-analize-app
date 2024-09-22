import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from openai import OpenAI

from dotenv import dotenv_values
import os

MODEL = "gpt-4o"
env = dotenv_values(".env")
openai_client = OpenAI(api_key=env["OPENAI_API_KEY"])

df = pd.read_csv('survey_data.csv',sep=';')

# Initialize session state for filters
if 'age_filter' not in st.session_state:
    st.session_state.age_filter = 'Show all'
if 'gender_filter' not in st.session_state:
    st.session_state.gender_filter = 'Show all'
if 'edu_filter' not in st.session_state:
    st.session_state.edu_filter = []
if 'industry_filter' not in st.session_state:
    st.session_state.industry_filter = []
if 'years_of_experience_filter' not in st.session_state:
    st.session_state.years_of_experience_filter = []
if 'animal_filter' not in st.session_state:
    st.session_state.animal_filter = []
if 'fav_place_filter' not in st.session_state:
    st.session_state.fav_place_filter = []
if 'sweet_salty_filter' not in st.session_state:
    st.session_state.sweet_salty_filter = 'Show all'


# st.write("Sprawdzenie brakujących wartości:")
# st.write(df.isnull().sum())

# st.write("Informacje o danych:")
# st.write(df.info())

# Initialize session state for saved filters
if 'saved_filters' not in st.session_state:
    st.session_state.saved_filters = {}

# add non standard CSS
st.markdown("""
    <style>
    [data-testid='stSidebar']{
    
    }

    .main {
        
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

# Refresh button
if st.sidebar.button("Refresh data"):
    st.session_state.clear()  # Clear session state to reset filters
    st.rerun()    # Rerun the app to reset the UI

# Save current filters button
if st.sidebar.button("Save current filters"):
    st.session_state.saved_filters = {
        'age_filter': st.session_state.age_filter,
        'gender_filter': st.session_state.gender_filter,
        'edu_filter': st.session_state.edu_filter,
        'industry_filter': st.session_state.industry_filter,
        'years_of_experience_filter': st.session_state.years_of_experience_filter,
        'animal_filter': st.session_state.animal_filter,
        'fav_place_filter': st.session_state.fav_place_filter,
        'sweet_salty_filter': st.session_state.sweet_salty_filter
    }
    st.success(f"Filters have been saved: {st.session_state.saved_filters}")

# Load saved filters button
if st.sidebar.button("Load saved filters") and st.session_state.saved_filters:
    st.session_state.age_filter = st.session_state.saved_filters.get('age_filter', 'Show all')
    st.session_state.gender_filter = st.session_state.saved_filters.get('gender_filter', 'Show all')
    st.session_state.edu_filter = st.session_state.saved_filters.get('edu_filter', [])
    st.session_state.industry_filter = st.session_state.saved_filters.get('industry_filter', [])
    st.session_state.years_of_experience_filter = st.session_state.saved_filters.get('years_of_experience_filter', [])
    st.session_state.animal_filter = st.session_state.saved_filters.get('animal_filter', [])
    st.session_state.fav_place_filter = st.session_state.saved_filters.get('fav_place_filter', [])
    st.session_state.sweet_salty_filter = st.session_state.saved_filters.get('sweet_salty_filter', 'Show all')
    
    st.success(f"Loaded filters: {st.session_state.saved_filters}")

    time.sleep(2)
    st.rerun()


# st.sidebar.write("Current session state:")
# st.sidebar.write(st.session_state)

st.sidebar.header("Filter data:")

# Sidebar with filters
unique_ages = ['Show all'] + list(df['age'].unique())
age_filter = st.sidebar.selectbox("Choose age range:", unique_ages, index=unique_ages.index(st.session_state.age_filter))
st.session_state.age_filter = age_filter

unique_genders = ['Show all'] + list(df['gender'].unique())
gender_filter = st.sidebar.selectbox("Choose gender:", unique_genders, index=unique_genders.index(st.session_state.gender_filter))
st.session_state.gender_filter = gender_filter

edu_filter = st.sidebar.multiselect("Select education:", options=list(df['edu_level'].unique()), default=st.session_state.edu_filter)
st.session_state.edu_filter = edu_filter

industry_filter = st.sidebar.multiselect("Select industry:", options=list(df['industry'].unique()), default=st.session_state.industry_filter)
st.session_state.industry_filter = industry_filter

years_of_experience_options = ['Show all'] + list(df['years_of_experience'].unique())
years_of_experience_filter = st.sidebar.multiselect("Select years of experience:", options=years_of_experience_options, default=st.session_state.years_of_experience_filter)
st.session_state.years_of_experience_filter = years_of_experience_filter

animal_filter = st.sidebar.multiselect("Select fav animal:", options=list(df['fav_animals'].unique()), default=st.session_state.animal_filter)
st.session_state.animal_filter = animal_filter

fav_place_filter = st.sidebar.multiselect("Select fav place to relax:", options=list(df['fav_place'].unique()), default=st.session_state.fav_place_filter)
st.session_state.fav_place_filter = fav_place_filter

sweet_salty_options = ['Show all'] + list(df['sweet_or_salty'].unique())
sweet_salty_filter = st.sidebar.selectbox("Choose taste preference:", sweet_salty_options, index=sweet_salty_options.index(st.session_state.sweet_salty_filter))
st.session_state.sweet_salty_filter = sweet_salty_filter

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

# add download button for filtered data
if st.button("Download filtered data"):
    filtered_data.to_csv('filtered_data.csv', sep=';', index=False)
    st.success("Data was downloaded as 'filtered_data.csv'.")  


# Show descriptive statistics
if filtered_data.shape[0] > 0:  # Check if there is any filtered data
    st.write("Descriptive statistics:")
    st.write(filtered_data.describe(include='all'))  # Include all columns
else:
    st.write("No data to display statistics")

st.markdown("---")

# Function to plot bar chart for selected column
def plot_bar_chart(data, column):
    plt.figure(figsize=(10, 5))
    data[column].value_counts().plot(kind='bar', color='skyblue')
    plt.title(f'Distribution of values ​​in a column {column}')
    plt.xlabel(column)
    plt.ylabel('Number of occurrences')
    plt.xticks(rotation=45)
    st.pyplot(plt)

st.sidebar.markdown("---") 
# Sidebar to select a column for the chart
column_to_plot = st.sidebar.selectbox("Choose column to visualization:", df.columns)

# Display the plot
st.write("Show distribution of values in a choosen column")

if filtered_data.shape[0] > 0:  # Check if there is any filtered data
    plot_bar_chart(filtered_data, column_to_plot)
else:
    st.write("No data to show plot.")

def generate_interpretation(data, column):
    # Prompt for model
    prompt = f"Please interpret the following data distribution: {data[column].value_counts().to_dict()} for the column '{column}'."
    
    # call the OpenAI API using the openai_client and the model
    response = openai_client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # get the response content with correct access to attributes
    return response.choices[0].message.content

# Add a button to generate the interpretation
if st.button("Generate Interpretation"):
    if filtered_data.shape[0] > 0:  # Check if there is any filtered data
        interpretation = generate_interpretation(filtered_data, column_to_plot)
        st.session_state.interpretation = interpretation  # Store in session state
        st.write("Interpretation of the results:")
        st.write(interpretation)
    else:
        st.warning("No data available to interpret.")
        
# Display the stored interpretation if it exists
if 'interpretation' in st.session_state:
    st.write("Previous Interpretation of the results:")
    st.write(st.session_state.interpretation)

