import pandas as pd
import matplotlib.pyplot as plt

def summarize_missing_by_country(df, time_cols=["Quarter", "Year"]):
    """
    Summarizes missing values per country column in a DataFrame.
    
    Parameters:
    - df: pd.DataFrame containing time columns and country columns
    - time_cols: list of columns to exclude from missing value summary
    
    Returns:
    - pd.DataFrame with total missing counts and percentage per country
    """
    country_cols = [col for col in df.columns if col not in time_cols]
    missing_counts = df[country_cols].isna().sum()
    missing_percent = df[country_cols].isna().mean() * 100

    summary_df = pd.DataFrame({
        "Missing Count": missing_counts,
        "Missing %": missing_percent.round(2)
    }).sort_values("Missing Count", ascending=False)

    return summary_df

def get_missing_entries(df, time_cols=["Quarter", "Year"]):
    """
    Returns a DataFrame showing all missing values with their time context and country.
    
    Parameters:
    - df: pd.DataFrame with time columns and country columns
    - time_cols: list of columns to retain for context
    
    Returns:
    - pd.DataFrame with rows for each missing value, showing Year, Quarter, and Country
    """
    country_cols = [col for col in df.columns if col not in time_cols]
    melted = df.melt(id_vars=time_cols, value_vars=country_cols,
                     var_name="Country", value_name="Value")
    
    missing_df = melted[melted["Value"].isna()].sort_values(time_cols + ["Country"])
    return missing_df.reset_index(drop=True)

def clean_country_missing_entries(df, country_name, time_cols=["Year", "Quarter"]):
    """
    Filters and cleans missing entries for a specific country from a long-format DataFrame.
    
    Parameters:
    - df: pd.DataFrame with columns including 'Country', 'Year', 'Quarter', and 'Value'
    - country_name: str, name of the country to filter
    - time_cols: list of str, columns to sort by (default: ['Year', 'Quarter'])
    
    Returns:
    - pd.DataFrame filtered for the country, sorted by time, with reset index
    """
    # Filter for the selected country
    country_df = df[df["Country"] == country_name]

    # Sort by Year and Quarter
    country_df_sorted = country_df.sort_values(by=time_cols, ascending=True)

    # Reset index
    country_df_cleaned = country_df_sorted.reset_index(drop=True)

    return country_df_cleaned

def filter_by_year(df, min_year=None, max_year=None, exclude_years=None):
    """
    Filters a DataFrame by year range and optionally excludes specific years.
    
    Parameters:
    - df: pd.DataFrame with a 'Year' column
    - min_year: int, keep rows with Year > min_year (optional)
    - max_year: int, keep rows with Year <= max_year (optional)
    - exclude_years: list of int, years to exclude from the result (optional)
    
    Returns:
    - pd.DataFrame filtered by year, with reset index
    """
    filtered_df = df.copy()

    if min_year is not None:
        filtered_df = filtered_df[filtered_df["Year"] > min_year]
    
    if max_year is not None:
        filtered_df = filtered_df[filtered_df["Year"] <= max_year]
    
    if exclude_years is not None:
        filtered_df = filtered_df[~filtered_df["Year"].isin(exclude_years)]

    return filtered_df.reset_index(drop=True)

def average_by_year(df, drop_quarter=True, preview=True):
    """
    Groups a DataFrame by 'Year' and averages country values.
    Optionally drops the 'Quarter' column and previews the result.
    
    Parameters:
    - df: pd.DataFrame with 'Year' and country columns
    - drop_quarter: bool, whether to drop the 'Quarter' column (default: True)
    - preview: bool, whether to print the head of the result (default: True)
    
    Returns:
    - pd.DataFrame with yearly averages
    """
    # Drop 'Quarter' if requested and present
    if drop_quarter and "Quarter" in df.columns:
        df = df.drop(columns="Quarter")

    # Group by year and average
    df_avg = df.groupby("Year").mean(numeric_only=True).reset_index()

    # Preview the result
    if preview:
        print(df_avg.head())

    return df_avg

def plot_countries(df, exclude_country=None, legend_columns=4):
    """
    Plots country data over years, excluding one country if specified.
    Displays the legend at the top in multiple columns.
    
    Parameters:
    - df: DataFrame with 'Year' and country columns
    - exclude_country: str, name of the country to exclude from the plot
    - legend_columns: int, number of columns in the legend
    """
    plt.figure(figsize=(14, 8))

    # Filter out the excluded country
    country_cols = [col for col in df.columns if col != "Year" and col != exclude_country]

    # Plot each remaining country
    for country in country_cols:
        plt.plot(df["Year"], df[country], label=country)

    plt.xlabel("Year")
    plt.ylabel("Value")
    title = "Yearly Data for Countries"
    if exclude_country:
        title += f" (excluding {exclude_country})"
    plt.title(title)

    # Stylized legend at the top
    plt.legend(loc="right", bbox_to_anchor=(0.5, 1.3),
               ncol=legend_columns, fontsize="small", frameon=False)

    plt.grid(True)
    plt.tight_layout()
    plt.show()
