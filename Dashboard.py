import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import joblib
from matplotlib.colors import to_hex
from streamlit_option_menu import option_menu
df = pd.read_csv('Nepali_Trekking_cleaned.csv')
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
            background-attachment: fixed;
            background-size: cover;
        }
        .centered-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 80vh;
            font-size: 1em;
            color: white;
            font-weight: bold;
        }
        .centered-text {
            font-size: 2em;
            color: white;
        }
        
        .description-text {
            text-align: center;
            font-size: 1em;
            color: black;
        }
        </style>
        <div class="centered-container">
        <div class="centered-text">Welcome to Trekking Recommendation System</div>
        <div class="description-text"><i>Experience the beauty and adventure of trekking in the majestic mountains of Nepal. Join us for an unforgettable journey!</i></div>
        </div>
        """,
        unsafe_allow_html=True
    )
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
    st.title("Recommendation System")
    loaded_model = joblib.load('random_forest_model.pkl')
    label_encoder = joblib.load('label_encoder.pkl')  # Load the LabelEncoder

    # Create a form
    with st.form(key='my_form'):
        cost = st.text_input('Cost', '')
        age = st.number_input('Age', min_value=0, max_value=100)
        Trekking_Group_Size = st.text_input('Trekking Group Size', '')
        fitness_level = st.selectbox('Fitness Level', ['Beginner', 'Intermediate', 'Advanced'])
        time = st.text_input('Time', '')
        altitude = st.text_input('Max Altitude', '')
        submit_button = st.form_submit_button(label='Recommended Trek')

    if submit_button:
        # Input validation
        if not cost or not Trekking_Group_Size or not time or not altitude:
            st.error("Please fill in all the fields.")
        else:
            try:
                # Convert inputs to appropriate types
                cost = float(cost)
                Trekking_Group_Size = float(Trekking_Group_Size)
                time = float(time)
                altitude = float(altitude)

                # Convert fitness level to numeric
                fitness_level_numeric = {'Beginner': 0, 'Intermediate': 1, 'Advanced': 2}[fitness_level]

                # Create a DataFrame with the input values
                input_data = pd.DataFrame({
                    'Cost': [cost],
                    'Age': [age],
                    'Trekking Group Size': [Trekking_Group_Size],
                    'Fitness Level': [fitness_level_numeric],
                    'Time': [time],
                    'Max Altitude': [altitude]
                })

                # Make predictions
                predictions = loaded_model.predict(input_data)
                trek_prediction_encoded = predictions[0][0]
                trip_grade_numeric_prediction = predictions[0][1]

                # Decode the label-encoded trek name
                trek_prediction = label_encoder.inverse_transform([int(trek_prediction_encoded)])[0]

                # Display the predictions
                st.write(f"Trek: {trek_prediction}")
                st.write(f"Trip Grade Numeric: {trip_grade_numeric_prediction}")

            except ValueError:
                st.error("Please enter valid numeric values for Cost, Trekking Group Size, Time, and Max Altitude.")
elif selected == "Visualizations":
    st.title("Visualizations")
    # df = pd.read_csv('Nepali_Trekking_cleaned.csv')

    # Dropdown menu for selecting the topic
    topic = st.selectbox("Select a topic for visualization",
                         ["Cost vs Duration", "Trip Grade Distribution", "Max Altitude Distribution", "Trek and Cost", "Trek and fitness Level"])

    if topic == "Cost vs Duration":
        fig, ax = plt.subplots()
        sns.lineplot(data=df, x="Cost", y="Time", ax=ax)
        ax.set_title("Cost vs Duration of Treks")
        st.pyplot(fig)
        st.markdown(
            """
            <p style="color: black; text-align: justify;">
            <strong>X-axis (Cost)</strong>: Represents the cost of the trek in currency (USD).<br>
            <strong>Y-axis (Time)</strong>: Represents the number of days taken for each trek.<br><br>

            <strong>Trend</strong>:<br>
            - The graph indicates a general increase in time with higher costs up to a certain point. Initially, lower-cost treks correspond to shorter durations, with some variation.<br>
            - As the cost increases beyond 2000, there is a sharp decrease in the trek duration (between 2500 and 3500 cost), which suggests that more expensive treks may be shorter but might include additional features such as helicopter rides or luxury services.<br>
            - There is some fluctuation in the mid-range costs (between 1000-2000), indicating variations in the length of the treks that may not strictly correlate with cost.<br><br>

            The data used for this graph likely stems from trekking offers in the dataset, where each trek package has attributes like cost and time.
            </p>
            """,
            unsafe_allow_html=True
        )
    elif topic == "Trip Grade Distribution":
        fig, ax = plt.subplots()
        palette = sns.color_palette("viridis", as_cmap=False, n_colors=len(df["Trip Grade Numeric"].unique()))
        sns.countplot(data=df, x="Trip Grade Numeric", ax=ax, palette=palette)
        ax.set_title("Distribution of Trip Grades")
        st.pyplot(fig)
        # Define the color palette and trip grade categories
        trip_grade_categories = {
            0: "Easy",
            1: "Light",
            2: "Light+Moderate",
            3: "Moderate",
            4: "Moderate-Hard",
            5: "Strenuous"
        }
        palette = sns.color_palette("viridis", n_colors=len(trip_grade_categories))

        # Display the legend next to the graph
        legend_html = "<div style='display: flex; flex-direction: column;'>"
        for grade, color in zip(trip_grade_categories.values(), palette):
            legend_html += f"<div style='display: flex; align-items: center;'><div style='width: 20px; height: 20px; background-color: {to_hex(color)}; margin-right: 10px;'></div>{grade}</div>"
        legend_html += "</div>"

        st.markdown(legend_html, unsafe_allow_html=True)
        st.markdown(
            """
            <p style="color: black; text-align: justify;">
            <strong>X-axis</strong>: Trip grade categories (ranging from 0 to 5).<br>
            <strong>Y-axis</strong>: Number of trekking packages.<br><br>
            <strong>Grade Distribution Breakdown:</strong><br>
            - <strong>Grade 0 (~20 trips):</strong> Few trips fall into this category, likely representing the easiest or least challenging treks.<br>
            - <strong>Grade 1 (~60 trips):</strong> A moderate number of easier trips are in this category.<br>
            - <strong>Grade 2 (~30 trips):</strong> There’s a dip, with fewer moderate-level trips.<br>
            - <strong>Grade 3 (~80 trips):</strong> Significant rise, suggesting many trips are moderately challenging.<br>
            - <strong>Grade 4 (~140 trips):</strong> The most common category, indicating many treks are challenging or high-quality.<br>
            - <strong>Grade 5 (~50 trips):</strong> Fewer, but still notable, treks are rated the most difficult or highest quality.<br><br>
            <strong>Insights:</strong><br>
            - <strong>Grade 4 Dominates:</strong> Most treks are rated highly, likely challenging or of excellent quality.<br>
            - <strong>Dip at Grade 2:</strong> Fewer trips fall into the moderate category.<br>
            - <strong>Skew Toward Higher Grades:</strong> More trips are rated higher, indicating a preference for challenging or well-regarded treks.
            </p>
            """,
            unsafe_allow_html=True
        )
    elif topic == "Max Altitude Distribution":
        fig = px.histogram(df, x="Max Altitude", nbins=20, title="Distribution of Maximum Altitudes")
        st.plotly_chart(fig)

        # Add detailed description
        st.markdown(
            """
            <p style="color: black; text-align: justify;">
            <strong>X-axis</strong>: Maximum altitude reached (in meters).<br>
            <strong>Y-axis</strong>: Number of trekking packages.<br><br>

            <strong>Key Points</strong>:<br>
            - <strong>5000-6000 meters</strong>: Most treks (over 100) reach altitudes in this range, likely popular routes like Everest or Annapurna.<br>
            - <strong>4000-5000 meters</strong>: A significant number of treks (less than 80) fall here, possibly less challenging routes.<br>
            - <strong>Below 4000 meters</strong>: Fewer treks, indicating lower-altitude routes are less common.<br>
            - <strong>Above 6000 meters</strong>: Very few treks go beyond this altitude, due to the technical challenges.<br><br>

            The majority of treks focus on high-altitude adventures.
            </p>
            """,
            unsafe_allow_html=True
        )
    elif topic == "Trek and Cost":
        fig = px.histogram(df, x="Trek", y="Cost", title="Trek and Cost")
        st.plotly_chart(fig)
        st.markdown(
            """
            <p style="color: black; text-align: justify;">
            The bar chart analyzes the costs of various Nepal trekking routes:<br>
            <strong>X-axis</strong>: Treks.<br>
            <strong>Y-axis</strong>: Cost (up to 3000 units, likely USD).<br>

            <strong>Trend</strong>:<br>
            - **High-cost trek:** The Everest Base Camp Heli Trek stands out, costing around 3000 units.
            - **Lower-cost treks:** The Annapurna Base Camp Short Trek, Ghorepani Poon Hill Trek, and Langtang Valley Trek are among the least expensive.
            - **Moderate range:** Many treks fall between 5,000 to 10,000 units.
            
            Cost variations are due to factors like trek duration, difficulty, altitude, and premium services such as helicopter rides or luxury accommodations.
            </p>
            """,
            unsafe_allow_html=True
        )
    elif topic == "Trek and fitness Level":
        # Define the color mapping for fitness levels
        color_map = {
            'Beginner': 'blue',
            'Intermediate': 'red',
            'Advanced': 'green'
        }

        # Map the numeric fitness levels to their corresponding labels
        fitness_level_labels = {0: 'Beginner', 1: 'Intermediate', 2: 'Advanced'}
        df['Fitness Level Label'] = df['Fitness Level'].map(fitness_level_labels)

        # Create the bar plot with the specified color mapping
        fig = px.bar(df, x="Trek", y="Fitness Level", color="Fitness Level Label",
                     title="Trek and Fitness Level", color_discrete_map=color_map)
        st.plotly_chart(fig)
        st.markdown(
            """
            <p style="color:black; text-align: justify;">
            The graph provides an analysis of trekking routes in Nepal based on the fitness levels required to complete them. 
            <b>Beginner-friendly treks</b>, such as the <b>Everest Base Camp Heli Trek</b>, <b>Annapurna Base Camp Short Trek</b>, and 
            <b>Ghorepani Poon Hill Trek</b>, are represented by <b style="color:green;">green bars</b>. These treks are less physically 
            demanding and involve shorter durations or easier terrain. The green bars, which are lower on the y-axis, suggest that these 
            treks are ideal for people with limited trekking experience or lower fitness levels.
            </p>
            <p style="color:black; text-align: justify;"> On the other hand, <b>intermediate-level treks</b> like the <b>Upper Mustang Trek</b>, <b>Manaslu Circuit Trek</b>, and 
            <b>Mardi Himal Trek</b> are indicated by <b style="color:red;">red bars</b>, which extend higher on the y-axis. These treks 
            require more stamina, endurance, and physical exertion due to challenging terrain, altitude, and longer durations. These routes 
            are suitable for trekkers with an intermediate fitness level who are prepared for more strenuous hikes.
            </p>
             <p style="color:black; text-align: justify;">
            Some treks, such as the <b>Everest Base Camp Trek</b> and <b>Langtang Valley Trek</b>, feature both <b style="color:green;">green</b> 
            and <b style="color:red;">red bars</b>, indicating that they accommodate trekkers of varying fitness levels. These treks offer 
            flexibility, allowing less experienced trekkers to participate while still presenting challenging sections for those seeking a 
            more demanding adventure.
            </p>
            <p style="color:black; text-align: justify;">
            In summary, <b>beginner treks</b> are characterized by their lower difficulty, shorter durations, and less challenging terrain, 
            making them suitable for novice trekkers. <b>Intermediate treks</b>, however, are more demanding and better suited for those with 
            more trekking experience and a higher level of physical fitness.
            </p>
            """, unsafe_allow_html=True
        )

