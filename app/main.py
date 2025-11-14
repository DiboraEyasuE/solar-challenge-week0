import streamlit as st
from app.utils import load_data, get_summary_stats, create_boxplot, top_regions_table

st.title("Solar Resource Dashboard")
st.write("Visualize solar irradiance data interactively.")

# --- Country selector ---
country = st.selectbox(
    "Select a Country",
    ["Benin", "Sierra", "Togo"]
)

# Load dataset
df = load_data(country)

# Handle errors
if "Error" in df.columns:
    st.error(df["Error"].iloc[0])
    st.stop()

# --- Metric selector (only GHI available) ---
metric = st.selectbox("Select a Metric", ["GHI"])

# Show preview
st.subheader("Data Preview")
st.write(df.head())

# Summary stats
st.subheader("Summary Statistics")
st.write(get_summary_stats(df))

# Boxplot
st.subheader("Boxplot of GHI")
fig = create_boxplot(df, metric)
st.pyplot(fig)

# Top regions (if files contain region column)
st.subheader("Top Regions (By Avg GHI)")
table = top_regions_table(df)
if isinstance(table, str):
    st.info(table)
else:
    st.write(table)
