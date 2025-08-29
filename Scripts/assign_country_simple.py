#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplified version of assign_country.py that works without external datasets.
Assigns country-specific parameters to hexagons for Namibia.
"""

import geopandas as gpd
import pandas as pd
import sys
import os

def assign_country_parameters(input_file, output_file):
    """Assign country-specific parameters to hexagons."""
    
    # Read the hexagon file
    hexagons = gpd.read_file(input_file)
    
    # Since we're working with Namibia (NA), assign NA to all hexagons
    hexagons['country'] = 'NA'
    
    # Add country-specific parameters from country_parameters.xlsx
    country_params_path = "Parameters/NA/country_parameters.xlsx"
    
    if os.path.exists(country_params_path):
        country_params = pd.read_excel(country_params_path)
        
        # Extract parameters for Namibia
        namibia_params = country_params[country_params['Country'] == 'Namibia'].iloc[0]
        
        # Add these parameters to all hexagons
        hexagons['solar_interest_rate'] = namibia_params['Solar interest rate']
        hexagons['solar_lifetime'] = namibia_params['Solar lifetime (years)']
        hexagons['wind_interest_rate'] = namibia_params['Wind interest rate']
        hexagons['wind_lifetime'] = namibia_params['Wind lifetime (years)']
        hexagons['plant_interest_rate'] = namibia_params['Plant interest rate']
        hexagons['plant_lifetime'] = namibia_params['Plant lifetime (years)']
        hexagons['infrastructure_interest_rate'] = namibia_params['Infrastructure interest rate']
        hexagons['infrastructure_lifetime'] = namibia_params['Infrastructure lifetime (years)']
        hexagons['electricity_price'] = namibia_params['Electricity price (euros/kWh)']
        hexagons['heat_price'] = namibia_params['Heat price (euros/kWh)']
    else:
        print(f"Warning: {country_params_path} not found. Using default values.")
        # Use default values from the README
        hexagons['solar_interest_rate'] = 0.06
        hexagons['solar_lifetime'] = 20
        hexagons['wind_interest_rate'] = 0.06
        hexagons['wind_lifetime'] = 20
        hexagons['plant_interest_rate'] = 0.06
        hexagons['plant_lifetime'] = 20
        hexagons['infrastructure_interest_rate'] = 0.06
        hexagons['infrastructure_lifetime'] = 50
        hexagons['electricity_price'] = 0.10465
        hexagons['heat_price'] = 0.02
    
    # Save the result
    hexagons.to_file(output_file, driver="GeoJSON")
    print(f"Successfully assigned country parameters to {len(hexagons)} hexagons")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    # Check if running from Snakemake or directly
    if 'snakemake' in globals():
        # Running from Snakemake
        input_file = str(snakemake.input)
        output_file = str(snakemake.output)
    else:
        # Running directly
        input_file = "Data/hex_final_NA.geojson"
        output_file = "Data/hexagons_with_country_NA.geojson"
    
    assign_country_parameters(input_file, output_file) 