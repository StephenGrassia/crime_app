import streamlit as st 

st.set_page_config(page_title="Home",
                   layout="wide")

st.write("<h1 style='text-align: center; color: black;'>Virginia Beach Crime Analysis</h1>", unsafe_allow_html=True)
st.write("<h5 style='text-align: center; color: black;'>Created by: Stephen Grassia</h5>", unsafe_allow_html=True)

st.write(
    """
    **The City of Virginia Beach is a mid-size city in southeastern Virginia, with a population of about 450,000.
    Unlike other mid-size to large cities, Virginia Beach is mainly suburban with the only ubran centers being Town Center, and the Oceanfront. As such,
    Virginia Beach has a pretty low crime rate as compared to other mid to large-sized cities. According to [Neighborhood Scout](https://www.neighborhoodscout.com/va/virginia-beach/crime),
    the chances of becoming a victim of violent crime is ***1 in 1,139*** compared to ***1 in 427*** in Virginia. To increase government transparency, the
    Virginia Beach Police Department well organized data relating to police incident reports.**     
    """
)

st.write("<h3 style='text-align: center; color: black;'>About the Author</h3>", unsafe_allow_html=True)
st.write(
    """
    **Stephen is a Geospatial Developing Analyst from New Jersey, currently living in Virginia Beach, Virginia. He graduated from Old Dominion University in 2017
    with a Bachelors of Science in Geography. His background includes healthcare, public health,and data analytics. In his spare time he enjoys bike riding, kickboxing, 
    and visiting local breweries.**
    """
)

