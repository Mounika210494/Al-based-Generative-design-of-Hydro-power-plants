"""
surrogate_train.py - trains XGBoost regressors on the synthetic dataset.
Usage:
python src/surrogate_train.py --data data/synthetic_dataset.csv --out models/
"""
import argparse, os, joblib
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb

def load_data(path):
    return pd.read_csv(path)

def prepare_xy(df):
    X = df[["dam_height","crest_length","penstock_diam","penstock_len","turbines"]]
    y_energy = df["annual_gwh"]
    y_cost = df["cost_musd"]
    y_env = df["env_score"]
    return X, y_energy, y_cost, y_env

def train_and_save(X, y, out_path):
    model = xgb.XGBRegressor(n_estimators=200, max_depth=6, random_state=42, verbosity=0)
    model.fit(X, y)
    joblib.dump(model, out_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default="data/synthetic_dataset.csv")
    parser.add_argument("--out", type=str, default="models/")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    df = load_data(args.data)
    X, y_energy, y_cost, y_env = prepare_xy(df)
    print("Training energy model...")
    train_and_save(X, y_energy, os.path.join(args.out,"energy_model.joblib"))
    print("Training cost model...")
    train_and_save(X, y_cost, os.path.join(args.out,"cost_model.joblib"))
    print("Training env model...")
    train_and_save(X, y_env, os.path.join(args.out,"env_model.joblib"))
    print("Saved models to", args.out)
