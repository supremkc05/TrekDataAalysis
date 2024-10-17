import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Add custom CSS to fix the sidebar
st.markdown(
    """
    <style>
    .css-1d391kg {
        position: fixed;
        width: 21rem;
    }
    .css-1d391kg .css-1v3fvcr {
        width: 21rem;
    }
    .css-1d391kg .css-1v3fvcr .css-1lcbmhc {
        width: 21rem;
    }
    .css-18e3th9 {
        padding-top: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# as sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        menu_icon="menu-button-wide-fill",
        options=["Home", "Dataset", "Recommendation", "Visualizations"],
        icons=["house", "book", "envelope", "bar-chart-line-fill"],
        default_index=0,
    )

if selected == "Home":
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://i.ibb.co/qnLyTLy/A-breathtaking-short.jpg");
            background-repeat: no-repeat;
            background-attachment: scroll;
            background-size: cover;
        }
        .centered-text {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80vh;
            font-size: 2em;
            color: white;
            font-weight: bold;
        }
        .description-text {
            text-align: center;
            font-size: 1em;
            color: black;
            margin-top: 0px;/* Small gap */
        }
        </style>
        <div class="centered-text"> <i>Welcome to Trekking Recommendation System</i></div>
        <div class="description-text"><i>Experience the beauty and adventure of trekking in the majestic mountains of Nepal. Join us for an unforgettable journey!</i></div>
        """,
        unsafe_allow_html=True
    )
    # st.title("")
elif selected == "Dataset":
    st.title("Dataset Information")
    st.markdown(
        """
        The dataset appears to describe various trekking packages in Nepal with detailed information about the treks, including cost, duration, difficulty, and other specifics. Here's a summary of the columns:
        - **Unnamed: 0**: Index (possibly redundant).
        - **Trek**: Name of the trekking route or package.
        - **Cost**: Cost of the trek in USD.
        - **Time**: Duration of the trek (in days).
        - **Trip Grade**: Difficulty level of the trek.
        - **Max Altitude**: Maximum altitude reached during the trek.
        - **Accommodation**: Type of accommodation provided.
        - **Best Travel Time**: Best time of the year to do the trek.
        - **Date of Travel**: The date when the trek is scheduled.
        - **Sex**: Gender of the trekker.
        - **Regional Code**: Regional identification code.
        - **Country**: Country of origin of the trekker.
        - **Fitness Level**: Required fitness level for the trek.
        - **Weather Conditions**: Weather experienced during the trek.
        - **Trekking Group Size**: Size of the trekking group.
        - **Guide/No Guide**: Whether a guide is provided.
        - **Equipment Used**: Equipment used during the trek.
        - **Purpose of Travel**: Reason for going on the trek (e.g., leisure, charity).
        - **Health Incidents**: Health-related incidents during the trek.
        - **Review/Satisfaction**: Satisfaction rating or review score.

        There are some missing or incomplete values in certain columns, but the dataset is overall rich in information.
        """
    )
elif selected == "Recommendation":
    st.title(f"You have selected {selected}")
elif selected == "Visualizations":
    st.title(f"You have selected {selected}")

df = pd.read_csv('Nepali_Trekking_cleaned.csv')