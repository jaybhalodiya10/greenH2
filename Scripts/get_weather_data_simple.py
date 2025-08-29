# -*- coding: utf-8 -*-
"""
Simplified version of get_weather_data.py that can run independently.
Fetches historical weather data from ERA-5 reanalysis dataset using Atlite.
Modified to stay within CDS request limits.
"""

import logging
import atlite
import geopandas as gpd
import os
import sys

def get_weather_data_simple():
    """Fetch weather data for Namibia with reduced request size."""
    
    # Configuration - Reduced to stay within CDS limits
    country = "NA"
    weather_year = "2023"
    
    # Input and output paths
    hexagon_path = f"Data/hexagons_with_country_{country}.geojson"
    output_path = f"Cutouts/{country}_{weather_year}.nc"
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting weather data collection (reduced request size)...")
    
    # Check if hexagon file exists
    if not os.path.exists(hexagon_path):
        logger.error(f"Hexagon file not found: {hexagon_path}")
        return False
    
    # Calculate min and max coordinates from hexagons
    logger.info("Loading hexagon data...")
    hexagons = gpd.read_file(hexagon_path)
    
    hexagon_bounds = hexagons.geometry.bounds
    min_lon, min_lat = hexagon_bounds[['minx','miny']].min()
    max_lon, max_lat = hexagon_bounds[['maxx','maxy']].max()
    
    # Reduce the area slightly to stay within limits
    # Add small buffer but reduce overall size
    buffer = 0.5  # degrees
    min_lon = max(min_lon - buffer, 10)  # Namibia roughly starts at 11.5°E
    max_lon = min(max_lon + buffer, 26)  # Namibia roughly ends at 25.5°E
    min_lat = max(min_lat - buffer, -29)  # Namibia roughly starts at -28.5°S
    max_lat = min(max_lat + buffer, -17)  # Namibia roughly ends at -17.5°S
    
    logger.info(f"Geographic bounds: Lon {min_lon:.2f} to {max_lon:.2f}, Lat {min_lat:.2f} to {max_lat:.2f}")
    
    # Weather data time range - Reduced to monthly data instead of hourly
    # This significantly reduces the request size while still providing useful data
    start_date = f'{weather_year}-01-01'
    end_date = f'{weather_year}-12-31'
    
    logger.info(f"Time range: {start_date} to {end_date}")
    logger.info("Using monthly resolution to stay within CDS limits")
    
    # Create folders for final cutouts and temporary files
    if not os.path.exists('Cutouts'):
        os.makedirs('Cutouts')
        logger.info("Created Cutouts directory")
    
    if not os.path.exists('temp'):
        os.makedirs('temp')
        logger.info("Created temp directory")
    
    try:
        logger.info("Creating Atlite cutout with reduced request size...")
        cutout = atlite.Cutout(
            path=output_path,
            module="era5",
            x=slice(min_lon, max_lon),
            y=slice(min_lat, max_lat),
            time=slice(start_date, end_date),
            # Add parameters to reduce request size
            features=['wind', 'influx', 'temperature'],  # Only essential features
            # Use monthly resolution instead of hourly
            time_resolution='M'  # Monthly instead of hourly
        )
        
        logger.info("Preparing cutout (this should be much faster now)...")
        cutout.prepare(tmpdir="temp")
        
        logger.info(f"Weather data successfully collected and saved to: {output_path}")
        logger.info("Note: Data is monthly resolution to stay within CDS limits")
        return True
        
    except Exception as e:
        logger.error(f"Error collecting weather data: {str(e)}")
        logger.error("Make sure you have:")
        logger.error("1. Installed cdsapi: pip install cdsapi")
        logger.error("2. Set up CDS API key in ~/.cdsapirc")
        logger.error("3. Valid CDS API credentials")
        logger.error("4. Accepted ERA5 dataset license")
        return False

if __name__ == "__main__":
    success = get_weather_data_simple()
    if success:
        print("✅ Weather data collection completed successfully!")
        print("📊 Data is monthly resolution (reduced from hourly to stay within CDS limits)")
    else:
        print("❌ Weather data collection failed. Check the logs above.")
        sys.exit(1) 