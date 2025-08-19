import random
import matplotlib.pyplot as plt

# Sample dataset for rivers
rivers = [
    {"name": "Ganga", "flow": 1200, "variation": 0.2},
    {"name": "Yamuna", "flow": 800, "variation": 0.25},
    {"name": "Godavari", "flow": 1500, "variation": 0.15}
]

# Turbine specs
turbines = [
    {"type": "Kaplan", "capacity": 50, "efficiency": 0.9},
    {"type": "Francis", "capacity": 75, "efficiency": 0.85},
    {"type": "Pelton", "capacity": 100, "efficiency": 0.8}
]

def generate_design():
    river = random.choice(rivers)
    turbine = random.choice(turbines)
    num_turbines = random.randint(3, 10)
    output = river["flow"] * turbine["efficiency"] * num_turbines
    cost = num_turbines * 1.5  # simplified cost factor
    return {
        "river": river["name"],
        "turbine": turbine["type"],
        "num_turbines": num_turbines,
        "output": output,
        "cost": cost
    }

# Generate multiple designs
designs = [generate_design() for _ in range(10)]

# Select best design by output/cost ratio
best_design = max(designs, key=lambda d: d["output"] / d["cost"])

# Save result
with open("outputs/best_design.txt", "w") as f:
    f.write(str(best_design))

# Output result
print("Best Design:", best_design)

# Visualizing the output
plt.bar([d["turbine"] for d in designs], [d["output"] for d in designs])
plt.xlabel("Turbine Type")
plt.ylabel("Estimated Output (MW)")
plt.title("Hydropower Plant Designs")
plt.savefig("outputs/output_chart.png")
plt.show()
