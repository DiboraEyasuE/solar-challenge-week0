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
        return self.df
    

    def basic_info(self):
        print(self.df.head())
        self.df.describe()
    
    def clean_data(self):
        """Removes highly null columns and outliers for a proper data visualization"""
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
            outliers = (outlier_flags > 3).any(axis=1)
            self.df['Outliers'] = outliers
        print("✅ Data cleaning completed!")
        return self.df


    def export_cleaned_data(self, country_name="benin"):
        """ Export cleaned dataset to CSV """
        output_path = f'../data/{country_name}_clean.csv'
        self.df.to_csv(output_path, index=False)
        print(f"✅ Cleaned data exported to: {output_path}")


    def time_series_analysis(self):
        """ Visualize solar radiation patterns over time for the indicator columns """
        plt.figure(figsize=(15, 10))
        
        plt.subplot(2, 2, 1)
        plt.plot(self.df.index, self.df['GHI'], color='orange', alpha=0.7)
        plt.title('* GHI Over Time')
        plt.ylabel('GHI (W/m²)')
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, 2)
        plt.plot(self.df.index, self.df['DNI'], color='red', alpha=0.7)
        plt.title(' ** DNI Over Time')
        plt.ylabel('DNI (W/m²)')
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, 3)
        plt.plot(self.df.index, self.df['DHI'], color='blue', alpha=0.7)
        plt.title(' # DHI Over Time')
        plt.ylabel('DHI (W/m²)')
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, 4)
        plt.plot(self.df.index, self.df['Tamb'], color='green', alpha=0.7)
        plt.title('## Temperature Over Time')
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
        outlier_summary = self.df['Outliers'].value_counts()
        
        plt.figure(figsize=(8, 6))
        outlier_summary.plot(kind='bar', color=['green', 'red'])
        plt.title('🎯 Outlier Distribution in Dataset')
        plt.xlabel('Outliers')
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


# Example Usage
if __name__ == "__main__":
    # Initialize EDA
    eda = SolarDataEDA("data/benin.csv")
    
    # Load and clean data
    eda.load_data()
    eda.clean_data()
    eda.basic_info()

    # Perform analysis
    eda.time_series_analysis()
    eda.daily_solar_patterns()
    eda.correlation_analysis()
    eda.distribution_analysis()
    eda.outlier_analysis()
    eda.cleaning_impact_analysis()
    
    # Export cleaned data
    eda.export_cleaned_data() 

        