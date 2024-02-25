import streamlit as st
import pandas as pd 

st.set_page_config(page_title="About the data",
                   layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'>About the data</h1>", unsafe_allow_html=True)

st.write(
    """
    The dataset is updated a couple times per week, and sits on the City og Virginia Beachs' [Open Data](https://data.virginiabeach.gov) website, powered by ESRI. 
    Below is a step-by-step instruction on importing that data with the need for Arcpy, or other geospatial libraries.  
    """
)

st.divider()

## Import the data
st.markdown(
    '''
    #### First, we will need to import the data using Pandas, and the ***read_csv*** fucntion, and display the first 5 rows using the ***.head()*** function.
    '''
)

code1 = '''url = "https://opendata.arcgis.com/api/v3/datasets/67bc708103e746f18e216c32ba39febe_0/downloads/data?format=csv&spatialRefId=4326&where=1%3D1"
df = pd.read_csv(url)
df.head()
'''
st.code(code1, language='python')

url = "https://opendata.arcgis.com/api/v3/datasets/67bc708103e746f18e216c32ba39febe_0/downloads/data?format=csv&spatialRefId=4326&where=1%3D1"
df = pd.read_csv(url)
st.write(df.head())

st.divider()

## Check the columns
st.markdown(
    '''
    #### The following code will grab each column in the dataframe, then place them into a list.
    '''
)
code2 = '''df_col = df.columns.tolist()
df_col
'''
st.code(code2, language='python')

df_col = df.columns.tolist()
st.write(df_col)

st.markdown(
    '''
    #### The columns are easily readable, and are straight-forward in telling the reader about the data each column contains.
    '''
)

st.divider()

## Data Clean-Up
st.markdown(
    '''
    ## Data Clean-Up
    #### Sometimes, when inputting data into a table or database, values can be typed in wrong. For example, ***Virginia Beach***, and ***Virginia Beach city*** are both legitimate names for the city.
    #### In our dataset, lets pick an ***Offense_Code***, and see the matching values in ***Offense_Description***
    '''
)

code3 = '''code_13B1 = df.loc[df['Offense_Code'] == '13B1']
values = pd.DataFrame(code_13B1[('Offense_Description')].value_counts()).head(20)
values
'''
st.code(code3, language='python')

code_13B1 = df.loc[df['Offense_Code'] == '13B1']

values = pd.DataFrame(code_13B1[('Offense_Description')].value_counts()).head(20)
st.write(values)

st.markdown(
    '''
    #### The ***Offense_Code*** ***'13B1'*** is for ***Assault, Simple***. However, we can see that there are different variations of the ***Offense_Description*** under a single ***Offense_Code***. 
    #### We are going to have to standardize each ***Offense_Description*** value based on the ***Offense_Code***.
    '''
)

code4 = '''most_frequent_desc = df.groupby('Offense_Code')['Offense_Description'].agg(lambda x: x.mode().iloc[0])
category_to_desc = most_frequent_desc.to_dict()
df['Offense_Description'] = df['Offense_Code'].map(category_to_desc)
'''
st.code(code4, language='python')

most_frequent_desc = df.groupby('Offense_Code')['Offense_Description'].agg(lambda x: x.mode().iloc[0])
category_to_desc = most_frequent_desc.to_dict()
df['Offense_Description'] = df['Offense_Code'].map(category_to_desc)

st.markdown(
    '''
    #### Let's break down the code. We want to get the highest count of each ***Offense_Description*** string from each ***Offense_Code***
    #### ***most_frequent_desc = df.groupby('Offense_Code')['Offense_Description'].agg(lambda x: x.mode().iloc[0])***
    - ***most_frequent_desc*** is the name of the variable
    - ***df.groupby('Offense_Code')*** groups the dataframe by each ***Offense_Code***
    - ***.agg(lambda x: x.mode().iloc[0])*** is applied to each group, with ***x.mode*** calculates the most frequent value of each ***Offense_Description*** in each group. ***.iloc[0]*** grabs the most frequent value.
    #### ***most_frequent_desc.to_dict()*** 
    - The resulting Series from preious code. This creates a dictionary which puts the ***Offense_Code*** as the keys, and the corresponding values with the most frequent ***Offense_Description***
    #### ***df['Offense_Description'] = df['Offense_Code'].map(category_to_desc)***
    - This maps the ***Offense_Code*** and most frequent ***Offense_Description*** from the dictionary to the ***Offense_Description*** column in the ***df*** dataframe.
    #### Check to see if it worked by using the following code.
    '''
)

code5 = '''code_13B1 = df.loc[df['Offense_Code'] == '13B1']
values = pd.DataFrame(code_13B1[('Offense_Description')].value_counts()).head(20)
values
'''
st.code(code5, language='python')

code_13B1 = df.loc[df['Offense_Code'] == '13B1']

values = pd.DataFrame(code_13B1[('Offense_Description')].value_counts()).head(20)
st.write(values)

st.markdown(
    '''
    #### Success. Now let's look at the columns, ***Date_Occurred*** and ***Date_Found***.
    #### First, we will check the dtypes for each column
    '''
)

code6 = '''pd.DataFrame(df.dtypes, columns=['Datatype']).rename_axis('Columns')'''
st.code(code6, language='python')

info = pd.DataFrame(df.dtypes, columns=['Datatype']).rename_axis('Columns')
st.dataframe(info)

st.markdown(
    '''
    #### Both date columns have the dtype ***object***.
    #### Both columns contain a date, and time value. We will need to separate the date, and time value into there own columns.     
    '''
)

code7 = '''def col_convert(field1,field2):
    df[field2] = pd.to_datetime(df[field2])
    df[field1] = df[field2].dt.time
    df[field2] = pd.to_datetime(df[field2]).date
col_convert('Time_Occurred', 'Date_Occurred')
col_convert('Time_Found', 'Date_Found')
'''
st.code(code7, language='python')


def col_convert(field1,field2):
    df[field2] = pd.to_datetime(df[field2])
    df[field1] = df[field2].dt.time
    df[field2] = pd.to_datetime(df[field2]).dt.date
col_convert('Time_Occurred', 'Date_Occurred')
col_convert('Time_Found', 'Date_Found')
st.dataframe(df)

st.markdown(
    '''
    - ***def col_convert(field1,field2)*** is a helper function with two parameters. It allows for a function within a function, and make the code cleaner, and more precise. They can also be used later.
    - ***df[field2] = pd.to_datetime(df[field2])*** converts the fields into datetime fields
    - ***df[field1] = df[field2].dt.time*** creates a new ***time*** field with the time portion of the ***Date_Occurred*** and ***Date_Found*** fields
    - ***df[field2] = pd.to_datetime(df[field2]).dt.date*** removes the time portion from ***Date_Occurred*** and ***Date_Found*** fields
    - ***col_convert('Time_Occurred', 'Date_Occurred')*** and ***col_convert('Time_Found', 'Date_Found')***
    '''
)

st.divider()
st.markdown(
    '''
    #### In the next section, we will go through ***Exploratory Data Analysis***.
'''
)