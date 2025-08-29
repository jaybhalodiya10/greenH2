#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplified version of water_cost.py that can run independently.
Calculates water costs for hydrogen production in each hexagon.
"""

import geopandas as gpd
import pandas as pd
import numpy as np

def calculate_water_costs():
    """Calculate water costs for hydrogen production."""
    
    # Input file paths
    hexagon_path = "Resources/hex_transport_NA.geojson"
    technology_parameters = "Parameters/NA/technology_parameters.xlsx"
    country_parameters_path = "Parameters/NA/country_parameters.xlsx"
    
    print("Loading data for water cost calculation...")
    
    # Load hexagons
    hexagons = gpd.read_file(hexagon_path)
    print(f"Loaded {len(hexagons)} hexagons")
    
    # Load water parameters
    water_data = pd.read_excel(technology_parameters, sheet_name='Water', index_col='Parameter').squeeze("columns")
    print("Loaded water parameters")
    
    # Load country parameters
    country_parameters = pd.read_excel(country_parameters_path, index_col='Country')
    namibia_params = country_parameters.loc['Namibia']
    print("Loaded Namibia parameters")
    
    # Extract water parameters
    electricity_demand_h2o_treatment = water_data['Freshwater treatment electricity demand (kWh/m3)']
    electricity_demand_h2o_ocean_treatment = water_data['Ocean water treatment electricity demand (kWh/m3)']
    water_transport_costs = water_data['Water transport cost (euros/100 km/m3)']
    water_spec_cost = water_data['Water specific cost (euros/m3)']
    water_demand = water_data['Water demand  (L/kg H2)']
    
    print("Calculating water costs for each hexagon...")
    
    # Initialize arrays for water costs
    h2o_costs_dom_water_bodies = np.empty(len(hexagons))
    h2o_costs_ocean = np.empty(len(hexagons))
    h2o_costs = np.empty(len(hexagons))
    
    # Calculate water costs for each hexagon
    for i in range(len(hexagons)):
        # Freshwater costs (from water bodies or waterways)
        h2o_costs_dom_water_bodies[i] = (
            water_spec_cost 
            + (water_transport_costs/100) * min(hexagons['waterbody_dist'].iloc[i], hexagons['waterway_dist'].iloc[i])
            + electricity_demand_h2o_treatment * namibia_params['Electricity price (euros/kWh)']
        ) * water_demand / 1000
        
        # Ocean water costs
        h2o_costs_ocean[i] = (
            water_spec_cost 
            + (water_transport_costs/100) * hexagons['ocean_dist'].iloc[i]
            + electricity_demand_h2o_ocean_treatment * namibia_params['Electricity price (euros/kWh)']
        ) * water_demand / 1000
        
        # Choose the lowest cost option
        h2o_costs[i] = min(h2o_costs_dom_water_bodies[i], h2o_costs_ocean[i])
    
    # Add water costs to hexagons
    hexagons['Ocean water costs'] = h2o_costs_ocean
    hexagons['Freshwater costs'] = h2o_costs_dom_water_bodies
    hexagons['Lowest water cost'] = h2o_costs
    
    # Save results
    output_file = "Resources/hex_water_NA.geojson"
    hexagons.to_file(output_file, driver='GeoJSON', encoding='utf-8')
    
    print(f"Water cost calculation complete. Results saved to {output_file}")
    print(f"Average water cost: {np.mean(h2o_costs):.4f} €/kg H2")
    
    return hexagons

if __name__ == "__main__":
    hexagons = calculate_water_costs() 