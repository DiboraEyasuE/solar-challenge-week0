import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from utils import create_country_selector, create_metric_selector, create_boxplot, create_top_regions_table
from scripts.preprocessor import load_sample_data

def main():
    st.set_page_config(page_title="Solar Data Dashboard", layout="wide")
    st.title("Solar Data Dashboard")
    
    # Sidebar widgets
    st.sidebar.header("Controls")
    selected_countries = create_country_selector()
    selected_metric = create_metric_selector()
    
    # Load data from scripts
    df = load_sample_data(selected_countries)
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Boxplot")
        fig = create_boxplot(df, selected_countries, selected_metric)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Top Regions Table")
        top_table = create_top_regions_table(df, selected_countries)
        st.dataframe(top_table)

if __name__ == "__main__":
    main()