import streamlit as st
from utils import load_data, get_summary_stats, create_boxplot, top_regions_table

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
st.subheader("Top GHI Rankings")

if "region" not in df.columns:
    st.info(
        "Region-level analysis is unavailable because the dataset does not contain "
        "a 'region' or 'location' field. "
        "Showing alternative ranking: Top Months by Average GHI."
    )
    
    df['month'] = df['Timestamp'].dt.month
    ghi_by_month = df.groupby('month')['GHI'].mean()
    st.bar_chart(ghi_by_month)

else:
    # Region ranking plot
    top_regions = df.groupby('region')['GHI'].mean().sort_values(ascending=False)
    st.bar_chart(top_regions)

