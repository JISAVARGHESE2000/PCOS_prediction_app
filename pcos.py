import streamlit as st
import pickle
import numpy as np
from PIL import Image

# Load model
with open("pcos_model.pkl", "rb") as obj:
    model = pickle.load(obj)

# Session state
if "result" not in st.session_state:
    st.session_state.result = None
if "probability" not in st.session_state:
    st.session_state.probability = None
if "page" not in st.session_state:
    st.session_state.page = 'welcome'

# Threshold
THRESHOLD = 0.4

# Mappings
level_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
yes_no_mapping = {'Yes': 1, 'No': 0}
severity_mapping = {'No Acne': 0, 'Mild': 1, 'Moderate': 2, 'Severe': 3}
bmi_mapping = {'Normal': 1, 'Underweight': 0, 'Overweight': 3, 'Obese': 4}
menstrual_regular_mapping = {'Regular': 1, 'Irregular': 0}
urban_rural_mapping = {'Urban': 1, 'Rural': 0}
ethnicity_mapping = {'Asian': 1, 'Caucasian': 2, 'African':3, 'Hispanic': 4, 'Other' :5}
country_mapping = {
    'Afghanistan': 0, 'Algeria': 1, 'Angola': 2, 'Argentina': 3, 'Australia': 4, 'Bangladesh': 5, 'Benin': 6, 'Brazil': 7,
    'Burkina Faso': 8, 'Burundi': 9, 'Cambodia': 10, 'Cameroon': 11, 'Canada': 12, 'Chad': 13, 'Chile': 14, 'China': 15,
    'Colombia': 16, 'Ecuador': 17, 'Egypt': 18, 'Ethiopia': 19, 'France': 20, 'Germany': 21, 'Ghana': 22, 'Guatemala': 23,
    'Guinea': 24, 'India': 25, 'Indonesia': 26, 'Iran': 27, 'Iraq': 28, 'Italy': 29, 'Ivory Coast': 30, 'Japan': 31,
    'Kazakhstan': 32, 'Kenya': 33, 'Madagascar': 34, 'Malawi': 35, 'Malaysia': 36, 'Mali': 37, 'Mexico': 38, 'Morocco': 39,
    'Mozambique': 40, 'Myanmar': 41, 'Nepal': 42, 'Netherlands': 43, 'Niger': 44, 'Nigeria': 45, 'North Korea': 46,
    'Pakistan': 47, 'Peru': 48, 'Philippines': 49, 'Poland': 50, 'Romania': 51, 'Russia': 52, 'Rwanda': 53,
    'Saudi Arabia': 54, 'Senegal': 55, 'Somalia': 56, 'South Africa': 57, 'South Korea': 58, 'Spain': 59,
    'Sri Lanka': 60, 'Sudan': 61, 'Syria': 62, 'Taiwan': 63, 'Tanzania': 64, 'Thailand': 65, 'Turkey': 66,
    'Uganda': 67, 'Ukraine': 68, 'United Kingdom': 69, 'United States': 70, 'Uzbekistan': 71, 'Venezuela': 72,
    'Vietnam': 73, 'Yemen': 74, 'Zambia': 75, 'Zimbabwe': 76
}

# Predict function
def predict_pcos(features):
    probability = model.predict_proba([features])[0][1]
    prediction = 1 if probability >= THRESHOLD else 0
    return ("🛑 Positive for PCOS", probability) if prediction == 1 else ("✅ Negative for PCOS", probability)

# Health advice
def health_advice(result):
    if "Positive" in result:
        return """**Suggested Lifestyle Changes:**
- Maintain a **balanced diet** rich in fiber and lean proteins  
- Engage in **regular physical activity**  
- **Manage stress** through mindfulness or yoga  
- **Consult a gynecologist** for medical treatment"""
    else:
        return """**Healthy Habits to Follow:**
- Keep a **balanced diet** and stay hydrated  
- **Exercise regularly** and keep your hormones in check  
- Have **regular check-ups** and manage stress levels"""

# Navigation control
def next_page(next_page):
    st.session_state.page = next_page

# Custom CSS
st.markdown("""
    <style>
        body { background-color: #f2f2f2; }
        .stButton > button {
            color: white;
            background-color: #4CAF50;
            padding: 0.5em 1.5em;
            border-radius: 8px;
            font-weight: bold;
        }
        h1, h2, h3, h4 {
            font-family: 'Segoe UI', sans-serif;
        }
        .footer {
            position: fixed;
            bottom: 10px;
            width: 100%;
            text-align: center;
            color: gray;
            font-size: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# Pages
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align:center; color:#FF4081;'>Welcome to the PCOS Prediction App</h1>", unsafe_allow_html=True)
    st.image(r"C:\Users\HP\OneDrive\Pictures\Screenshots\Screenshot 2025-01-31 062001.png", use_column_width=True)
    st.markdown("### Empowering women through early PCOS detection and guidance.")
    st.markdown("#### 💡 *“Health is the greatest gift. Let's protect it together.”*")
    st.button("➡️ Continue", on_click=lambda: next_page('introduction'))

elif st.session_state.page == 'introduction':
    st.title("🌸 Introduction to PCOS Predictor")
    st.markdown("""
    This app is powered by a **Random Forest Classifier** trained on global data from 75 countries  
    with an accuracy of **94%** in predicting PCOS.  
    Simply input your health and lifestyle details to receive a personalized result  
    along with recommendations to stay healthy!
    """)
    st.button("➡️ Proceed to Form", on_click=lambda: next_page('input'))

elif st.session_state.page == 'input':
    st.title("📝 Fill Out the Form")

    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Select Country", list(country_mapping.keys()))
        age = st.number_input("Enter Age", min_value=10, max_value=60, value=25)
        bmi = st.selectbox("BMI Category", list(bmi_mapping.keys()))
        menstrual = st.radio("Menstrual Regularity", ["Regular", "Irregular"])
        hirsutism = st.radio("Hirsutism (Facial Hair)", ["Yes", "No"])
        acne = st.selectbox("Acne Severity", list(severity_mapping.keys()))
        family = st.radio("Family History of PCOS", ["Yes", "No"])
        insulin = st.radio("Insulin Resistance", ["Yes", "No"])

    with col2:
        lifestyle = st.slider("Lifestyle Score", 1, 10, 5)
        stress = st.selectbox("Stress Level", list(level_mapping.keys()))
        location = st.radio("Living Area", ["Urban", "Rural"])
        socioeconomic = st.selectbox("Socioeconomic Status", list(level_mapping.keys()))
        awareness = st.radio("Awareness of PCOS", ["Yes", "No"])
        fertility = st.radio("Fertility Concerns", ["Yes", "No"])
        undiagnosed = st.number_input("Likelihood of Undiagnosed PCOS (0.0 to 1.0)", min_value=0.0, max_value=1.0)
        ethnicity = st.selectbox("Select Ethnicity", list(ethnicity_mapping.keys()))

    user_input = [
        country_mapping[country],
        age,
        bmi_mapping[bmi],
        menstrual_regular_mapping[menstrual],
        yes_no_mapping[hirsutism],
        severity_mapping[acne],
        yes_no_mapping[family],
        yes_no_mapping[insulin],
        lifestyle,
        level_mapping[stress],
        urban_rural_mapping[location],
        level_mapping[socioeconomic],
        yes_no_mapping[awareness],
        yes_no_mapping[fertility],
        undiagnosed,
        ethnicity_mapping[ethnicity]
    ]

    if st.button("🔍 Predict My Risk"):
        result, prob = predict_pcos(user_input)
        st.session_state.result = result
        st.session_state.probability = prob
        next_page('result')

elif st.session_state.page == 'result':
    st.title("📊 Your PCOS Prediction Result")
    if st.session_state.result:
        st.markdown(f"<h2 style='color:#E91E63;'>{st.session_state.result}</h2>", unsafe_allow_html=True)
        st.write(f"### Probability of PCOS: **{st.session_state.probability:.2%}**")
        st.success(health_advice(st.session_state.result))
    else:
        st.warning("No prediction available. Please go back and fill the form.")

    st.button("🔁 Start Over", on_click=lambda: next_page('welcome'))

# Footer
st.markdown("<div class='footer'>Made with ❤️ by JISA VARGHESE | PCOS Awareness Initiative</div>", unsafe_allow_html=True)
