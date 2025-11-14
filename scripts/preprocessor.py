def clean_column_names(df):
    df.columns = [c.strip().lower() for c in df.columns]
    return df
