import pandas as pd
import os
import matplotlib.pyplot as plt


# ------------------------------
# Load solar dataset
# ------------------------------
def load_data(country):
    file_map = {
        "Benin": "benin_clean.csv",
        "Sierra": "sierraleone_clean.csv",
        "Togo": "togo_clean.csv"
    }

    base_path = os.path.join(os.path.dirname(__file__), "..", "data")
    filename = os.path.join(base_path, file_map.get(country, ""))

    if not os.path.exists(filename):
        return pd.DataFrame({"Error": [f"File not found: {filename}"]})

    df = pd.read_csv(filename)

    if "GHI" not in df.columns:
        return pd.DataFrame({"Error": ["GHI column not found"]})

    return df.dropna(subset=["GHI"])


# ------------------------------
# Summary statistics
# ------------------------------
def get_summary_stats(df):
    return df["GHI"].describe()


# ------------------------------
# Boxplot 
# ------------------------------
def create_boxplot(df, metric):
    fig, ax = plt.subplots()
    ax.boxplot(df[metric], vert=True)
    ax.set_title(f"{metric} Distribution")
    ax.set_ylabel(metric)
    return fig


# ------------------------------
# Top regions table (if available)
# ------------------------------
def top_regions_table(df):
    if "region" not in df.columns:
        return "No region column available in this dataset."

    table = df.groupby("region")["GHI"].mean().sort_values(ascending=False).head(5)
    return table.reset_index()

