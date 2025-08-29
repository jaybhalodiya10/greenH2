import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Polygon
import json

def create_namibia_hexagons():
    """Create a basic hexagon file for Namibia with required attributes."""
    
    # Namibia bounding box (approximate)
    # Namibia is roughly from -17.5 to -28.5 latitude and 11.5 to 25.5 longitude
    lat_min, lat_max = -28.5, -17.5
    lon_min, lon_max = 11.5, 25.5
    
    # Create a simple grid of hexagons (simplified as rectangles for now)
    # In a real implementation, you'd use proper H3 hexagons
    lat_step = 0.5
    lon_step = 0.5
    
    hexagons = []
    
    lat = lat_min
    while lat < lat_max:
        lon = lon_min
        while lon < lon_max:
            # Create a simple polygon (rectangle) for each hexagon
            coords = [
                [lon, lat],
                [lon + lon_step, lat],
                [lon + lon_step, lat + lat_step],
                [lon, lat + lat_step],
                [lon, lat]
            ]
            
            polygon = Polygon(coords)
            
            # Create hexagon data with required attributes
            hex_data = {
                "geometry": polygon,
                "waterbody_dist": np.random.uniform(0, 100),  # Random distance 0-100 km
                "waterway_dist": np.random.uniform(0, 50),    # Random distance 0-50 km
                "ocean_dist": np.random.uniform(0, 200),      # Random distance 0-200 km
                "grid_dist": np.random.uniform(0, 100),       # Random distance 0-100 km
                "road_dist": np.random.uniform(0, 50),        # Random distance 0-50 km
                "theo_pv": np.random.uniform(100, 1000),     # Random PV potential 100-1000 MW
                "theo_wind": np.random.uniform(50, 500),     # Random wind potential 50-500 MW
                "country": "NA"                               # Namibia ISO code
            }
            
            hexagons.append(hex_data)
            lon += lon_step
        lat += lat_step
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(hexagons, crs="EPSG:4326")
    
    # Save to GeoJSON
    output_file = "Data/hex_final_NA.geojson"
    gdf.to_file(output_file, driver="GeoJSON")
    
    print(f"Created {len(hexagons)} hexagons for Namibia")
    print(f"Saved to {output_file}")
    
    return gdf

if __name__ == "__main__":
    create_namibia_hexagons() 