import streamlit as st
import pandas as pd
import numpy as np
import pickle

# -------------------------------
# Page config
# -------------------------------

st.set_page_config(
    page_title="Water Quality Risk Prediction",
    layout="wide"
)

st.title("💧 Water Quality Risk Prediction System")

# -------------------------------
# Load model and dataset
# -------------------------------

model = pickle.load(open("water_quality_model.pkl", "rb"))
df = pd.read_csv("featured_dataset.csv")

# -------------------------------
# Sidebar mode selection
# -------------------------------

mode = st.sidebar.radio(
    "Select Input Mode",
    ["Manual Input", "Dataset Selection"]
)

# ====================================
# MANUAL INPUT
# ====================================

if mode == "Manual Input":

    st.header("Enter Water Parameters")

    col1, col2 = st.columns(2)

    with col1:
        Temperature = st.number_input(
            "Temperature (°C)",
            value=20.0
        )

        DO = st.number_input(
            "Dissolved Oxygen",
            value=8.0
        )

        pH = st.number_input(
            "pH",
            value=7.0
        )

    with col2:
        Conductivity = st.number_input(
            "Conductivity",
            value=100.0
        )

        BOD = st.number_input(
            "BOD",
            value=1.0
        )

        Nitrate = st.number_input(
            "Nitrate",
            value=0.5
        )


# ====================================
# DATASET INPUT
# ====================================

else:

    st.header("Select From Dataset")

    states = sorted(df["State"].dropna().unique())

    selected_state = st.selectbox(
        "Select State",
        states
    )
    
    state_df = df[
        df["State"] == selected_state
    ]

    locations = sorted(
        state_df["Location"].dropna().unique()
    )

    selected_location = st.selectbox(
        "Select Water Body / Location",
        locations
    )

    row = state_df[
        state_df["Location"] ==
        selected_location
    ].iloc[0]

    st.subheader("Water Body Details")

    st.write(
        f"**State:** {selected_state}"
    )

    st.write(
        f"**Location:** {selected_location}"
    )

    Temperature = row["Temperature"]
    DO = row["DO"]
    pH = row["pH"]
    Conductivity = row["Conductivity"]
    BOD = row["BOD"]
    Nitrate = row["Nitrate"]

# ====================================
# Prediction Button
# ====================================

if st.button("Predict Water Quality"):

    # -------------------------------
    # Feature Engineering
    # -------------------------------

    bod_do_ratio = round(
        BOD/(DO+0.01),2
    )

    temp_do_interaction = round(
        Temperature*DO,2
    )

    input_data = pd.DataFrame([[
        Temperature,
        DO,
        pH,
        Conductivity,
        BOD,
        Nitrate,
        bod_do_ratio,
        temp_do_interaction
    ]],

    columns=[
        "Temperature",
        "DO",
        "pH",
        "Conductivity",
        "BOD",
        "Nitrate",
        "BOD_DO_Ratio",
        "Temp_DO_Interaction"
    ])

    prediction = model.predict(
        input_data
    )[0]

    # -------------------------------
    # Rule Based Classification
    # -------------------------------

    if (
        BOD >= 30 or
        DO <= 2 or
        Conductivity >= 1200 or
        Nitrate >= 20
    ):
        prediction = "Hazardous"
        wqri = 95

    elif (
        BOD >= 12 or
        DO <= 4 or
        Conductivity >= 700 or
        Nitrate >= 10 or
        pH >= 8.5
    ):
        prediction = "Risky"
        wqri = 75

    elif (
        BOD >= 5 or
        DO <= 6 or
        Conductivity >= 350 or
        Nitrate >= 4
    ):
        prediction = "Moderate"
        wqri = 50

    else:
        prediction = "Safe"
        wqri = 20

    # -------------------------------
    # Prediction Result
    # -------------------------------

    st.subheader("Prediction Result")

    if prediction == "Safe":
        st.success("✅ Water Status : SAFE")

    elif prediction == "Moderate":
        st.warning("⚠ Water Status : MODERATE")

    elif prediction == "Risky":
        st.warning("🚨 Water Status : RISKY")

    else:
        st.error("☠ Water Status : HAZARDOUS")

    # -------------------------------
    # WQRI
    # -------------------------------

    st.subheader(
        "Water Quality Risk Index"
    )

    st.progress(
        wqri / 100
    )

    st.write(
        f"WQRI : {wqri}%"
    )

    # -------------------------------
    # Water Usage & Treatment
    # -------------------------------

    st.subheader(
        "Water Usage & Treatment Recommendation"
    )

    if prediction == "Safe":

        st.success("Current Usage")
        st.write("✅ Drinking Water")
        st.write("✅ Domestic Use")
        st.write("✅ Agriculture")
        st.write("✅ Industrial Use")
        st.write("✅ Aquatic Life Support")

        st.info("Treatment Recommendation")
        st.write("• Basic filtration")
        st.write("• Regular monitoring")

        st.success("Usage After Treatment")
        st.write("✅ Safe for all purposes")

    elif prediction == "Moderate":

        st.warning(
            "Current Usage Before Treatment"
        )

        st.write("⚠ Agriculture")
        st.write("⚠ Washing / Cleaning")
        st.write("⚠ Limited Industrial Use")
        st.write("❌ Not recommended for drinking")

        st.info(
            "Treatment Recommendation"
        )

        st.write("• Sand filtration")
        st.write("• Activated carbon treatment")
        st.write("• Chlorination")
        st.write("• Biological treatment")

        st.success(
            "Usage After Treatment"
        )

        st.write("✅ Domestic use")
        st.write("✅ Agriculture")
        st.write("✅ Drinking after purification")

    elif prediction == "Risky":

        st.error(
            "Current Usage Before Treatment"
        )

        st.write("⚠ Limited Industrial Use")
        st.write("❌ Avoid drinking")
        st.write("❌ Avoid domestic use")
        st.write("❌ Avoid agriculture")

        st.info(
            "Treatment Recommendation"
        )

        st.write("• Reverse Osmosis (RO)")
        st.write("• Chemical treatment")
        st.write("• Biological treatment")
        st.write("• UV disinfection")

        st.success(
            "Usage After Treatment"
        )

        st.write("✅ Agriculture")
        st.write("✅ Industrial use")
        st.write("✅ Domestic use after treatment")

    else:

        st.error(
            "Current Usage Before Treatment"
        )

        st.write("❌ Unsafe for drinking")
        st.write("❌ Unsafe for domestic use")
        st.write("❌ Unsafe for agriculture")
        st.write("❌ Not suitable for direct use")

        st.info(
            "Treatment Recommendation"
        )

        st.write("• Multi-stage filtration")
        st.write("• Reverse Osmosis (RO)")
        st.write("• Chemical purification")
        st.write("• UV treatment")
        st.write("• Wastewater treatment processing")

        st.success(
            "Usage After Treatment"
        )

        st.write("✅ Industrial use")
        st.write("✅ Agriculture")
        st.write("✅ Drinking after complete purification")

    # -------------------------------
    # Generated Features
    # -------------------------------

    st.subheader(
        "Generated Features"
    )

    st.write(
        f"BOD/DO Ratio: {bod_do_ratio}"
    )

    st.write(
        f"Temp_DO_Interaction: {temp_do_interaction}"
    )

    # -------------------------------
    # Input Summary
    # -------------------------------

    st.subheader(
        "Input Summary"
    )

    result = pd.DataFrame({

        "Parameter": [
            "Temperature",
            "DO",
            "pH",
            "Conductivity",
            "BOD",
            "Nitrate"
        ],

        "Value": [
            Temperature,
            DO,
            pH,
            Conductivity,
            BOD,
            Nitrate
        ]

    })

    st.table(result)