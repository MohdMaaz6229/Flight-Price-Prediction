import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime, timedelta
import time
import requests

# Try importing streamlit_lottie, with fallback
try:
    from streamlit_lottie import st_lottie
    lottie_available = True
except ModuleNotFoundError:
    lottie_available = False
    st.warning("⚠️ 'streamlit-lottie' not installed. Confetti animation will be skipped. Install with: pip install streamlit-lottie")

# -----------------------------
# Set page configuration (MUST be the first Streamlit command)
# -----------------------------
st.set_page_config(page_title="Flight Price Prediction", layout="wide", page_icon="✈️")

# -----------------------------
# Custom CSS for modern, interactive design
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    /* Black background */
    .stApp {
        background: #000000;
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
    }

    /* Main container with animated card effect */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        margin: 1rem;
        animation: slideIn 1s ease-out;
    }

    /* Header styling */
    h1 {
        color: #ffffff;
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
        animation: fadeIn 2s ease-in-out;
    }

    /* Subheader */
    h3 {
        color: #1e3c72;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }

    /* Input fields with interactive effects */
    .stSelectbox, .stDateInput, .stTimeInput {
        background: #f0f4f8;
        border-radius: 10px;
        padding: 0.5rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stSelectbox:hover, .stDateInput:hover, .stTimeInput:hover {
        transform: scale(1.02);
        box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
    }
    .stSelectbox:focus-within, .stDateInput:focus-within, .stTimeInput:focus-within {
        border: 2px solid #4d4d4d;
    }

    /* Button with gradient and pulse animation */
    .stButton>button {
        background: linear-gradient(45deg, #333333, #4d4d4d);
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        border: none;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 12px rgba(255, 255, 255, 0.3);
        animation: pulse 1.5s infinite;
    }

    /* Success message */
    .stSuccess {
        background: #d4edda;
        border-radius: 10px;
        padding: 1rem;
        color: #155724;
        font-family: 'Poppins', sans-serif;
    }

    /* Animations */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideIn {
        0% { opacity: 0; transform: translateX(-50px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 255, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
    }

    /* Sidebar styling */
    .css-1v3fvcr {
        background: #1a1a1a;
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    .css-1v3fvcr h2, .css-1v3fvcr p {
        color: white;
    }

    /* Responsive design */
    @media (max-width: 600px) {
        .main-container {
            margin: 0.5rem;
            padding: 1rem;
        }
        .stButton>button {
            padding: 0.4rem 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Load Lottie animation for success (if available)
# -----------------------------
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_confetti = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_x1gjdldl.json") if lottie_available else None

# -----------------------------
# Load trained model
# -----------------------------
@st.cache_resource
def load_model():
    try:
        return pickle.load(open("flight_rf_model.pkl", "rb"))
    except FileNotFoundError:
        st.error("🚨 Model file 'flight_rf_model.pkl' not found. Please ensure it exists.")
        st.stop()
model = load_model()

# -----------------------------
# Define feature lists (from training data)
# -----------------------------
airlines = ['Air Asia', 'Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
            'Multiple carriers', 'Multiple carriers Premium economy', 'SpiceJet', 'Trujet',
            'Vistara', 'Vistara Premium economy']
sources = ['Banglore', 'Chennai', 'Delhi', 'Kolkata', 'Mumbai']
destinations = ['Banglore', 'Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New Delhi']
stops = ['non-stop', '1 stop', '2 stops', '3 stops', '4 stops']

model_columns = [
    'Total_Stops', 'Date', 'Month', 'Year', 'Arrival_hour', 'Arrival_minute',
    'Departure_hour', 'Departure_minute', 'Duration_hour', 'Duration_minute',
    'Airline_Air Asia', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
    'Airline_Jet Airways', 'Airline_Jet Airways Business', 'Airline_Multiple carriers',
    'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet', 'Airline_Trujet',
    'Airline_Vistara', 'Airline_Vistara Premium economy', 'Source_Banglore',
    'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
    'Destination_Banglore', 'Destination_Cochin', 'Destination_Delhi',
    'Destination_Hyderabad', 'Destination_Kolkata', 'Destination_New Delhi'
]

# -----------------------------
# Sidebar for additional info
# -----------------------------
with st.sidebar:
    st.header("🛫 Flight Price Predictor")
    st.markdown("""
    **Welcome to the Flight Price Prediction App!**
    - Select your flight details to get an estimated ticket price.
    - Powered by an XGBoost model trained on 10,000+ flight records.
    - Data from 2019, covering 6 major Indian cities.
    """)
    st.markdown("**Run Locally**: `streamlit run flight_app.py`")

# -----------------------------
# Streamlit App UI
# -----------------------------
st.title("✈️ Flight Price Prediction")
st.markdown("Plan your trip and predict ticket prices with ease!")

# Main container
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.header("🛠️ Enter Flight Details")

    # Input form
    with st.form("flight_form"):
        st.subheader("Flight Information")
        col1, col2 = st.columns([1, 1])

        with col1:
            airline = st.selectbox("✈️ Airline", airlines, help="Choose the airline for your flight.")
            source = st.selectbox("🏙️ Source City", sources, help="Select the departure city.")
            destination = st.selectbox("🏙️ Destination City", destinations, help="Select the arrival city.")
            journey_date = st.date_input("📅 Journey Date", min_value=datetime.today(), help="Pick your travel date.")

        with col2:
            dep_time = st.time_input("⏰ Departure Time", help="Set the departure time.")
            arrival_time = st.time_input("⏰ Arrival Time", help="Set the arrival time.")
            total_stops = st.selectbox("🛬 Total Stops", stops, help="Number of stops (non-stop = 0).")

        # Centered button
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Predict Price")
        st.markdown("</div>", unsafe_allow_html=True)

    # Process inputs and predict
    if submitted:
        # Validate Source != Destination
        if source == destination:
            st.error("🚨 Source and Destination cities cannot be the same!")
            st.stop()

        # Calculate Duration
        dep_dt = datetime.combine(journey_date, dep_time)
        arr_dt = datetime.combine(journey_date, arrival_time)
        if arr_dt < dep_dt:
            arr_dt += timedelta(days=1)
        duration = arr_dt - dep_dt
        duration_hours = int(duration.total_seconds() // 3600)
        duration_minutes = int((duration.total_seconds() % 3600) // 60)
        st.info(f"🕑 Duration: {duration_hours}h {duration_minutes}m")

        # Map Total_Stops to numerical
        stops_mapping = {'non-stop': 0, '1 stop': 1, '2 stops': 2, '3 stops': 3, '4 stops': 4}
        stops_num = stops_mapping[total_stops]

        # Create input DataFrame
        input_data = pd.DataFrame({
            'Total_Stops': [stops_num],
            'Date': [journey_date.day],
            'Month': [journey_date.month],
            'Year': [2019],  # Fixed to 2019 as in training data
            'Arrival_hour': [arrival_time.hour],
            'Arrival_minute': [arrival_time.minute],
            'Departure_hour': [dep_time.hour],
            'Departure_minute': [dep_time.minute],
            'Duration_hour': [duration_hours],
            'Duration_minute': [duration_minutes],
            'Airline_' + airline: [1],
            'Source_' + source: [1],
            'Destination_' + destination: [1]
        })

        # Initialize input with zeros for all model columns
        input_encoded = pd.DataFrame(0, index=[0], columns=model_columns)
        
        # Update with input values
        for col in input_data.columns:
            if col in model_columns:
                input_encoded[col] = input_data[col]

        # Ensure all one-hot encoded columns are present
        for col in model_columns:
            if col.startswith('Airline_') or col.startswith('Source_') or col.startswith('Destination_'):
                if col in input_data.columns:
                    input_encoded[col] = input_data[col]
                else:
                    input_encoded[col] = 0

        # Validate feature names
        try:
            model_feature_names = model.feature_names_in_
            if not all(col in model_feature_names for col in input_encoded.columns):
                missing_features = [col for col in model_feature_names if col not in input_encoded.columns]
                extra_features = [col for col in input_encoded.columns if col not in model_feature_names]
                st.error(f"🚨 Feature mismatch! Missing features: {missing_features}. Extra features: {extra_features}")
                st.stop()
        except AttributeError:
            st.warning("⚠️ Model does not provide feature_names_in_. Assuming feature order matches.")

        # Debug: Show input data
        with st.expander("🔍 Debug: Input Features"):
            st.write(input_encoded)

        # Prediction with progress bar
        with st.spinner("Analyzing flight data..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)  # Simulate processing
                progress_bar.progress(i + 1)
            try:
                prediction = model.predict(input_encoded)[0]
                st.success(f"💰 Predicted Flight Price: ₹ {int(prediction):,}")
                if lottie_available and lottie_confetti:
                    st_lottie(lottie_confetti, height=150, key="confetti")
            except Exception as e:
                st.error(f"🚨 Prediction failed: {str(e)}")
            finally:
                progress_bar.empty()

    st.markdown('</div>', unsafe_allow_html=True)