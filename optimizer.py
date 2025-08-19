"""
optimizer.py - example NSGA-II run using pymoo
"""
import argparse, os
import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.core.problem import ElementwiseProblem
from src.surrogate_model import SurrogateModel
import pandas as pd

class HydroProblem(ElementwiseProblem):
    def __init__(self, surrogate):
        xl = np.array([10, 50, 1.0, 50.0, 1.0, 0.0])
        xu = np.array([50, 300, 4.0, 400.0, 3.0, 1.0])
        super().__init__(n_var=6, n_obj=3, n_constr=0, xl=xl, xu=xu)
        self.surrogate = surrogate

    def _evaluate(self, x, out, *args, **kwargs):
        dam_height = float(x[0])
        crest = float(x[1])
        pen_d = float(x[2])
        pen_l = float(x[3])
        turbines = int(round(x[4]))
        df = pd.DataFrame([{
            "dam_height": dam_height,
            "crest_length": crest,
            "penstock_diam": pen_d,
            "penstock_len": pen_l,
            "turbines": turbines
        }])
        pred = self.surrogate.predict_df(df).iloc[0]
        f1 = -float(pred["pred_annual_gwh"])
        f2 = float(pred["pred_cost_musd"])
        f3 = float(pred["pred_env_score"])
        out["F"] = [f1, f2, f3]

def run_optimization(model_dir, pop_size=60, n_gen=80, out_csv="results/pareto.csv"):
    os.makedirs("results", exist_ok=True)
    surrogate = SurrogateModel(model_dir)
    problem = HydroProblem(surrogate)
    algorithm = NSGA2(pop_size=pop_size,
                      sampling=get_sampling("real_random"),
                      crossover=get_crossover("real_sbx", prob=0.9, eta=15),
                      mutation=get_mutation("real_pm", eta=20))
    res = minimize(problem, algorithm, ('n_gen', n_gen), verbose=True)
    rows=[]
    for xi, fi in zip(res.X, res.F):
        rows.append({
            "dam_height": float(xi[0]),
            "crest_length": float(xi[1]),
            "penstock_diam": float(xi[2]),
            "penstock_len": float(xi[3]),
            "turbines": int(round(xi[4])),
            "obj_energy_neg": float(fi[0]),
            "obj_cost": float(fi[1]),
            "obj_env": float(fi[2])
        })
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    print("Saved pareto front to", out_csv)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", type=str, default="models")
    parser.add_argument("--pop-size", type=int, default=60)
    parser.add_argument("--generations", type=int, default=80)
    parser.add_argument("--out", type=str, default="results/pareto.csv")
    args = parser.parse_args()
    run_optimization(args.model_dir, args.pop_size, args.generations, args.out)
