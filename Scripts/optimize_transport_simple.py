#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplified version of optimize_transport_and_conversion.py that can run independently.
Calculates basic transport costs for hydrogen.
"""

import geopandas as gpd
import numpy as np
import pandas as pd
from functions import CRF, cheapest_trucking_strategy, h2_conversion_stand, cheapest_pipeline_strategy
from shapely.geometry import Point
import os

def optimize_transport_simple():
    """Run transport optimization with hardcoded parameters."""
    
    # Input file paths
    hexagon_path = "Data/hexagons_with_country_NA.geojson"
    technology_parameters = "Parameters/NA/technology_parameters.xlsx"
    demand_parameters = "Parameters/NA/demand_parameters.xlsx"
    country_parameters = "Parameters/NA/country_parameters.xlsx"
    conversion_parameters = "Parameters/NA/conversion_parameters.xlsx"
    transport_parameters = "Parameters/NA/transport_parameters.xlsx"
    pipeline_parameters = "Parameters/NA/pipeline_parameters.xlsx"
    
    # Create Resources folder if it doesn't exist
    if not os.path.exists('Resources'):
        os.makedirs('Resources')
    
    # Load data
    print("Loading data...")
    
    # Load hexagons
    hexagons = gpd.read_file(hexagon_path)
    print(f"Loaded {len(hexagons)} hexagons")
    
    # Load demand centers
    demand_center_list = pd.read_excel(demand_parameters, sheet_name='Demand centers', index_col='Demand center')
    print(f"Loaded {len(demand_center_list)} demand centers")
    
    # Load country parameters
    country_params = pd.read_excel(country_parameters, index_col='Country')
    namibia_params = country_params.loc['Namibia']
    print("Loaded Namibia parameters")
    
    # Load technology parameters
    infra_data = pd.read_excel(technology_parameters, sheet_name='Infra', index_col='Infrastructure')
    global_data = pd.read_excel(technology_parameters, sheet_name='Global', index_col='Parameter').squeeze("columns")
    
    # Get infrastructure costs
    road_capex_long = infra_data.at['Long road', 'CAPEX']
    road_capex_short = infra_data.at['Short road', 'CAPEX']
    road_opex = infra_data.at['Short road', 'OPEX']
    
    print("Starting transport cost calculations...")
    
    # Initialize results
    results = []
    
    # Process each demand center
    for demand_center in demand_center_list.index:
        demand_info = demand_center_list.loc[demand_center]
        demand_location = Point(demand_info['Lon [deg]'], demand_info['Lat [deg]'])
        demand_quantity = demand_info['Annual demand [kg/a]']
        demand_state = demand_info['Demand state']
        
        print(f"Processing demand center: {demand_center}")
        
        # Calculate distances and costs for each hexagon
        for idx, hexagon in hexagons.iterrows():
            hex_center = hexagon.geometry.centroid
            
            # Calculate distance (simplified - using centroid)
            distance = hex_center.distance(demand_location) * 111  # Rough conversion to km
            
            # Basic transport cost calculation (simplified)
            if distance < 10:
                road_cost = road_capex_short * distance
            else:
                road_cost = road_capex_long * distance
            
            # Add annual O&M costs
            road_cost += road_opex * distance
            
            # Simple trucking cost (very simplified)
            trucking_cost = distance * 0.1  # 0.1 €/km/kg as placeholder
            
            # Store results
            result = {
                'hexagon_id': idx,
                'demand_center': demand_center,
                'distance_km': distance,
                'road_construction_cost': road_cost,
                'trucking_cost': trucking_cost,
                'total_transport_cost': road_cost + trucking_cost
            }
            results.append(result)
    
    # Convert to DataFrame
    results_df = pd.DataFrame(results)
    
    # Save results
    output_file = "Resources/hex_transport_NA.geojson"
    
    # Add transport costs to hexagons
    hexagons['avg_transport_cost'] = 0.0
    hexagons['min_distance_to_demand'] = float('inf')
    
    for idx, hexagon in hexagons.iterrows():
        hex_results = results_df[results_df['hexagon_id'] == idx]
        if len(hex_results) > 0:
            hexagons.loc[idx, 'avg_transport_cost'] = hex_results['total_transport_cost'].mean()
            hexagons.loc[idx, 'min_distance_to_demand'] = hex_results['distance_km'].min()
    
    # Save to GeoJSON
    hexagons.to_file(output_file, driver="GeoJSON")
    
    print(f"Transport optimization complete. Results saved to {output_file}")
    print(f"Processed {len(results)} hexagon-demand center combinations")
    
    return hexagons, results_df

if __name__ == "__main__":
    hexagons, results = optimize_transport_simple() 