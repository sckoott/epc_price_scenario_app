import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


@st.cache_data
def load_data():
    df = pd.read_csv('master_merged_final.csv', parse_dates=False)
    return df


df = load_data()

coeffs = {
    'EU_cPrice': 0.37549,
    'AcitivityIndex': 0.21220,
    'Oil_Price': -0.13564,
    'NatGas_Price': -0.48151,
    'ER_USCAD': 25.24684,
    'carbon.credit': 0.03298,
    'carbon.price': 0.35388,
    'alberta.carbon': -0.11811
}
intercept = -66.62277

st.title("Alberta EPC Price Forecast App")
st.write("Select a scenario or adjust manually to forecast the EPC price.")

st.sidebar.header("Scenario or Manual Inputs")

scenario = st.sidebar.radio(
    "Choose a Scenario",
    ("Manual Input", "🌍 Climate Acceleration", "🔥 Energy Crisis", "🧊 Climate Fatigue",
     "🌪️ Global Recession Pressure")
)

defaults = {
    'EU_cPrice': 75.0, 'AcitivityIndex': 295.0, 'Oil_Price': 80.0,
    'NatGas_Price': 3.5, 'ER_USCAD': 1.33, 'carbon.credit': 30.0,
    'carbon.price': 30.0, 'alberta.carbon': 20.0
}

scenario_description = ""

if scenario == "🌍 Climate Acceleration":
    defaults.update({
        'EU_cPrice': 110, 'AcitivityIndex': 285, 'Oil_Price': 90,
        'NatGas_Price': 4.5, 'ER_USCAD': 1.32, 'carbon.credit': 50,
        'carbon.price': 60, 'alberta.carbon': 40
    })
    scenario_description = "Tightened EU climate policies, carbon prices surge globally. Alberta faces slight economic slowdown."

elif scenario == "🔥 Energy Crisis":
    defaults.update({
        'EU_cPrice': 90, 'AcitivityIndex': 300, 'Oil_Price': 110,
        'NatGas_Price': 6.0, 'ER_USCAD': 1.28, 'carbon.credit': 40,
        'carbon.price': 45, 'alberta.carbon': 35
    })
    scenario_description = "Oil supply shocks drive up energy prices, strong Alberta economy, moderate carbon market stability."

elif scenario == "🧊 Climate Fatigue":
    defaults.update({
        'EU_cPrice': 75, 'AcitivityIndex': 295, 'Oil_Price': 80,
        'NatGas_Price': 3.5, 'ER_USCAD': 1.33, 'carbon.credit': 30,
        'carbon.price': 30, 'alberta.carbon': 20
    })
    scenario_description = "Weakened global climate commitment, lower carbon pricing attention, stable Alberta economy."

elif scenario == "🌪️ Global Recession Pressure":
    defaults.update({
        'EU_cPrice': 65, 'AcitivityIndex': 275, 'Oil_Price': 70,
        'NatGas_Price': 2.8, 'ER_USCAD': 1.38, 'carbon.credit': 20,
        'carbon.price': 20, 'alberta.carbon': 15
    })
    scenario_description = "Global recession fears reduce energy demand and carbon pricing pressure. Stronger USD weakens CAD."

inputs = {}
for var in defaults:
    inputs[var] = st.sidebar.number_input(var, value=defaults[var])

if scenario != "Manual Input":
    st.info(f"**Scenario Description:** {scenario_description}")

if st.sidebar.button("Predict"):
    forecast = intercept + sum(inputs[var] * coeffs[var] for var in coeffs)
    st.subheader(f"📈 Forecasted EPC Price: **{forecast:.2f} CAD** per ton")

    df['Fitted'] = intercept + sum(df[var] * coeffs[var] for var in coeffs)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['MonthlyPrice'], label='Actual Price', marker='o')
    ax.plot(df.index, df['Fitted'], label='Model Fitted Price', linestyle='--')
    ax.scatter(len(df), forecast, color='red', marker='x', s=100, label='Scenario Forecast')
    ax.set_xlabel("Observation (Months)")
    ax.set_ylabel("EPC Price (CAD)")
    ax.legend()
    st.pyplot(fig)
