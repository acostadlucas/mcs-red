# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Monte Carlo Simulation project for Real Estate Development (MCS-RED) that analyzes financial risk in real estate strategy selection. The project combines:
- ETL processes for macroeconomic data scraping and cleaning
- Statistical hypothesis testing on country economic profiles
- Monte Carlo simulations using Geometric Brownian Motion (GBM) and Cox-Ingersoll-Ross (CIR) models
- Country similarity analysis for real estate market comparisons

## Environment Setup

**Python Version**: >=3.11

**Dependency Management**: Poetry

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run Jupyter notebooks
jupyter notebook
```

**Environment Variables**: The `.env` file contains scraping target URLs for various economic indicators from theglobaleconomy.com. These URLs are used in the ETL crawlers.

## Key Commands

### Development
```bash
# Launch Jupyter Lab for notebook work
jupyter lab

# Run a specific notebook (example)
jupyter nbconvert --execute --to notebook hypothesis_test/hypothesis_test_01.ipynb
```

### Data Processing
The project uses Jupyter notebooks exclusively for data processing. There are no CLI scripts to run. Key workflows are:
1. ETL_first_iteration: Web scraping macroeconomic data
2. ETL_second_iteration: Data cleaning and transformation
3. hypothesis_test: Statistical analysis and hypothesis testing
4. python_finance_simulations_statistics: Monte Carlo simulations

## Architecture

### Data Flow

1. **ETL_first_iteration/crawlers_and_transformers/**: Web scraping notebooks that extract economic indicators (GDP, HPI, CPI, unemployment, etc.) from theglobaleconomy.com
   - Each scraper targets a specific economic indicator
   - Outputs raw data to `data/` directory

2. **ETL_second_iteration/**: Data cleaning and transformation
   - `quarters_clean.py`: Reusable utility functions for missing value analysis, country filtering, and visualization
   - Clean notebooks (clean_*.ipynb) process raw data and handle missing values using forward fill (ffill) method
   - Outputs cleaned data to `data/` as parquet files

3. **data/**: Central data storage
   - `data/by_country/`: Country-specific macroeconomic profiles (e.g., `Australia_macro_profile.parquet`)
   - `data/for_thesis/`: Prepared datasets for thesis analysis (synthetic HPI, volatility calculations)
   - Clean indicator files: `clean_hpi.parquet`, `clean_gdp.parquet`, etc.

4. **hypothesis_test/**: Statistical analysis (104 notebooks)
   - Correlation analysis between macroeconomic indicators and house prices
   - Missing value imputation strategies (ffill preferred over interpolation)
   - Country profile comparisons

5. **python_finance_simulations_statistics/**: Monte Carlo simulations and financial modeling
   - `mcs_gbm_10paths.ipynb`: Geometric Brownian Motion simulation for house price projections
   - `msc_cir_5paths.ipynb`: Cox-Ingersoll-Ross model for interest rate simulation
   - `country_similarity.ipynb`: Country economic similarity ranking using volatility, CV, and trend metrics
   - `a_market_conditions.ipynb`, `b_time_to_sell.ipynb`, `c_cost_involved.ipynb`: Real estate decision modeling

### Key Utilities

**quarters_clean.py** (ETL_second_iteration/quarters_clean.py):
- `summarize_missing_by_country()`: Analyze missing values per country
- `get_missing_entries()`: Extract detailed missing value locations
- `clean_country_missing_entries()`: Filter and clean country-specific data
- `filter_by_year()`: Year-range filtering with exclusions
- `average_by_year()`: Convert quarterly data to yearly averages
- `plot_countries()`: Visualize country comparisons

### Data Processing Patterns

**Missing Value Strategy**: The project uses **forward fill (ffill)** as the primary imputation method. This was chosen after analysis showing that maintaining constant values for gaps is less risky than interpolation with limited data points.

**Time Range**: Most analysis focuses on 2016-2024, with earlier data cleaned if insufficient coverage exists.

**Country Profiles**: Each country has a unified DataFrame with columns:
- Year
- labor_force, livestock_prod, agr_land, urban_pop
- gov_exp, reserves, investment
- cpi, gdp, priv_cred, unemployment
- house_price

### Monte Carlo Simulation Parameters

**Geometric Brownian Motion (GBM)** for house prices:
```python
# Key parameters calculated from historical data:
# - mu (drift): Estimated from mean of log returns (~0.05 for Paraguay example)
# - sigma (volatility): Standard deviation of log returns (~0.02 for Paraguay example)
# - S0: Initial house price index
# - T: Time horizon (typically 1 year)
# - dt: Time step (1/12 for monthly, 1/50 for finer resolution)
```

Functions in simulation notebooks:
- `estimate_drift()`: Calculate drift from HPI series
- `estimate_volatility()`: Calculate volatility from log returns
- `geometric_brownian_motion()`: Generate price paths

### Correlation Analysis Pattern

Notebooks frequently analyze:
1. Correlation matrices between macroeconomic indicators
2. Ranking indicators by correlation with house_price
3. Identifying most/least correlated pairs for each indicator

Standard workflow:
```python
# 1. Load country profile
df = pd.read_parquet("data/by_country/CountryName_macro_profile.parquet")

# 2. Apply ffill and filter years
df = df.ffill()
df = df[df['Year'] >= 2016].reset_index(drop=True)

# 3. Correlation analysis
corr_matrix = df.drop(columns=['Year']).corr()
# Focus on correlation with house_price
```

## Important Notes

- **No traditional test suite**: This is a research/thesis project using notebooks for exploratory analysis
- **Data sources**: All economic data scraped from theglobaleconomy.com (URLs in .env)
- **Output formats**: Primarily parquet files for efficient storage and pandas compatibility
- **Visualization**: Heavy use of matplotlib and seaborn for plots throughout notebooks
- **Country similarity**: Uses combined metrics (volatility, coefficient of variation, trend) to rank economic similarity between countries

## Project Context

This project supports a thesis on real estate development strategy selection. The Monte Carlo approach simulates various market scenarios to assess financial risk across different development alternatives. The country similarity analysis helps identify comparable markets for benchmarking real estate behavior.
