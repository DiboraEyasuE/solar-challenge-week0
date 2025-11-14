import pandas as pd
import numpy as np

def load_solar_data(countries):
    """
    Generate sample solar data that simulates reading from local CSVs
    This replaces actual CSV files to maintain Git hygiene
    """
    np.random.seed(42)
    data = []
    
    # Simulate data that would come from country-specific CSV files
    for country in countries:
        # Different countries have different solar characteristics
        country_profiles = {
            'Benin': {'ghi_mean': 500, 'temp_mean': 28},
            'Ghana': {'ghi_mean': 520, 'temp_mean': 29},
            'Nigeria': {'ghi_mean': 480, 'temp_mean': 27},
            'Togo': {'ghi_mean': 510, 'temp_mean': 28.5}
        }
        
        profile = country_profiles.get(country, {'ghi_mean': 500, 'temp_mean': 27})
        
        # Generate sample data points
        for i in range(100):
            data.append({
                'Country': country,
                'Region': f"{country}_Region_{np.random.randint(1, 4)}",
                'GHI': max(0, np.random.normal(profile['ghi_mean'], 100)),
                'DNI': max(0, np.random.normal(profile['ghi_mean'] * 0.8, 80)),
                'DHI': max(0, np.random.normal(profile['ghi_mean'] * 0.2, 30)),
                'Tamb': np.random.normal(profile['temp_mean'], 5),
                'WS': max(0, np.random.normal(3, 1.5)),
                'RH': np.random.normal(60, 15)
            })
    
    return pd.DataFrame(data)

def get_available_countries():
    """Return list of countries that would have CSV files"""
    return ['Benin', 'Ghana', 'Nigeria', 'Togo']