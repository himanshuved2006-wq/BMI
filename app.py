import streamlit as st
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="HealthNexus AI", page_icon="🧪", layout="wide")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>streamlit run app.py
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 HealthNexus: Advanced Biometric Analyzer")
st.write("Professional-grade BMI, IBW, and Caloric expenditure analysis.")

# --- SIDEBAR: ADVANCED INPUTS ---
with st.sidebar:
    st.header("🧬 Configuration")
    unit_system = st.radio("Unit System", ("Metric (kg/cm)", "Imperial (lbs/in)"))
    gender = st.selectbox("Biological Gender", ["Male", "Female"])
    activity_level = st.select_slider("Activity Level", 
                                     options=["Sedentary", "Light", "Moderate", "Active", "Athlete"])

    if unit_system == "Metric (kg/cm)":
        weight = st.number_input("Weight (kg)", 1.0, 300.0, 75.0)
        height = st.number_input("Height (cm)", 50.0, 250.0, 175.0)
        height_m = height / 100
    else:
        weight_lbs = st.number_input("Weight (lbs)", 1.0, 700.0, 165.0)
        height_in = st.number_input("Height (inches)", 20.0, 100.0, 70.0)
        weight = weight_lbs * 0.453592
        height_m = height_in * 0.0254

# --- CORE CALCULATIONS ---
bmi = round(weight / (height_m ** 2), 2)

# Robinson Formula for Ideal Body Weight (IBW)
base_height_in = (height_m * 39.37) - 60
if gender == "Male":
    ibw = 52 + (1.9 * base_height_in)
else:
    ibw = 49 + (1.7 * base_height_in)

# --- DASHBOARD LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Analysis Gauge")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        gauge={'axis': {'range': [None, 40]},
               'bar': {'color': "#ffffff"},
               'steps': [
                   {'range': [0, 18.5], 'color': "#3b82f6"},
                   {'range': [18.5, 25], 'color': "#10b981"},
                   {'range': [25, 30], 'color': "#f59e0b"},
                   {'range': [30, 40], 'color': "#ef4444"}]},
        title={'text': "Current BMI"}))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Health Metrics")
    m1, m2 = st.columns(2)
    m1.metric("Ideal Weight", f"{round(ibw, 1)} kg")
    m2.metric("BMI Category", "Normal" if 18.5 <= bmi <= 25 else "Attention Req.")
    
    st.write("---")
    st.info(f"**Target:** To reach a 'Normal' BMI of 22, your target weight is **{round(22 * (height_m**2), 1)} kg**.")
    
    # Simple Weight History Simulation for LinkedIn Demo
    st.write("**Recent Trend**")
    st.line_chart([bmi+1.2, bmi+0.8, bmi+0.5, bmi])

# --- DOWNLOAD REPORT ---
st.download_button("Export Health Report (CSV)", data=f"Metric,Value\nBMI,{bmi}\nIBW,{ibw}", file_name="health_report.csv")
# --- CALORIE & BMR CALCULATION ---
st.write("---")
st.subheader("🔥 Energy Expenditure & Nutrition")

# Get age for BMR calculation
with st.sidebar:
    age = st.number_input("Age", min_value=1, max_value=120, value=25)

# BMR Calculation (Mifflin-St Jeor)
if gender == "Male":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

# Activity Multipliers
multipliers = {
    "Sedentary": 1.2,
    "Light": 1.375,
    "Moderate": 1.55,
    "Active": 1.725,
    "Athlete": 1.9
}
tdee = bmr * multipliers[activity_level]

# Displaying Results in Expandable Sections
col_a, col_b = st.columns(2)

with col_a:
    st.metric("BMR (Basal Metabolic Rate)", f"{int(bmr)} kcal")
    st.caption("Calories burned if you did nothing all day.")

with col_b:
    st.metric("TDEE (Daily Maintenance)", f"{int(tdee)} kcal")
    st.caption("Calories needed to maintain current weight.")

# Nutritional Breakdown for LinkedIn Visuals
st.write("#### 🥗 Daily Macronutrient Suggestion (Maintenance)")
p, c, f = st.columns(3)
p.info(f"**Protein:** {int((tdee*0.3)/4)}g")
c.info(f"**Carbs:** {int((tdee*0.4)/4)}g")
f.info(f"**Fats:** {int((tdee*0.3)/9)}g")