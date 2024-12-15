import streamlit as st
import requests

# Define the options for year
year_options = [
    1969, 1978, 1979, 1980, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 
    1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 
    2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 
    2014, 2015, 2016
]

# Page title and description
st.title("Car Price Prediction")
st.markdown("<h4 style='text-align: center;'>Fill in the details to predict the car price</h4>", unsafe_allow_html=True)

# Create input fields with dropdowns, number inputs, and text input
brand = st.selectbox("Select the Brand", ["BMW", "Mercedes-Benz", "Audi", "Toyota", "Renault", "Volkswagen", "Mitsubishi"])
body = st.selectbox("Select the Body type", ["sedan", "van", "crossover", "wagon", "other", "hatch"])
mileage = st.number_input("Enter Mileage (in km)", min_value=0.0, step=0.1)
engine_v = st.number_input("Enter Engine Volume (in liters)", min_value=0.0, step=0.1)
engine_type = st.selectbox("Select Engine Type", ["Petrol", "Diesel", "Gas", "Other"])
year = st.selectbox("Select the Year", year_options)
model = st.text_input("Enter the Model")

# Registration options as radio buttons
registration = st.radio("Is the car registered?", ["yes", "no"])

# Submit button
if st.button("Predict"):
    data = {
        "Brand": brand,
        "Body": body,
        "Mileage": mileage,
        "EngineV": engine_v,
        "Engine_Type": engine_type,
        "Registration": registration,
        "Year": year,
        "Model": model
    }

    # Send a POST request to the FastAPI backend for prediction
    response = requests.post("http://127.0.0.1:8000/predict", json=data)

    # Display prediction result
    if response.status_code == 200:
        prediction = response.json()
        st.markdown(f"<h4 style='text-align: center; color: #2d6a4f;'>Predicted Price: **${prediction['prediction']:,.2f}**</h4>", unsafe_allow_html=True)
    else:
        st.error("Error: Unable to get prediction, please try again later.")

# Add some custom style to make the page more appealing
st.markdown("""
    <style>
    body {
        background-color: #f4f4f9;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .stSelectbox>div>div>div {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #e1e1e1;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #e1e1e1;
    }
    .stRadio>div>div {
        border-radius: 8px;
        background-color: #ffffff;
    }
    .stText {
        color: #333333;
    }
    .css-18e3pys {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
