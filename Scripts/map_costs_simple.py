# -*- coding: utf-8 -*-
"""
Standalone version of map_costs.py for Namibia (NA) and weather year 2023
Creates visualizations of hydrogen cost analysis
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def create_cost_maps():
    """Create cost visualization maps"""
    
    print("Starting cost mapping and visualization...")
    
    # Set parameters for Namibia and 2023
    country = "NA"
    weather_year = "2023"
    
    # File paths
    hexagons_path = f'Results/hex_cost_components_{country}_{weather_year}.geojson'
    demand_excel_path = f'Parameters/{country}/demand_parameters.xlsx'
    
    # Load hexagons
    print("Loading hexagons with cost data...")
    hexagons = gpd.read_file(hexagons_path)
    print(f"Loaded {len(hexagons)} hexagons")
    
    # Load demand parameters
    print("Loading demand parameters...")
    demand_parameters = pd.read_excel(demand_excel_path, index_col='Demand center').squeeze("columns")
    demand_centers = demand_parameters.index
    print(f"Found {len(demand_centers)} demand centers: {list(demand_centers)}")
    
    # Create Plots directory
    plots_dir = f'Plots/{country}_{weather_year}'
    os.makedirs(plots_dir, exist_ok=True)
    print(f"Created plots directory: {plots_dir}")
    
    # Create visualizations for each demand center
    for demand_center in demand_centers:
        print(f"Creating maps for demand center: {demand_center}")
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle(f'Hydrogen Cost Analysis - {demand_center}, Namibia ({weather_year})', fontsize=16)
        
        # Flatten axes for easier iteration
        axes = axes.flatten()
        
        # Plot 1: Total LCOH (trucking)
        ax = axes[0]
        if f'{demand_center} trucking LCOH' in hexagons.columns:
            hexagons.plot(column=f'{demand_center} trucking LCOH', 
                         ax=ax, legend=True, cmap='viridis',
                         legend_kwds={'label': 'LCOH (€/kg H2)'})
            ax.set_title(f'{demand_center} - Trucking LCOH')
            ax.axis('off')
        
        # Plot 2: Total LCOH (pipeline)
        ax = axes[1]
        if f'{demand_center} pipeline LCOH' in hexagons.columns:
            hexagons.plot(column=f'{demand_center} pipeline LCOH', 
                         ax=ax, legend=True, cmap='viridis',
                         legend_kwds={'label': 'LCOH (€/kg H2)'})
            ax.set_title(f'{demand_center} - Pipeline LCOH')
            ax.axis('off')
        
        # Plot 3: Wind capacity
        ax = axes[2]
        if f'{demand_center} trucking wind capacity' in hexagons.columns:
            hexagons.plot(column=f'{demand_center} trucking wind capacity', 
                         ax=ax, legend=True, cmap='Blues',
                         legend_kwds={'label': 'Wind Capacity (MW)'})
            ax.set_title(f'{demand_center} - Wind Capacity (Trucking)')
            ax.axis('off')
        
        # Plot 4: Solar capacity
        ax = axes[3]
        if f'{demand_center} trucking solar capacity' in hexagons.columns:
            hexagons.plot(column=f'{demand_center} trucking solar capacity', 
                         ax=ax, legend=True, cmap='Oranges',
                         legend_kwds={'label': 'Solar Capacity (MW)'})
            ax.set_title(f'{demand_center} - Solar Capacity (Trucking)')
            ax.axis('off')
        
        # Plot 5: Electrolyzer capacity
        ax = axes[4]
        if f'{demand_center} trucking electrolyzer capacity' in hexagons.columns:
            hexagons.plot(column=f'{demand_center} trucking electrolyzer capacity', 
                         ax=ax, legend=True, cmap='Reds',
                         legend_kwds={'label': 'Electrolyzer Capacity (MW)'})
            ax.set_title(f'{demand_center} - Electrolyzer Capacity (Trucking)')
            ax.axis('off')
        
        # Plot 6: Cost comparison
        ax = axes[5]
        if (f'{demand_center} trucking LCOH' in hexagons.columns and 
            f'{demand_center} pipeline LCOH' in hexagons.columns):
            
            # Calculate cost difference
            cost_diff = (hexagons[f'{demand_center} trucking LCOH'] - 
                        hexagons[f'{demand_center} pipeline LCOH'])
            
            hexagons.plot(column=cost_diff, 
                         ax=ax, legend=True, cmap='RdBu_r',
                         legend_kwds={'label': 'Cost Difference (Trucking - Pipeline) €/kg H2'})
            ax.set_title(f'{demand_center} - Cost Difference (Trucking vs Pipeline)')
            ax.axis('off')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the plot
        plot_path = f'{plots_dir}/{demand_center}_cost_analysis.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"Saved cost analysis plot to: {plot_path}")
        
        # Close the figure to free memory
        plt.close()
    
    # Create summary statistics
    print("\nCreating summary statistics...")
    summary_data = []
    
    for demand_center in demand_centers:
        for transport_type in ["trucking", "pipeline"]:
            lcoh_col = f'{demand_center} {transport_type} LCOH'
            if lcoh_col in hexagons.columns:
                lcoh_values = hexagons[lcoh_col].dropna()
                if len(lcoh_values) > 0:
                    summary_data.append({
                        'Demand Center': demand_center,
                        'Transport Type': transport_type,
                        'Min LCOH (€/kg H2)': lcoh_values.min(),
                        'Max LCOH (€/kg H2)': lcoh_values.max(),
                        'Mean LCOH (€/kg H2)': lcoh_values.mean(),
                        'Median LCOH (€/kg H2)': lcoh_values.median(),
                        'Std Dev LCOH (€/kg H2)': lcoh_values.std()
                    })
    
    # Create summary DataFrame and save
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_path = f'{plots_dir}/cost_summary.csv'
        summary_df.to_csv(summary_path, index=False)
        print(f"Saved cost summary to: {summary_path}")
        
        # Print summary
        print("\n" + "="*80)
        print("HYDROGEN COST ANALYSIS SUMMARY")
        print("="*80)
        print(summary_df.to_string(index=False))
        print("="*80)
    
    print(f"\n🎉 All cost maps and visualizations completed!")
    print(f"📁 Results saved in: {plots_dir}")
    
    return plots_dir

if __name__ == "__main__":
    create_cost_maps() 