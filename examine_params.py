import pandas as pd
import os

def examine_parameters():
    """Examine the structure of parameter files."""
    
    # Check country parameters
    country_params_path = "Parameters/NA/country_parameters.xlsx"
    if os.path.exists(country_params_path):
        print("=== Country Parameters ===")
        country_params = pd.read_excel(country_params_path)
        print(f"Shape: {country_params.shape}")
        print(f"Columns: {list(country_params.columns)}")
        print(f"First few rows:")
        print(country_params.head())
        print()
    
    # Check demand parameters
    demand_params_path = "Parameters/NA/demand_parameters.xlsx"
    if os.path.exists(demand_params_path):
        print("=== Demand Parameters ===")
        demand_params = pd.read_excel(demand_params_path)
        print(f"Shape: {demand_params.shape}")
        print(f"Columns: {list(demand_params.columns)}")
        print(f"First few rows:")
        print(demand_params.head())
        print()

if __name__ == "__main__":
    examine_parameters() 