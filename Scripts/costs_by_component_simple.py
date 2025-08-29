# -*- coding: utf-8 -*-
"""
Standalone version of costs_by_component.py for Namibia (NA) and weather year 2023
"""

import geopandas as gpd
import pandas as pd
import numpy as np

def calculate_cost_components():
    """Calculate cost breakdown by equipment type"""
    
    print("Starting cost component calculation...")
    
    # Set parameters for Namibia and 2023
    country = "NA"
    weather_year = "2023"
    
    # File paths
    hexagons_path = f'Results/hex_total_cost_{country}_{weather_year}.geojson'
    demand_excel_path = f'Parameters/{country}/demand_parameters.xlsx'
    country_excel_path = f'Parameters/{country}/country_parameters.xlsx'
    
    # Load hexagons
    print("Loading hexagons with total cost data...")
    hexagons = gpd.read_file(hexagons_path)
    print(f"Loaded {len(hexagons)} hexagons")
    
    # Load parameters
    print("Loading parameters...")
    demand_parameters = pd.read_excel(demand_excel_path, index_col='Demand center').squeeze("columns")
    country_parameters = pd.read_excel(country_excel_path, index_col='Country')
    demand_centers = demand_parameters.index
    print(f"Found {len(demand_centers)} demand centers: {list(demand_centers)}")
    
    # Calculate cost components for each hexagon and demand center
    print("Calculating cost components...")
    
    for demand_center in demand_centers:
        annual_demand = demand_parameters.loc[demand_center, 'Annual demand [kg/a]']
        
        for transport_type in ["trucking", "pipeline"]:
            # Get capacity columns
            wind_cap_col = f'{demand_center} {transport_type} wind capacity'
            solar_cap_col = f'{demand_center} {transport_type} solar capacity'
            electrolyzer_cap_col = f'{demand_center} {transport_type} electrolyzer capacity'
            battery_cap_col = f'{demand_center} {transport_type} battery capacity'
            h2_storage_col = f'{demand_center} {transport_type} h2 storage'
            
            if all(col in hexagons.columns for col in [wind_cap_col, solar_cap_col, electrolyzer_cap_col]):
                # Calculate annualized costs for each component
                for i, country_code in enumerate(hexagons['country']):
                    try:
                        country_params = country_parameters.loc[country_code]
                        
                        # Wind costs
                        wind_capacity = hexagons.loc[i, wind_cap_col]
                        wind_capex = wind_capacity * country_params['Wind capital cost [€/W]']
                        wind_lifetime = country_params['Wind lifetime [a]']
                        wind_annual_cost = wind_capex / wind_lifetime
                        
                        # Solar costs
                        solar_capacity = hexagons.loc[i, solar_cap_col]
                        solar_capex = solar_capacity * country_params['Solar capital cost [€/W]']
                        solar_lifetime = country_params['Solar lifetime [a]']
                        solar_annual_cost = solar_capex / solar_lifetime
                        
                        # Electrolyzer costs
                        electrolyzer_capacity = hexagons.loc[i, electrolyzer_cap_col]
                        electrolyzer_capex = electrolyzer_capacity * country_params['Electrolyzer capital cost [€/W]']
                        electrolyzer_lifetime = country_params['Electrolyzer lifetime [a]']
                        electrolyzer_annual_cost = electrolyzer_capex / electrolyzer_lifetime
                        
                        # Battery costs
                        battery_capacity = hexagons.loc[i, battery_cap_col]
                        battery_capex = battery_capacity * country_params['Battery capital cost [€/W]']
                        battery_lifetime = country_params['Battery lifetime [a]']
                        battery_annual_cost = battery_capex / battery_lifetime
                        
                        # H2 storage costs
                        h2_storage_capacity = hexagons.loc[i, h2_storage_col]
                        h2_storage_capex = h2_storage_capacity * country_params['H2 storage capital cost [€/Wh]']
                        h2_storage_lifetime = country_params['H2 storage lifetime [a]']
                        h2_storage_annual_cost = h2_storage_capex / h2_storage_lifetime
                        
                        # Store component costs
                        hexagons.loc[i, f'{demand_center} {transport_type} wind cost'] = wind_annual_cost
                        hexagons.loc[i, f'{demand_center} {transport_type} solar cost'] = solar_annual_cost
                        hexagons.loc[i, f'{demand_center} {transport_type} electrolyzer cost'] = electrolyzer_annual_cost
                        hexagons.loc[i, f'{demand_center} {transport_type} battery cost'] = battery_annual_cost
                        hexagons.loc[i, f'{demand_center} {transport_type} h2 storage cost'] = h2_storage_annual_cost
                        
                    except Exception as e:
                        print(f"Error processing hexagon {i}: {e}")
                        continue
                
                print(f"Added cost components for {demand_center} {transport_type}")
            else:
                print(f"Warning: Some capacity columns missing for {demand_center} {transport_type}")
    
    # Save results
    output_geojson = f'Results/hex_cost_components_{country}_{weather_year}.geojson'
    output_csv = f'Results/hex_cost_components_{country}_{weather_year}.csv'
    
    # Create Results directory if it doesn't exist
    import os
    os.makedirs('Results', exist_ok=True)
    
    # Save as GeoJSON
    hexagons.to_file(output_geojson, driver='GeoJSON')
    print(f"Cost component results saved to {output_geojson}")
    
    # Save as CSV (drop geometry column)
    hexagons_csv = hexagons.drop(columns=['geometry'])
    hexagons_csv.to_csv(output_csv, index=False)
    print(f"Cost component results also saved to {output_csv}")
    
    # Print summary
    print("\nCost component calculation complete!")
    print(f"Results saved to {output_geojson} and {output_csv}")
    
    return output_geojson, output_csv

if __name__ == "__main__":
    calculate_cost_components() 