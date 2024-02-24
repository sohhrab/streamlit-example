import streamlit as st
import numpy as np
import plotly.express as px

# ... (likelihood_scale, impact_scale, risk_zones, calculate_risk_score remain the same)

# Define likelihood and impact scales
likelihood_scale = {
    "Very Low": 1,
    "Low": 2,
    "Medium": 3,
    "High": 4,
    "Very High": 5
}

impact_scale = {
    "Insignificant": 1,
    "Minor": 2,
    "Moderate": 3,
    "Major": 4,
    "Severe": 5
}

# Define risk tolerance zones
risk_zones = {
    1: "Green (Low Risk)",
    2: "Green (Low Risk)",
    3: "Green (Low Risk)",
    4: "Green (Low Risk)",
    5: "Green (Low Risk)",
    6: "Green (Low Risk)",
    7: "Green (Low Risk)",
    8: "Green (Low Risk)",
    9: "Yellow (Moderate Risk)",
    10: "Yellow (Moderate Risk)",
    11: "Yellow (Moderate Risk)",
    12: "Yellow (Moderate Risk)",
    13: "Yellow (Moderate Risk)",
    14: "Yellow (Moderate Risk)",
    15: "Yellow (Moderate Risk)",
    16: "Red (High Risk)",
    17: "Red (High Risk)",
    18: "Red (High Risk)",
    19: "Red (High Risk)",
    20: "Red (High Risk)",
    21: "Red (High Risk)",
    22: "Red (High Risk)",
    23: "Red (High Risk)",
    24: "Red (High Risk)",
    25: "Red (High Risk)"
}

def calculate_risk_score(likelihood, impact):
  """
  Calculates the risk score based on likelihood and impact scales.

  Args:
      likelihood (str): The likelihood of the risk event.
      impact (str): The impact of the risk event.

  Returns:
      int: The risk score.
  """
  return likelihood_scale[likelihood] * impact_scale[impact]

def assess_risk(risk_description, likelihood, impact):
  """
  Assesses a risk based on its description, likelihood, and impact.

  Args:
      risk_description (str): The description of the risk.
      likelihood (str): The likelihood of the risk event.
      impact (str): The impact of the risk event.

  Returns:
      dict: A dictionary containing the risk information and assessment.
  """
  risk_score = calculate_risk_score(likelihood, impact)
  risk_zone = risk_zones[risk_score]
  return {
      "risk_description": risk_description,
      "likelihood": likelihood,
      "impact": impact,
      "risk_score": risk_score,
      "risk_zone": risk_zone
  }

def collect_and_assess_risk():
    """
    Collects user input for risk assessment, displays results, and saves to database
    """
    st.title("Risk Assessment")

    risk_description = st.text_input("Enter a brief risk description:")
    likelihood = st.selectbox("Enter likelihood:", options=list(likelihood_scale.keys()))
    impact = st.selectbox("Enter impact:", options=list(impact_scale.keys()))

    if st.button("Assess Risk"):
        result = assess_risk(risk_description, likelihood, impact)

        # Display Results
        st.subheader("Risk Assessment Results")
        for key, value in result.items():
            st.write(f"{key.capitalize()}: {value}")

        # Database Integration (Using SQLite for simplicity)
        try:
            import sqlite3
            conn = sqlite3.connect('risk_assessments.db') 
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO RiskAssessments (RiskDescription, Likelihood, Impact, RiskScore, RiskZone, AssessmentDate) 
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)  
            """, (risk_description, likelihood, impact, result['risk_score'], result['risk_zone']))

            conn.commit()
            conn.close()
            st.success("Risk assessment saved to database!")
        except Exception as e:
            st.error(f"Error saving to database: {e}") 
#df = pd.DataFrame({
#    'Likelihood': list(likelihood_scale.keys()),
#    'Impact': list(impact_scale.keys()),
#    'Risk Score': [calculate_risk_score(l, i) for l in likelihood_scale.keys() for i in impact_scale.keys()]
# }) 

 # Create heatmap
#fig = px.imshow(df, 
#                x = 'Likelihood', 
#                y = 'Impact',
#                color = 'Risk Score',
#                color_continuous_scale='RdYlGn', # Adjust colorscale if desired
#                aspect="auto"
#               )

#st.plotly_chart(fig) 

# Main Streamlit App
if __name__ == "__main__":
    collect_and_assess_risk()
