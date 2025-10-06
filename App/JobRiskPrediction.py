import streamlit as st
import pandas as pd
import joblib
import json
import seaborn as sns
import matplotlib.pyplot as plt


from streamlit_option_menu import option_menu



df = pd.read_csv('cleaned_data (1).csv')  #
df = df.fillna("None")


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)



page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"]{
    background-image: url("https://images.adsttc.com/media/images/5b1e/dc66/f197/cc77/1d00/000d/large_jpg/ADNOCHQ-092_Credit_Mohammed_Al_Janabi.jpg?1528749145");
    background-size: cover;
    }
    
    [data-testid="stExpander"]{
    background-color: #ffffff;
    }
    [data-testid="stSidebar"]{
    background-color: #51749b;
    }
    [data-testid="stHeader"]{
    background-color: #51749b;
    }
    </style>
    """


st.markdown(page_bg_img, unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Explore", "Job Characteristics", "Predict"],
        icons=["house", "card-list" , "ui-checks", "check2-square"],
    )


if selected == "Home":
    st.title("Job Automation Risk Prediction")

    st.write("Welcome Job Automation Risk Prediction!")
    st.write("To explore the job data, click Explore"+" in the navigation bar on the left.")
    st.write("To predict a job's automation risk, navigate to "+"Job Characteristics.")



if selected == "Explore":
    st.title("Explore The Data")

    st.write("Welcome to the exploration tab!")
    st.write("Explore the data of the dataset. This can help you identify specific value that contributes to your job's Risk Rating.")
    st.write("To view the distribution of each unique value in a specific attribute by risk level, choose an attribute below:")


    higher_level_category = st.selectbox("Select an attribute:",
                                         ['Technological Skill', 'Activity', 'Work Context', 'Skill', 'Knowledge', 'Ability',
                                          'Interest', 'Work Values', 'Work Style', 'Industry'])

    category_mapping = {
        'Technological Skill': ['Tech_Skill_1', 'Tech_Skill_2', 'Tech_Skill_3', 'Tech_Skill_4', 'Tech_Skill_5'],
        'Activity': ['Activity_1', 'Activity_2', 'Activity_3', 'Activity_4', 'Activity_5'],
        'Work Context': ['Work_Context_1', 'Work_Context_2', 'Work_Context_3', 'Work_Context_4', 'Work_Context_5'],
        'Skill': ['Skill_1', 'Skill_2', 'Skill_3', 'Skill_4', 'Skill_5'],
        'Knowledge': ['Knowledge_1', 'Knowledge_2', 'Knowledge_3', 'Knowledge_4', 'Knowledge_5'],
        'Ability': ['Ability_1', 'Ability_2', 'Ability_3', 'Ability_4', 'Ability_5'],
        'Interest': ['Interest_1', 'Interest_2', 'Interest_3'],
        'Work Values': ['Work_Values_1', 'Work_Values_2', 'Work_Values_3'],
        'Work Style': ['Work_Style_1', 'Work_Style_2', 'Work_Style_3', 'Work_Style_4', 'Work_Style_5'],
        'Industry': ['Industry']
    }

    selected_columns = category_mapping.get(higher_level_category, [])

    if selected_columns:
        unique_value_counts = {}

        for column in selected_columns:
            grouped = df.groupby([column, df['Risk'].str.lower()]).size().reset_index(name='Count')
            for index, row in grouped.iterrows():
                unique_value = row[column]
                risk = row['Risk']
                count = row['Count']
                if unique_value not in unique_value_counts:
                    unique_value_counts[unique_value] = {'high': 0, 'low': 0, 'medium': 0}
                unique_value_counts[unique_value][risk] += count

        unique_value_df = pd.DataFrame.from_dict(unique_value_counts, orient='index')

        unique_value_df['Total'] = unique_value_df.sum(axis=1)

        # Bar Plot
        fig, ax = plt.subplots(figsize=(10, 60))
        unique_value_df.sort_values('Total', ascending=True, inplace=True)
        unique_value_df.drop('Total', axis=1, inplace=True)
        unique_value_df.plot(kind='barh', colormap='Set2', ax=ax)
        plt.xlabel('Count')
        plt.ylabel(higher_level_category)
        plt.title(f'Distribution of {higher_level_category} by Risk')
        plt.legend(title='Risk', loc='upper right')
        st.pyplot(fig)


selected_items = {}


if selected == "Job Characteristics":
    st.title("What are your job's characteristics?")
    st.write("pick the characteristics of a chosen job, then navigate to "+" Predict "+"to see it's predicted automation risk level")
    column_messages = {
        'Tech_Skill_1': "What are the main technological skills required for this job?",
        'Tech_Skill_2': "",
        'Tech_Skill_3': "List secondary technological skills required for this job:",
        'Tech_Skill_4': "",
        'Tech_Skill_5': "Additional technological skills that may be relevant:",

        'Activity_1': "What are the main activities of this job?",
        'Activity_2': "",
        'Activity_3': "List secondary activities that may be in this job:",
        'Activity_4': "",
        'Activity_5': "Additional activities that may be relevant:",

        'Work_Context_1': "What are the work context for this job?",
        'Work_Context_2': "",
        'Work_Context_3': "List secondary work contexts that may exist in this job:",
        'Work_Context_4': "",
        'Work_Context_5': "Additional work contexts that may be relevant:",

        'Skill_1': "What are the main skills required for this job?",
        'Skill_2': "",
        'Skill_3': "List secondary skills required for this job:",
        'Skill_4': "",
        'Skill_5': "Additional skills that may be relevant:",

        'Knowledge_1': "What are the main knowledge areas required for this job?",
        'Knowledge_2': "",
        'Knowledge_3': "List secondary knowledge areas required for this job:",
        'Knowledge_4': "",
        'Knowledge_5': "Additional knowledge areas that may be relevant:",

        'Ability_1': "What are the main abilities required for this job?",
        'Ability_2': "",
        'Ability_3': "List secondary abilities required for this job:",
        'Ability_4': "",
        'Ability_5': "Additional abilities that may be relevant:",

        'Interest_1': "What are the main interests required for this job?",
        'Interest_2': "",
        'Interest_3': "Any additional interest?",

        'Work_Values_1': "What are the main work values required for this job?",
        'Work_Values_2': "",
        'Work_Values_3': "List secondary work values required for this job.",


        'Work_Style_1': "What are the main work styles that this job has?",
        'Work_Style_2': "",
        'Work_Style_3': "List secondary work styles of this job:",
        'Work_Style_4': "",
        'Work_Style_5': "Any additional work styles?",

        'Education': "What are the required education level for this job?",
        'Industry': "What type of industry is this job in?"
    }


    with st.expander("####  Technical Skills"):
        columns_Tech = [
            'Tech_Skill_1', 'Tech_Skill_2', 'Tech_Skill_3', 'Tech_Skill_4', 'Tech_Skill_5',
        ]

        for column in columns_Tech:
            unique_values = df[column].unique()
            message = column_messages.get(column, f"Select an item for {column}:")
            selected_items[column] = st.selectbox(message, unique_values)


    with st.expander("####  Activities"):
        columns_Activity = [
            'Activity_1', 'Activity_2', 'Activity_3', 'Activity_4', 'Activity_5',
        ]

        for column in columns_Activity:
            unique_values = df[column].unique()
            message = column_messages.get(column, f"Select an item for {column}:")
            selected_items[column] = st.selectbox(message, unique_values)


    with st.expander("####  Work Context"):
        columns_Context = [
            'Work_Context_1', 'Work_Context_2', 'Work_Context_3', 'Work_Context_4', 'Work_Context_5',
        ]

        for column in columns_Context:
            unique_values = df[column].unique()
            message = column_messages.get(column, f"Select an item for {column}:")
            selected_items[column] = st.selectbox(message, unique_values)


    with st.expander("#### Skills"):
        columns_Skill = [
            'Skill_1', 'Skill_2', 'Skill_3', 'Skill_4', 'Skill_5',
        ]

        for column in columns_Skill:
            unique_values = df[column].unique()
            message = column_messages.get(column, f"Select an item for {column}:")
            selected_items[column] = st.selectbox(message, unique_values)


    with st.expander("####  Knowledge"):
        columns_Knowledge = [
            'Knowledge_1', 'Knowledge_2', 'Knowledge_3', 'Knowledge_4', 'Knowledge_5',
        ]

        for column in columns_Knowledge:
            unique_values = df[column].unique()
            message = column_messages.get(column, f"Select an item for {column}:")
            selected_items[column] = st.selectbox(message, unique_values)


    with st.expander("#### Abilities"):
        columns_Ability = [
            'Ability_1', 'Ability_2', 'Ability_3', 'Ability_4', 'Ability_5',
        ]

        for column in columns_Ability:
            unique_values = df[column].unique()
            message = column_messages.get(column, f"Select an item for {column}:")
            selected_items[column] = st.selectbox(message, unique_values)


    with st.expander("#### Interests"):
        columns_Interest = [
            'Interest_1', 'Interest_2', 'Interest_3',
        ]

        for column in columns_Interest:
            unique_values = df[column].unique()
            message = column_messages.get(column, f"Select an item for {column}:")
            selected_items[column] = st.selectbox(message, unique_values)


    with st.expander("#### Work Values"):
        columns_Values = [
            'Work_Values_1', 'Work_Values_2', 'Work_Values_3',
        ]

        for column in columns_Values:
            unique_values = df[column].unique()
            message = column_messages.get(column, f"Select an item for {column}:")
            selected_items[column] = st.selectbox(message, unique_values)


    with st.expander("#### Work Styles"):
        columns_Style = [
            'Work_Style_1', 'Work_Style_2', 'Work_Style_3', 'Work_Style_4', 'Work_Style_5',
        ]

        for column in columns_Style:
            unique_values = df[column].unique()
            message = column_messages.get(column, f"Select an item for {column}:")
            selected_items[column] = st.selectbox(message, unique_values)


    with st.expander("#### Miscellaneous and Salary"):
        min_salary = df['Salary_Monthly'].min()
        max_salary = df['Salary_Monthly'].max()
        selected_salary = st.slider("Select a salary:", min_salary, max_salary, min_salary)
        st.markdown(f"Salary: ${selected_salary}", unsafe_allow_html=True)


        columns_Misc = [
            'Education', 'Industry'
        ]

        for column in columns_Misc:
            unique_values = df[column].unique()
            message = column_messages.get(column, f"Select an item for {column}:")
            selected_items[column] = st.selectbox(message, unique_values)



        Salary_Annual = selected_salary
        Salary_Month = Salary_Annual / 2

        Tech_Skill_1 = selected_items['Tech_Skill_1']
        Tech_Skill_2 = selected_items['Tech_Skill_2']
        Tech_Skill_3 = selected_items['Tech_Skill_3']
        Tech_Skill_4 = selected_items['Tech_Skill_4']
        Tech_Skill_5 = selected_items['Tech_Skill_5']

        Activity_1 = selected_items['Activity_1']
        Activity_2 = selected_items['Activity_2']
        Activity_3 = selected_items['Activity_3']
        Activity_4 = selected_items['Activity_4']
        Activity_5 = selected_items['Activity_5']

        Work_Context_1 = selected_items['Work_Context_1']
        Work_Context_2 = selected_items['Work_Context_2']
        Work_Context_3 = selected_items['Work_Context_3']
        Work_Context_4 = selected_items['Work_Context_4']
        Work_Context_5 = selected_items['Work_Context_5']

        Skill_1 = selected_items['Skill_1']
        Skill_2 = selected_items['Skill_2']
        Skill_3 = selected_items['Skill_3']
        Skill_4 = selected_items['Skill_4']
        Skill_5 = selected_items['Skill_5']

        Knowledge_1 = selected_items['Knowledge_1']
        Knowledge_2 = selected_items['Knowledge_2']
        Knowledge_3 = selected_items['Knowledge_3']
        Knowledge_4 = selected_items['Knowledge_4']
        Knowledge_5 = selected_items['Knowledge_5']

        Education = selected_items['Education']

        Ability_1 = selected_items['Ability_1']
        Ability_2 = selected_items['Ability_2']
        Ability_3 = selected_items['Ability_3']
        Ability_4 = selected_items['Ability_4']
        Ability_5 = selected_items['Ability_5']

        Interest_1 = selected_items['Interest_1']
        Interest_2 = selected_items['Interest_2']
        Interest_3 = selected_items['Interest_3']

        Work_Values_1 = selected_items['Work_Values_1']
        Work_Values_2 = selected_items['Work_Values_2']
        Work_Values_3 = selected_items['Work_Values_3']

        Work_Style_1 = selected_items['Work_Style_1']
        Work_Style_2 = selected_items['Work_Style_2']
        Work_Style_3 = selected_items['Work_Style_3']
        Work_Style_4 = selected_items['Work_Style_4']
        Work_Style_5 = selected_items['Work_Style_5']

        Industry = selected_items['Industry']


        # Load the mappings from Json file
        def load_mappings():
            with open('categorical_mappings.json', 'r') as json_file:
                mappings = json.load(json_file)
            return mappings


        mappings = load_mappings()

        # Pass the values to the model

        input_data = pd.DataFrame({
            'Salary_Monthly': [selected_salary / 2],
            'Tech_Skill_1_encoded': [mappings['Tech_Skill_1'][Tech_Skill_1]],
            'Tech_Skill_2_encoded': [mappings['Tech_Skill_2'][Tech_Skill_2]],
            'Tech_Skill_3_encoded': [mappings['Tech_Skill_3'][Tech_Skill_3]],
            'Tech_Skill_4_encoded': [mappings['Tech_Skill_4'][Tech_Skill_4]],
            'Tech_Skill_5_encoded': [mappings['Tech_Skill_5'][Tech_Skill_5]],
            'Activity_1_encoded': [mappings['Activity_1'][Activity_1]],
            'Activity_2_encoded': [mappings['Activity_2'][Activity_2]],
            'Activity_3_encoded': [mappings['Activity_3'][Activity_3]],
            'Activity_4_encoded': [mappings['Activity_4'][Activity_4]],
            'Activity_5_encoded': [mappings['Activity_5'][Activity_5]],
            'Work_Context_1_encoded': [mappings['Work_Context_1'][Work_Context_1]],
            'Work_Context_2_encoded': [mappings['Work_Context_2'][Work_Context_2]],
            'Work_Context_3_encoded': [mappings['Work_Context_3'][Work_Context_3]],
            'Work_Context_4_encoded': [mappings['Work_Context_4'][Work_Context_4]],
            'Work_Context_5_encoded': [mappings['Work_Context_5'][Work_Context_5]],
            'Skill_1_encoded': [mappings['Skill_1'][Skill_1]],
            'Skill_2_encoded': [mappings['Skill_2'][Skill_2]],
            'Skill_3_encoded': [mappings['Skill_3'][Skill_3]],
            'Skill_4_encoded': [mappings['Skill_4'][Skill_4]],
            'Skill_5_encoded': [mappings['Skill_5'][Skill_5]],
            'Knowledge_1_encoded': [mappings['Knowledge_1'][Knowledge_1]],
            'Knowledge_2_encoded': [mappings['Knowledge_2'][Knowledge_2]],
            'Knowledge_3_encoded': [mappings['Knowledge_3'][Knowledge_3]],
            'Knowledge_4_encoded': [mappings['Knowledge_4'][Knowledge_4]],
            'Knowledge_5_encoded': [mappings['Knowledge_5'][Knowledge_5]],
            'Education_encoded': [mappings['Education'][Education]],
            'Ability_1_encoded': [mappings['Ability_1'][Ability_1]],
            'Ability_2_encoded': [mappings['Ability_2'][Ability_2]],
            'Ability_3_encoded': [mappings['Ability_3'][Ability_3]],
            'Ability_4_encoded': [mappings['Ability_4'][Ability_4]],
            'Ability_5_encoded': [mappings['Ability_5'][Ability_5]],
            'Interest_1_encoded': [mappings['Interest_1'][Interest_1]],
            'Interest_2_encoded': [mappings['Interest_2'][Interest_2]],
            'Interest_3_encoded': [mappings['Interest_3'][Interest_3]],
            'Work_Values_1_encoded': [mappings['Work_Values_1'][Work_Values_1]],
            'Work_Values_2_encoded': [mappings['Work_Values_2'][Work_Values_2]],
            'Work_Values_3_encoded': [mappings['Work_Values_3'][Work_Values_3]],
            'Work_Style_1_encoded': [mappings['Work_Style_1'][Work_Style_1]],
            'Work_Style_2_encoded': [mappings['Work_Style_2'][Work_Style_2]],
            'Work_Style_3_encoded': [mappings['Work_Style_3'][Work_Style_3]],
            'Work_Style_4_encoded': [mappings['Work_Style_4'][Work_Style_4]],
            'Work_Style_5_encoded': [mappings['Work_Style_5'][Work_Style_5]],
            'Industry_encoded': [mappings['Industry'][Industry]],
            # Include other columns that the model was trained on
        })

    model = joblib.load('Model.pkl')
    predictions = model.predict(input_data)

    st.session_state.prediction_result = predictions
    prediction_result = st.session_state.prediction_result



if selected == "Predict":

    st.title("Predict Your Job's automation risk")
    st.write("Click the Predict button to see the prediction result")
    prediction_result = st.session_state.prediction_result
    #st.write(prediction_result)
    if st.button("Predict"):
        # Make predictions using the loaded mode

        # Create a dictionary to map numeric predictions to text values
        risk_mapping = {0: 'High', 1: 'Low', 2: 'Moderate'}

        # Map the numeric prediction to its text value
        predicted_risk = risk_mapping[prediction_result[0]] # Assuming predictions is an array with a single prediction

        # Create a pop-up for the prediction result
        if predicted_risk == 'Low':
            popup_color = 'green'
            popup_message = "Congratulations! Your job is predicted to have a low automation risk level."
            risk_level = "This means that the automation risk for this job is less than 35%."
        elif predicted_risk == 'Moderate':
            popup_color = 'orange'
            popup_message = "Your job has a moderate chance of being at risk from automation."
            risk_level = "This means that the automation risk for this job is more than 35% but lower than 70%."
        else:
            popup_color = 'red'
            popup_message = "Unfortunately, your job has a high automation risk."
            risk_level = "This means that the automation risk for this job is over 70%."

        st.write(f"Your job's predicted risk category is:")
        st.markdown(
            f"<div style='background-color: {popup_color}; padding: 10px; border-radius: 5px; color: white;'>{predicted_risk}</div>",
            unsafe_allow_html=True
        )
        st.write(popup_message)
        st.write(risk_level)
        st.write("You may explore which job characteristic has contributed to your risk level using the Explore option")