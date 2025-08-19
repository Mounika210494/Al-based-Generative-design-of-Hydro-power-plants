"""
surrogate_model.py - wrapper to load and query trained surrogate models
"""
import joblib, os
import pandas as pd

class SurrogateModel:
    def __init__(self, model_dir="models"):
        self.energy = joblib.load(os.path.join(model_dir, "energy_model.joblib"))
        self.cost = joblib.load(os.path.join(model_dir, "cost_model.joblib"))
        self.env = joblib.load(os.path.join(model_dir, "env_model.joblib"))

    def predict_df(self, df):
        X = df[["dam_height","crest_length","penstock_diam","penstock_len","turbines"]]
        pred_energy = self.energy.predict(X)
        pred_cost = self.cost.predict(X)
        pred_env = self.env.predict(X)
        out = df.copy()
        out["pred_annual_gwh"] = pred_energy
        out["pred_cost_musd"] = pred_cost
        out["pred_env_score"] = pred_env
        return out
