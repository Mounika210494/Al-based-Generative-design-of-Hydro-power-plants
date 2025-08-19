"""
power.py - simple hydraulic power calculations
"""
def calc_power_mw(Q, H, eta=0.9):
    rho = 1000.0
    g = 9.81
    return rho * g * Q * H * eta / 1e6

def annual_energy_gwh(P_mw, capacity_factor=0.45):
    return P_mw * 8760 * capacity_factor / 1000.0
