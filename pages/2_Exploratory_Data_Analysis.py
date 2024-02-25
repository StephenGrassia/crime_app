import streamlit as st
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import datetime

today = datetime.date.today()

st.set_page_config(page_title="EDA",
                   layout="wide")

@st.cache_data 
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data("https://opendata.arcgis.com/api/v3/datasets/67bc708103e746f18e216c32ba39febe_0/downloads/data?format=csv&spatialRefId=4326&where=1%3D1")

@st.cache_data
def normalization(dataframe):
    most_frequent_desc = dataframe.groupby('Offense_Code')['Offense_Description'].agg(lambda x: x.mode().iloc[0])
    category_to_desc = most_frequent_desc.to_dict()
    dataframe['Offense_Description'] = dataframe['Offense_Code'].map(category_to_desc)
    dataframe['Date_Occurred'] = pd.to_datetime(dataframe['Date_Occurred']).dt.normalize()
    dataframe['year'], dataframe['month'], dataframe['day_of_week'] = dataframe['Date_Occurred'].dt.year, dataframe['Date_Occurred'].dt.month, dataframe['Date_Occurred'].dt.day_of_week
    return dataframe
df = normalization(df)

st.markdown("<h1 style='text-align: center; color: black;'>Exploratory Data Analysis</h1>", unsafe_allow_html=True)
st.write(
    """
    Exploratory Data Analysis, according to [GeeksforGeeks](https://www.geeksforgeeks.org/what-is-exploratory-data-analysis), is the method of exploring datasets to discover patterns, 
    identify outliers, and relationships between variables. In this section, we will build upon the data clean-up from the previous section, and 
    visualize the data with various methods.
    - Total Number of rows
    - Top 5 Offenses
        - Top 5 Neighborhoods per Top 5 Offenses
    - Top 5 Neighborhoods
        - top 5 Offenses per Top 5 Neighborhoods
    """
)

## Total count
st.markdown(
    '''
    #### Let start out with finding the total number of rows. 
    '''
)

code1 = '''countRows = len(df)
countRows
'''
st.code(code1, language='python')

countRows = len(df)
countRows

count_text = f"So, between ***2018-01-01*** to ***{today}***, there have been ***{countRows}*** incidents where the police have been called."
st.markdown(count_text)
st.markdown(
    '''
    #### Now, let's find the Top 5 offenses using the ***Offense_Description*** column
    '''
)

code2 = '''top5_offenses = pd.DataFrame(df['Offense_Description'].value_counts().head(5))
top5_offenses
'''
st.code(code2, language='python')

top5_offenses = pd.DataFrame(df['Offense_Description'].value_counts().head(5))
st.dataframe(top5_offenses)

st.markdown(
    '''
    #### Since 2018, the offense with the most incidents is ***Larceny, From Motor Vehicle*** with a count of ***13,325.***
    #### The above code will get the rows in the dataframe that contain one of the ***Top 5 Offenses***. Below, we can subset to show rows that have the corresponding ***Offense_Description***.
    '''
)

# Get the top 5 offenses
top5_offenses = df['Offense_Description'].value_counts().head(5).index

# Let the user select an offense
offenses = st.selectbox('Select a Top 5 Offense', top5_offenses)

# Filter data
filtered_data = df[df['Offense_Description'] == offenses]

def col_df(col):
    count_df = pd.DataFrame(filtered_data[col].value_counts().head(10))
    count_df.reset_index(inplace=True)
    return count_df
sub_df = col_df('Subdivision')


sub_df = sub_df.sort_values(by='count', ascending=False).head(10)

barchart, heatmap_dm, heatmap_ym = st.tabs(["Bar Chart", "Heat Map (Day of Week/Month)", "Heat Map(Month, Year)"])

with barchart:
    plt.figure(figsize=(15,6))
    plot = sns.barplot(
        data=sub_df,
        x='Subdivision',
        y='count'
    )
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Subdivision")
    plt.ylabel("Count of Incidents")

    st.pyplot(plot.get_figure())

with heatmap_dm:
    filtered_data['num'] = 1
    dayMonth = filtered_data.groupby(by=['day_of_week', 'month']).count()['num'].unstack()
    plt.figure(figsize=(15,6))
    hm = sns.heatmap(dayMonth, cmap='coolwarm')
    plt.title(f"'{offenses} 'Incidents by Day of Week & Month")
    plt.xlabel("Month")
    plt.ylabel("Day of Week")
    
    st.pyplot(hm.get_figure())

with heatmap_ym:
    filtered_data['num'] = 1
    monthYear = filtered_data.groupby(by=['month', 'year']).count()['num'].unstack()
    plt.figure(figsize=(15,6))
    hy = sns.heatmap(monthYear, cmap='coolwarm')
    plt.title(f"'{offenses} 'Incidents by Month, & Year")
    plt.xlabel("Year")
    plt.ylabel("Month")
    
    st.pyplot(hy.get_figure())
## Analysis BreakDown

multi = '''Going through each offense, we can see that the largest ***Subdivision*** in every one of the ***Top 5 Offense_Description*** is ***OceanFront - 31st St South***.  
Doing some research, this neighborhood is in the middle of ***OceanFront/Atlantic Ave***, a high-tourist area. ***Larceny, From Motor Vehicle*** is the only offense that is
is consistant throughout the week, but only in July. This can be due to Virginia Beach, especially the OceanFront, is a tourist destination.  
'''
st.markdown(multi)

code_text = '''Below is the code for making the charts in any python interface. 
It may look complicated, but it is easy, and simple to follow/understand.
We will first start off with the barplot.'''
st.markdown(code_text)

code3 = '''plt.figure(figsize=(15,6))
sns.barplot(
    data=df,
    x='Subdivision',
    y='count'
)
plt.xticks(rotation=45, ha='right')
plt.xlabel("Subdivision")
plt.ylabel("Count of Incidents")

plt.tight_layout()
plt.show()'''

st.code(code3, language='python')

