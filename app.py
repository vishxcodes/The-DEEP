import streamlit as st
import joblib
import numpy as np

# Load the trained model
model = joblib.load("water_quality_model.pkl")

# Custom Styling
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(to right, #00c6ff, #0072ff);
            color: white;
        }
        .main-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 0px 20px rgba(0,0,0,0.2);
            text-align: center;
            margin-top: 20px;
        }
        .stButton>button {
            background-color: #0072ff;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 10px;
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 style='text-align: center;'>🌊 Water Quality Prediction App</h1>", unsafe_allow_html=True)

# Sidebar UI
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/615/615075.png", width=100)
st.sidebar.header("Enter Water Quality Parameters")

# User inputs
temp = st.sidebar.number_input("🌡 Temperature (°C)", min_value=-10.0, max_value=50.0, step=0.1)
do = st.sidebar.number_input("💧 Dissolved Oxygen (mg/l)", min_value=0.0, max_value=15.0, step=0.1)
ph = st.sidebar.number_input("⚗️ PH Level", min_value=0.0, max_value=14.0, step=0.1)
conductivity = st.sidebar.number_input("🔌 Conductivity (µmhos/cm)", min_value=0.0, step=10.0)
nitrate = st.sidebar.number_input("🧪 Nitrate + Nitrite (mg/l)", min_value=0.0, step=0.1)
fecal_coliform = st.sidebar.number_input("🦠 Fecal Coliform (MPN/100ml)", min_value=0, step=1)
total_coliform = st.sidebar.number_input("🦠 Total Coliform (MPN/100ml)", min_value=0, step=1)

# Main Card UI
st.markdown("<div class='main-card'>", unsafe_allow_html=True)

# Prediction
if st.button("🚀 Predict Water Quality"):
    input_data = np.array([[temp, do, ph, conductivity, nitrate, fecal_coliform, total_coliform]])
    predicted_bod = model.predict(input_data)[0]  # Predict BOD

    # Classification
    if predicted_bod < 1:
        water_quality = "✅ Clean Water - Minimal Organic Pollution"
        color = "green"
    elif 1 <= predicted_bod < 3:
        water_quality = "⚠️ Fairly Clean Water - Low Organic Pollution"
        color = "blue"
    elif 3 <= predicted_bod < 5:
        water_quality = "⚠️ Moderately Polluted Water"
        color = "orange"
    elif 5 <= predicted_bod < 30:
        water_quality = "🚨 Heavily Polluted Water"
        color = "red"
    else:
        water_quality = "💀 Extremely Polluted - Likely Contaminated with Sewage/Industrial Waste!"
        color = "darkred"

    # Display Results
    st.success(f"🚰 Predicted BOD Level: **{predicted_bod:.2f} mg/L**")
    st.markdown(f"<h3 style='color: {color};'>{water_quality}</h3>", unsafe_allow_html=True)
    st.progress(min(predicted_bod / 30, 1.0))  # Animated progress bar

st.markdown("</div>", unsafe_allow_html=True)