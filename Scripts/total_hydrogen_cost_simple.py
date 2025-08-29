# -*- coding: utf-8 -*-
"""
Standalone version of total_hydrogen_cost.py for Namibia (NA) and weather year 2023
"""

import geopandas as gpd
import pandas as pd
import numpy as np

def calculate_total_hydrogen_cost():
    """Calculate total hydrogen cost combining all components"""
    
    print("Starting total hydrogen cost calculation...")
    
    # Set parameters for Namibia and 2023
    country = "NA"
    weather_year = "2023"
    
    # File paths
    hexagons_path = f'Resources/hex_lcoh_{country}_{weather_year}.geojson'
    demand_excel_path = f'Parameters/{country}/demand_parameters.xlsx'
    
    # Load hexagons
    print("Loading hexagons with LCOH data...")
    hexagons = gpd.read_file(hexagons_path)
    print(f"Loaded {len(hexagons)} hexagons")
    
    # Load demand parameters
    print("Loading demand parameters...")
    demand_parameters = pd.read_excel(demand_excel_path, index_col='Demand center').squeeze("columns")
    demand_centers = demand_parameters.index
    print(f"Found {len(demand_centers)} demand centers: {list(demand_centers)}")
    
    # Calculate total cost for each hexagon and demand center
    print("Calculating total hydrogen costs...")
    
    for demand_center in demand_centers:
        for transport_type in ["trucking", "pipeline"]:
            # Get LCOH column name
            lcoh_col = f'{demand_center} {transport_type} LCOH'
            
            if lcoh_col in hexagons.columns:
                # Calculate total cost (LCOH * annual demand)
                annual_demand = demand_parameters.loc[demand_center, 'Annual demand [kg/a]']
                total_cost = hexagons[lcoh_col] * annual_demand
                
                # Add total cost column
                hexagons[f'{demand_center} {transport_type} total cost'] = total_cost
                
                print(f"Added total cost for {demand_center} {transport_type}")
            else:
                print(f"Warning: LCOH column {lcoh_col} not found")
    
    # Save results
    output_path = f'Results/hex_total_cost_{country}_{weather_year}.geojson'
    
    # Create Results directory if it doesn't exist
    import os
    os.makedirs('Results', exist_ok=True)
    
    hexagons.to_file(output_path, driver='GeoJSON')
    print(f"Total cost results saved to {output_path}")
    
    # Print summary
    print("\nTotal hydrogen cost calculation complete!")
    print(f"Results saved to {output_path}")
    
    return output_path

if __name__ == "__main__":
    calculate_total_hydrogen_cost() 