"""
generate_dataset.py - creates a synthetic dataset CSV
Run: python src/generate_dataset.py --n 200 --out data/synthetic_dataset.csv
"""
import argparse, csv, random

def synthetic_row(i):
    dam_height = round(random.uniform(10, 50), 2)
    crest_length = round(random.uniform(50, 300), 2)
    penstock_diam = round(random.uniform(1, 4), 2)
    penstock_len = round(random.uniform(50, 400), 2)
    turbines = random.choice([1,2,3])
    turbine_type = random.choice(["Francis","Kaplan"])
    base_flow = random.uniform(20,200)
    Q = max(10.0, round(base_flow * (0.8 + dam_height/100.0), 2))
    H = round(dam_height * 0.95, 2)
    P = (1000*9.81*Q*H*0.88)/1e6
    annual_gwh = round(P * 8760 * 0.45 / 1000.0, 3)
    cost = round(0.05 * dam_height * crest_length + 0.9 * P, 3)
    inundation = (dam_height * crest_length) / 10000.0
    env_score = round(min(1.0, inundation / 10.0 + random.uniform(-0.05,0.05)), 3)
    return [i, dam_height, crest_length, penstock_diam, penstock_len, turbines, turbine_type, Q, H, round(P,3), annual_gwh, cost, env_score]

def create_csv(n=200, out="data/synthetic_dataset.csv"):
    header = ["id","dam_height","crest_length","penstock_diam","penstock_len","turbines","turbine_type","Q_m3s","gross_head_m","power_mw","annual_gwh","cost_musd","env_score"]
    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(1, n+1):
            writer.writerow(synthetic_row(i))
    print("Wrote", n, "rows to", out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=200)
    parser.add_argument("--out", type=str, default="data/synthetic_dataset.csv")
    args = parser.parse_args()
    create_csv(args.n, args.out)
