# -*- coding: utf-8 -*-
from enum import Enum, auto
from typing import Dict, Any

import numpy as np


# The Enum is retained as it's the best practice for defining fixed sets of constants.
class OccupancyType(Enum):
    """Defines the building occupancy types for risk factor calculation."""
    RESIDENTIAL_DWELLING = 'Resi. (dwelling)'
    RESIDENTIAL_INSTITUTIONAL = 'Resi. (institutional)'
    RESIDENTIAL_OTHER = 'Resi. (other)'
    OFFICE = 'Office'
    RETAIL = 'Retail'
    ASSEMBLY_HIGH = 'Assembly (high)'
    ASSEMBLY_MED = 'Assembly (med)'
    ASSEMBLY_LOW = 'Assembly (low)'
    INDUSTRIAL_HIGH = 'Industrial (high)'
    INDUSTRIAL_LOW = 'Industrial (low)'


def clause_8_risk_factor(occupancy: OccupancyType, building_height: float) -> float:
    """Helper function to determine the risk factor."""
    h = building_height

    if occupancy in {OccupancyType.RESIDENTIAL_DWELLING, OccupancyType.RESIDENTIAL_OTHER}:
        if h <= 5: return 1.0
        if h <= 18: return 1.35
        if h <= 30: return 2.0
        return 2.65

    if occupancy == OccupancyType.RESIDENTIAL_INSTITUTIONAL:
        if h <= 5: return 1.35
        if h <= 18: return 2.0
        if h <= 30: return 2.65
        return 3.3

    # Default case for Office, Retail, Assembly, and Industrial
    if h <= 5: return 0.65
    if h <= 18: return 1.0
    if h <= 30: return 1.35
    return 2.0


def eq_b_2_ventilation_factor(H: float, A_vv: float, A_vh: float, A_f: float):
    # For large compartments or those with roof openings
    alpha_v = min(max(A_vv / A_f, 0.025), 0.25)
    alpha_h = A_vh / A_f
    b_v = 12.5 * (1 + 10 * alpha_v - alpha_v ** 2)
    if b_v < 10:
        raise ValueError(f"'b_v' should be >= 10, but is {b_v:.2f}")

    w_f = ((6 / H) ** 0.3) * ((0.62 + 90 * (0.4 - alpha_v) ** 4) / (1 + b_v * alpha_h))
    return w_f


def eq_b_3_ventilation_factor(A_f, A_t, O):
    w_f = (1 / np.sqrt(O)) * (A_f / A_t)
    return w_f


def clause_b_1_t_e_d(
        q_f_k: float,
        m: float,
        delta_1: float,
        k_b: float,
        A_f: float,
        A_t: float,
        H: float,
        A_vv: float,
        A_vh: float = 0.0,
) -> Dict[str, Any]:
    """
    Calculates the equivalent time of fire exposure using a functional approach.

    This function takes all necessary parameters and returns a dictionary containing
    the input parameters and all calculated intermediate and final values.

    Args:
        q_f_k (float): Characteristic fire load density [MJ/m^2].
        m (float): Combustion factor [-].
        delta_1 (float): Sprinkler factor [-].
        k_b (float): Conversion factor [min*m^2/MJ].
        A_f (float): Floor area of the compartment [m^2].
        A_t (float): Total internal surface area of the compartment [m^2].
        H (float): Height of the compartment [m].
        A_vv (float): Area of vertical openings [m^2].
        occupancy (OccupancyType): The type of building occupancy.
        building_height (float): The total height of the building [m].
        A_vh (float, optional): Area of horizontal openings (roof) [m^2]. Defaults to 0.0.

    Returns:
        A dictionary with keys for all inputs and calculated results like 't_e_d',
        'q_f_d', 'w_f', 'risk_factor', and 'opening_factor'.
    """
    # 1. Validate inputs
    if not (isinstance(q_f_k, (float, int)) and q_f_k > 0):
        raise ValueError("'q_f_k' must be a numerical value greater than 0.")

    # 2. Calculate design fire load density (q_f_d)
    q_f_d = q_f_k * m * delta_1

    # 3. Calculate opening factor (O)
    O = (A_vv * np.sqrt(H_v)) / A_t

    # 4. Calculate ventilation factor (w_f)
    if A_f >= 100.0 or A_vh > 0.0:
        w_f = eq_b_2_ventilation_factor(H, A_vv, A_vh, A_f)
    else:
        # For small compartments without roof openings
        w_f = eq_b_3_ventilation_factor(A_f, A_t, O)

    # 6. Calculate final equivalent time of exposure (t_e_d)
    t_e_d = q_f_d * k_b * w_f

    # 7. Return all values in a dictionary for easy inspection
    return {
        # Inputs
        "q_f_k": q_f_k, "m": m, "delta_1": delta_1, "k_b": k_b, "A_f": A_f,
        "A_t": A_t, "H": H, "A_vv": A_vv, "A_vh": A_vh,
        # Calculated Results
        "q_f_d": q_f_d,
        "opening_factor": O,
        "w_f": w_f,
        "t_e_d": t_e_d,
    }


### **Example Usage & Self-Contained Test**
def run_functional_test():
    """Runs a test case to validate the functional calculation."""
    print("Running functional validation test...")

    # --- Call the function with the input parameters ---
    results = clause_b_1_t_e_d(
        q_f_k=900.0,
        m=1.0,
        delta_1=0.61,
        k_b=0.09,
        A_f=856.5,
        A_t=980.0,
        H=4.0,
        A_vv=235.2,
        A_vh=0.0,
    )

    # --- Verification ---
    pre_calculated_result = 37.13907
    calculated_result = results['t_e_d']

    # Print results from the dictionary
    print(f"Design Fire Load (q_f_d): {results['q_f_d']:.2f} MJ/m^2")
    print(f"Opening Factor (O): {results['opening_factor']:.4f} m^0.5")
    print(f"Ventilation Factor (w_f): {results['w_f']:.4f}")
    print("-" * 30)
    print(f"Pre-calculated t_e_d: {pre_calculated_result:.4f} min")
    print(f"Calculated t_e_d:     {calculated_result:.4f} min")

    assert np.isclose(pre_calculated_result, calculated_result, atol=1e-4)
    print("\n✅ Test passed successfully!")


if __name__ == "__main__":
    run_functional_test()
