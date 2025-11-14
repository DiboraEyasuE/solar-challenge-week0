import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def create_country_selector():
    countries = ['Benin', 'Ghana', 'Nigeria', 'Togo']
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        options=countries,
        default=countries[:2]
    )
    return selected_countries

def create_metric_selector():
    metrics = ['GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'RH']
    selected_metric = st.sidebar.selectbox(
        "Select Solar Metric",
        options=metrics
    )
    return selected_metric

def create_boxplot(df, selected_countries, selected_metric):
    fig, ax = plt.subplots()
    
    data_to_plot = []
    labels = []
    for country in selected_countries:
        country_data = df[df['Country'] == country]
        if selected_metric in country_data.columns:
            data_to_plot.append(country_data[selected_metric].dropna())
            labels.append(country)
    
    if data_to_plot:
        ax.boxplot(data_to_plot, labels=labels)
        ax.set_title(f'Boxplot of {selected_metric}')
        ax.set_ylabel(selected_metric)
    
    return fig

def create_top_regions_table(df, selected_countries):
    if 'Region' in df.columns and 'GHI' in df.columns:
        top_data = []
        for country in selected_countries:
            country_data = df[df['Country'] == country]
            if not country_data.empty:
                top_region = country_data.loc[country_data['GHI'].idxmax()]
                top_data.append({
                    'Country': country,
                    'Top Region': top_region['Region'],
                    'Max GHI': round(top_region['GHI'], 2)
                })
        return pd.DataFrame(top_data)
    return pd.DataFrame()