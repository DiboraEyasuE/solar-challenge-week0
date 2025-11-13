import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy import stats
import seaborn as sns


class SolarDataEDA:
    def __init__(self, filepath):
        """Initialise with the dataset's filepath"""
        self.filepath = filepath
        self.df = None
        self.key_columns = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
    
    def load_data(self):
        """Load dataset from CSV and preprocess it"""
        if not os.path.exists(self.filepath):
            print(print(f"❌ File not found: {self.filepath}"))
            return
        
        self.df = pd.read_csv(self.filepath, parse_dates = ['Timestamp'], index_col='Timestamp')
        self.df.sort_index(inplace=True)    # Ensure the data is sorted by date
        print("✅ Data loaded successfully!")
        print(self.df.head())

    
    def clean_outliers(self, df):
        """Removes highly null columns and outliers for a proper data visualization"""
        self.df = df
        outliers = pd.Series(False, index=self.df.index)
        self.missing_data = self.df.isna().sum()
        self.total_rows = len(self.df)
        self.missing_percentage = (self.missing_data / self.total_rows) * 100
        self.columns_to_drop = self.missing_percentage[self.missing_percentage > 5].index

        # remove columns with above 5% null values and store it in a new datframe
        self.df = self.df.drop(columns=self.columns_to_drop) 
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.df = self.df.fillna(self.df[self.numeric_cols].median())

        # detect outliers with z_score
        available_key_cols = [col for col in self.key_columns if col in self.df.columns]
        if available_key_cols:
            outlier_flags = np.abs(stats.zscore(self.df[available_key_cols]))
            outliers = outliers | (outlier_flags > 3)
            self.df['Outliers'] = outliers
        print("✅ Data cleaning completed!")
        return self.df


    def export_cleaned(self, df):
        """ Export cleaned dataset to CSV """
        self.df = df
        self.df.to_csv('../data/benin_clean.csv', index=False)

    def time_series_analysis(self, df):
        """ Visualize solar radiation patterns over time for the indicator columns """
        plt.figure(figsize=(15, 10))
        
        plt.subplot(2, 2, 1)
        plt.plot(self.df.index, self.df['GHI'], color='orange', alpha=0.7)
        plt.title('☀️ GHI Over Time')
        plt.ylabel('GHI (W/m²)')
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, 2)
        plt.plot(self.df.index, self.df['DNI'], color='red', alpha=0.7)
        plt.title('🔴 DNI Over Time')
        plt.ylabel('DNI (W/m²)')
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, 3)
        plt.plot(self.df.index, self.df['DHI'], color='blue', alpha=0.7)
        plt.title('🔵 DHI Over Time')
        plt.ylabel('DHI (W/m²)')
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, 4)
        plt.plot(self.df.index, self.df['Tamb'], color='green', alpha=0.7)
        plt.title('🌡️ Temperature Over Time')
        plt.ylabel('Temperature (°C)')
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()


    def daily_solar_patterns(self):
        """Analyze daily patterns of solar radiation."""
        self.df['Hour'] = self.df.index.hour
        daily_patterns = self.df.groupby('Hour')[['GHI', 'DNI', 'DHI']].mean()

        plt.figure(figsize=(12, 6))
        plt.plot(daily_patterns.index, daily_patterns['GHI'], label='GHI', marker='o', linewidth=2)
        plt.plot(daily_patterns.index, daily_patterns['DNI'], label='DNI', marker='s', linewidth=2)
        plt.plot(daily_patterns.index, daily_patterns['DHI'], label='DHI', marker='^', linewidth=2)
        plt.title('📊 Average Daily Solar Radiation Patterns')
        plt.xlabel('Hour of Day')
        plt.ylabel('Radiation (W/m²)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()


    def correlation_analysis(self):
        """Create correlation heatmap for key variables."""
        plt.figure(figsize=(10, 8))
        correlation_matrix = self.df[self.key_columns].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5)
        plt.title('🔥 Correlation Heatmap - Solar Measurements')
        plt.tight_layout()
        plt.show()

    def distribution_analysis(self):
        """Show distribution of key measurements using boxplots."""
        plt.figure(figsize=(12, 6))
        self.df[self.key_columns].boxplot()
        plt.title('📦 Distribution of Solar & Wind Measurements')
        plt.ylabel('Measurement Values')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.show()

    def outlier_analysis(self):
        """Analyze and visualize outliers in the dataset."""
        outlier_summary = self.df['Has_Outlier'].value_counts()
        
        plt.figure(figsize=(8, 6))
        outlier_summary.plot(kind='bar', color=['green', 'red'])
        plt.title('🎯 Outlier Distribution in Dataset')
        plt.xlabel('Has Outlier')
        plt.ylabel('Number of Rows')
        plt.xticks(rotation=0)
        plt.show()
        
        print(f"📊 Outlier Summary: {outlier_summary[True]} rows with outliers")

    def cleaning_impact_analysis(self):
        """Analyze impact of cleaning events on sensor readings."""
        if 'Cleaning' in self.df.columns:
            cleaning_impact = self.df.groupby('Cleaning')[['ModA', 'ModB']].mean()
            plt.figure(figsize=(10, 6))
            cleaning_impact.plot(kind='bar')
            plt.title('🧹 Impact of Cleaning Events on Sensor Readings')
            plt.xlabel('Cleaning Event (0=No, 1=Yes)')
            plt.ylabel('Average Sensor Reading (W/m²)')
            plt.legend(['ModA', 'ModB'])
            plt.grid(True, alpha=0.3)
            plt.show()


        def get_summary(self):
            """Return key statistics for comparison"""
            if self.df is not None:
                return {
                    'mean_GHI': self.df['GHI'].mean(),
                    'median_GHI': self.df['GHI'].median(),
                    'std_GHI': self.df['GHI'].std(),
                    'max_GHI': self.df['GHI'].max()
                }
            return {}
        

        def generate_bubble_chart(self):
            """Bubble Chart: GHI vs Tamb with RH bubble size"""
            if all(col in self.df.columns for col in ['GHI', 'Tamb', 'RH']):
                plt.figure(figsize=(10, 6))
                plt.scatter(self.df['Tamb'], self.df['GHI'], 
                        s=self.df['RH']/2, alpha=0.6, color='blue')
                plt.xlabel('Temperature (°C)')
                plt.ylabel('GHI (W/m²)')
                plt.title('Bubble Chart: GHI vs Temperature (Bubble size = RH%)')
                plt.grid(True, alpha=0.3)
                plt.show()
            else:
                print("❌ Required columns (GHI, Tamb, RH) not available for bubble chart")

    def generate_histograms(self):
        """Generate Histograms for GHI and Wind Speed"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # GHI Histogram
        if 'GHI' in self.df.columns:
            axes[0].hist(self.df['GHI'].dropna(), alpha=0.7, bins=30, color='orange')
            axes[0].set_xlabel('GHI (W/m²)')
            axes[0].set_ylabel('Frequency')
            axes[0].set_title('GHI Distribution Histogram')
            axes[0].grid(True, alpha=0.3)
        
        # Wind Speed Histogram
        if 'WS' in self.df.columns:
            axes[1].hist(self.df['WS'].dropna(), alpha=0.7, bins=30, color='green')
            axes[1].set_xlabel('Wind Speed (m/s)')
            axes[1].set_ylabel('Frequency')
            axes[1].set_title('Wind Speed Distribution Histogram')
            axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

    def generate_correlation_heatmap(self):
        """Generate Correlation Heatmap"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        key_cols = [col for col in ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS', 'BP'] if col in numeric_cols]
        
        if len(key_cols) > 1:
            plt.figure(figsize=(8, 6))
            correlation_matrix = self.df[key_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                    square=True, linewidths=0.5)
            plt.title('Correlation Heatmap - Solar Measurements')
            plt.tight_layout()
            plt.show()
        else:
            print("❌ Not enough numeric columns for correlation heatmap")

    def generate_scatter_plots(self):
        """Generate multiple scatter plots"""
        plots_created = 0
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # WS vs GHI
        if all(col in self.df.columns for col in ['WS', 'GHI']):
            axes[0,0].scatter(self.df['WS'], self.df['GHI'], alpha=0.6, color='red')
            axes[0,0].set_xlabel('Wind Speed (m/s)')
            axes[0,0].set_ylabel('GHI (W/m²)')
            axes[0,0].set_title('Wind Speed vs GHI')
            axes[0,0].grid(True, alpha=0.3)
            plots_created += 1
        
        # RH vs Tamb
        if all(col in self.df.columns for col in ['RH', 'Tamb']):
            axes[0,1].scatter(self.df['RH'], self.df['Tamb'], alpha=0.6, color='blue')
            axes[0,1].set_xlabel('Relative Humidity (%)')
            axes[0,1].set_ylabel('Temperature (°C)')
            axes[0,1].set_title('Relative Humidity vs Temperature')
            axes[0,1].grid(True, alpha=0.3)
            plots_created += 1
        
        # RH vs GHI
        if all(col in self.df.columns for col in ['RH', 'GHI']):
            axes[1,0].scatter(self.df['RH'], self.df['GHI'], alpha=0.6, color='green')
            axes[1,0].set_xlabel('Relative Humidity (%)')
            axes[1,0].set_ylabel('GHI (W/m²)')
            axes[1,0].set_title('Relative Humidity vs GHI')
            axes[1,0].grid(True, alpha=0.3)
            plots_created += 1
        
        # WD vs GHI
        if all(col in self.df.columns for col in ['WD', 'GHI']):
            axes[1,1].scatter(self.df['WD'], self.df['GHI'], alpha=0.6, color='purple')
            axes[1,1].set_xlabel('Wind Direction (°)')
            axes[1,1].set_ylabel('GHI (W/m²)')
            axes[1,1].set_title('Wind Direction vs GHI')
            axes[1,1].grid(True, alpha=0.3)
            plots_created += 1
        
        if plots_created > 0:
            plt.tight_layout()
            plt.show()
        else:
            print("❌ No scatter plots could be created - missing required columns")

    def generate_wind_analysis(self):
        """Generate wind rose and wind analysis"""
        if all(col in self.df.columns for col in ['WD', 'WS']):
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), subplot_kw=dict(projection='polar'))
            
            # Wind Rose
            theta = np.radians(self.df['WD'].dropna())
            radii = self.df['WS'].dropna()
            
            ax1.scatter(theta, radii, alpha=0.6)
            ax1.set_title('Wind Rose - Direction vs Speed')
            
            # Wind Speed distribution
            wind_bins = np.linspace(0, self.df['WS'].max(), 12)
            wind_dir_bins = np.linspace(0, 2*np.pi, 13)
            
            ax2.hist(theta, bins=wind_dir_bins, alpha=0.7)
            ax2.set_title('Wind Direction Distribution')
            
            plt.tight_layout()
            plt.show()
        else:
            print("❌ Wind direction/speed data not available for wind analysis")
                

    # Example Usage
if __name__ == "__main__":
    # Initialize EDA
    eda = SolarDataEDA("data/benin.csv")
        
    # Load and clean data
    eda.load_data()
    eda.clean_data()
        
    # Perform analysis
    eda.solar_radiation_timeseries()
    eda.daily_solar_patterns()
    eda.correlation_analysis()
    eda.distribution_analysis()
    eda.outlier_analysis()
    eda.cleaning_impact_analysis()
        
# Export cleaned data
eda.export_cleaned_data() 

            