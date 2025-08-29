#!/usr/bin/env python3
"""
Script to help set up CDS API configuration for GeoH2.
This will create the necessary configuration file for accessing ERA5 weather data.
"""

import os
import sys

def setup_cds_api():
    """Set up CDS API configuration."""
    
    print("🌤️  Setting up CDS API for GeoH2 Weather Data Access")
    print("=" * 60)
    
    # Check if cdsapi is installed
    try:
        import cdsapi
        print("✅ cdsapi package is already installed")
    except ImportError:
        print("❌ cdsapi package not found. Installing...")
        os.system("pip install cdsapi")
        try:
            import cdsapi
            print("✅ cdsapi package installed successfully")
        except ImportError:
            print("❌ Failed to install cdsapi. Please install manually: pip install cdsapi")
            return False
    
    # Determine the configuration file path
    if os.name == 'nt':  # Windows
        config_dir = os.path.expanduser("~")
        config_file = os.path.join(config_dir, ".cdsapirc")
    else:  # Unix/Linux/Mac
        config_dir = os.path.expanduser("~")
        config_file = os.path.join(config_dir, ".cdsapirc")
    
    print(f"\n📁 Configuration file will be created at: {config_file}")
    
    # Check if config file already exists
    if os.path.exists(config_file):
        print(f"⚠️  Configuration file already exists at: {config_file}")
        overwrite = input("Do you want to overwrite it? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("Keeping existing configuration file.")
            return True
    
    print("\n🔑 Please provide your CDS API credentials:")
    print("(You can find these at: https://cds.climate.copernicus.eu/api-how-to)")
    print()
    
    # Get API credentials
    url = input("CDS API URL (default: https://cds.climate.copernicus.eu/api): ").strip()
    if not url:
        url = "https://cds.climate.copernicus.eu/api"
    
    key = input("CDS API Key: ").strip()
    
    if not key:
        print("❌ API Key is required!")
        return False
    
    # Create configuration content
    config_content = f"""# CDS API Configuration
# Created by GeoH2 setup script
# 
# To get your API key, visit: https://cds.climate.copernicus.eu/api-how-to
# Make sure you're registered for CDS-Beta access

url: {url}
key: {key}
"""
    
    try:
        # Create the configuration file
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        print(f"\n✅ CDS API configuration file created successfully!")
        print(f"📁 Location: {config_file}")
        print("\n🔒 Security note: Keep your API key secure and don't share it.")
        
        # Test the configuration
        print("\n🧪 Testing CDS API connection...")
        try:
            import cdsapi
            c = cdsapi.Client()
            print("✅ CDS API connection test successful!")
            print("🎉 You're ready to collect weather data!")
        except Exception as e:
            print(f"⚠️  Connection test failed: {str(e)}")
            print("This might be normal if you haven't activated your account yet.")
            print("Please check your email for activation instructions.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating configuration file: {str(e)}")
        return False

def main():
    """Main function."""
    print("GeoH2 CDS API Setup")
    print("This script will help you configure access to ERA5 weather data.")
    print()
    
    success = setup_cds_api()
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Make sure your CDS account is activated")
        print("2. Run: python Scripts/get_weather_data_simple.py")
        print("3. Or continue with Snakemake workflow")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 