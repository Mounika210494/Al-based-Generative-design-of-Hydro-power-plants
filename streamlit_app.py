"""
streamlit_app.py - demo app
Run: streamlit run src/streamlit_app.py
"""
import streamlit as st
import pandas as pd
from src.surrogate_model import SurrogateModel

st.title("AI Generative Hydro — Demo")

dam = st.slider("Dam height (m)", 10.0, 50.0, 30.0)
crest = st.slider("Crest length (m)", 50.0, 300.0, 150.0)
pdia = st.slider("Penstock diameter (m)", 1.0, 4.0, 2.5)
plen = st.slider("Penstock length (m)", 50.0, 400.0, 200.0)
turb = st.selectbox("Turbine count", [1,2,3])

if st.button("Predict"):
    try:
        m = SurrogateModel("models")
        df = pd.DataFrame([{"dam_height":dam,"crest_length":crest,"penstock_diam":pdia,"penstock_len":plen,"turbines":turb}])
        pred = m.predict_df(df).iloc[0]
        st.write("Predicted annual energy (GWh):", round(pred["pred_annual_gwh"],3))
        st.write("Predicted cost (M USD):", round(pred["pred_cost_musd"],3))
        st.write("Predicted env score (0-1):", round(pred["pred_env_score"],3))
    except Exception as e:
        st.error("Model not available. Train surrogate models first with `python src/surrogate_train.py`")
