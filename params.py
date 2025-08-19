"""
params.py - parameter generation utilities
""" 
import random

def random_design(seed=None):
    if seed is not None:
        random.seed(seed)
    return {
        "dam_height": round(random.uniform(10, 50), 2),
        "crest_length": round(random.uniform(50, 300), 2),
        "penstock_diam": round(random.uniform(1, 4), 2),
        "penstock_len": round(random.uniform(50, 400), 2),
        "turbines": random.choice([1,2,3]),
        "turbine_type": random.choice(["Francis","Kaplan"])
    }
