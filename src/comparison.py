import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import kruskal

class CountryComparator:
    def __init__(self):
        self.combined_df = None
        self.results = {}
        self.country_data = {}
    
    def load_and_combine(self, country_data_dict):
        """Load and combine all country data with country labels"""
        country_dfs = []
        self.country_data = {}
        
        for country_name, filepath in country_data_dict.items():
            df = pd.read_csv(filepath)
            df['country'] = country_name
            country_dfs.append(df)
            self.country_data[country_name] = df
        
        self.combined_df = pd.concat(country_dfs, ignore_index=True)
        print(f"✅ Combined {len(country_dfs)} countries with {len(self.combined_df)} total rows")
        return self.combined_df
    
    def generate_boxplots(self, metrics=['GHI', 'DNI', 'DHI']):
        """Generate boxplots for specified metrics"""
        for metric in metrics:
            if metric in self.combined_df.columns:
                plt.figure(figsize=(8, 5))
                self.combined_df.boxplot(column=metric, by='country')
                plt.title(f'Boxplot of {metric} by Country')
                plt.suptitle('')
                plt.show()
    
    def calculate_summary_stats(self, metrics=['GHI', 'DNI', 'DHI']):
        """Calculate summary statistics"""
        summary = (self.combined_df.groupby("country")[metrics]
                  .agg(["mean", "median", "std"]))
        return summary
    
    def statistical_test(self, metric='GHI'):
        """Run Kruskal-Wallis test"""
        countries = self.combined_df['country'].unique()
        metric_data = [self.combined_df[self.combined_df['country'] == country][metric] 
                      for country in countries]
        
        kw_stat, kw_p = kruskal(*metric_data)
        
        print("Kruskal-Wallis Results:")
        print(f"H-statistic: {kw_stat:.4f}")
        print(f"p-value: {kw_p:.6f}")
        
        if kw_p < 0.05:
            print("✅ Statistically significant differences between countries")
        else:
            print("❌ No significant differences between countries")
        
        return kw_stat, kw_p
    
    def plot_ranking(self, metric='GHI'):
        """Plot country ranking by metric"""
        metric_means = self.combined_df.groupby("country")[metric].mean().sort_values(ascending=False)
        
        plt.figure(figsize=(6, 4))
        metric_means.plot(kind='bar', color=['gold', 'green', 'blue'])
        plt.title(f"Average {metric} by Country")
        plt.ylabel(f"{metric} (W/m²)")
        plt.xlabel("Country")
        plt.xticks(rotation=0)
        plt.show()
        
        return metric_means
    
    def generate_bubble_chart(self):
        """Bubble Chart: GHI vs Tamb with RH bubble size"""
        plt.figure(figsize=(10, 6))
        
        for country, df in self.country_data.items():
            if all(col in df.columns for col in ['GHI', 'Tamb', 'RH']):
                plt.scatter(df['Tamb'], df['GHI'], 
                           s=df['RH']/2,  # Bubble size based on RH
                           alpha=0.6, label=country)
        
        plt.xlabel('Temperature (°C)')
        plt.ylabel('GHI (W/m²)')
        plt.title('Bubble Chart: GHI vs Temperature (Bubble size = RH%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def generate_histograms(self):
        """Generate Histograms for GHI and Wind Speed"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # GHI Histogram
        for country, df in self.country_data.items():
            if 'GHI' in df.columns:
                axes[0].hist(df['GHI'].dropna(), alpha=0.7, label=country, bins=30)
        axes[0].set_xlabel('GHI (W/m²)')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('GHI Distribution Histogram')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Wind Speed Histogram
        for country, df in self.country_data.items():
            if 'WS' in df.columns:
                axes[1].hist(df['WS'].dropna(), alpha=0.7, label=country, bins=30)
        axes[1].set_xlabel('Wind Speed (m/s)')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title('Wind Speed Distribution Histogram')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def generate_correlation_heatmaps(self):
        """Generate Correlation Heatmaps for each country"""
        for country, df in self.country_data.items():
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            key_cols = [col for col in ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS', 'BP'] if col in numeric_cols]
            
            if len(key_cols) > 1:
                plt.figure(figsize=(8, 6))
                correlation_matrix = df[key_cols].corr()
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                           square=True, linewidths=0.5)
                plt.title(f'Correlation Heatmap - {country}')
                plt.tight_layout()
                plt.show()
    
    def generate_scatter_plots(self):
        """Generate multiple scatter plots"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # WS vs GHI
        for country, df in self.country_data.items():
            if all(col in df.columns for col in ['WS', 'GHI']):
                axes[0,0].scatter(df['WS'], df['GHI'], alpha=0.6, label=country)
        axes[0,0].set_xlabel('Wind Speed (m/s)')
        axes[0,0].set_ylabel('GHI (W/m²)')
        axes[0,0].set_title('Wind Speed vs GHI')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # RH vs Tamb
        for country, df in self.country_data.items():
            if all(col in df.columns for col in ['RH', 'Tamb']):
                axes[0,1].scatter(df['RH'], df['Tamb'], alpha=0.6, label=country)
        axes[0,1].set_xlabel('Relative Humidity (%)')
        axes[0,1].set_ylabel('Temperature (°C)')
        axes[0,1].set_title('Relative Humidity vs Temperature')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # RH vs GHI
        for country, df in self.country_data.items():
            if all(col in df.columns for col in ['RH', 'GHI']):
                axes[1,0].scatter(df['RH'], df['GHI'], alpha=0.6, label=country)
        axes[1,0].set_xlabel('Relative Humidity (%)')
        axes[1,0].set_ylabel('GHI (W/m²)')
        axes[1,0].set_title('Relative Humidity vs GHI')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # WD vs GHI
        for country, df in self.country_data.items():
            if all(col in df.columns for col in ['WD', 'GHI']):
                axes[1,1].scatter(df['WD'], df['GHI'], alpha=0.6, label=country)
        axes[1,1].set_xlabel('Wind Direction (°)')
        axes[1,1].set_ylabel('GHI (W/m²)')
        axes[1,1].set_title('Wind Direction vs GHI')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def generate_wind_analysis(self):
        """Generate wind rose and wind analysis"""
        if any('WD' in df.columns for df in self.country_data.values()):
            fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw=dict(projection='polar'))
            
            for idx, (country, df) in enumerate(self.country_data.items()):
                if 'WD' in df.columns and 'WS' in df.columns:
                    wind_dir = df['WD'].dropna()
                    wind_speed = df['WS'].dropna()
                    
                    if len(wind_dir) > 0:
                        theta = np.radians(wind_dir)
                        radii = wind_speed
                        
                        axes[idx].scatter(theta, radii, alpha=0.6)
                        axes[idx].set_title(f'Wind Pattern - {country}')
            
            plt.tight_layout()
            plt.show()
        else:
            print("Wind direction data not available for wind rose")