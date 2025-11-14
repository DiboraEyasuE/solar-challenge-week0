# Solar Data Analysis Project

# Overview

This project focuses on analyzing how different environmental measurements affect a country's potential for solar installation. By employing statistical modeling, we aim to provide actionable insights for investors, analysts, and policymakers. 

## Business Objective

The primary goal is to study how solar radiation, air temperature, relative humidity, barometric pressure, precipitation, wind speed, and wind direction along with cleaned and soiled radiance sensor (soiling measurement) affect the potential for solar installation.

## Situational Overview

As an analytics engineer at MoonLight Energy Solutions, a consultancy firm specializing in data-driven insights for the energy sector, the analysis aims to:
  * Identify key events affecting solar irradiance which is a key element for solar installation decade.
  * Measure the impact of these events on price changes.
  * Provide clear, data-driven insights to guide investment strategies and policy development

## Data

The dataset includes environmental variable records from August 9, 2021, to August 9, 2022 capturing the full annual cycle in the fields
  * GHI (W/m²): Global Horizontal Irradiance, the total solar radiation received per square meter on a horizontal surface.
  * DNI (W/m²): Direct Normal Irradiance, the amount of solar radiation received per square meter on a surface perpendicular to the rays of the sun.
  * DHI (W/m²): Diffuse Horizontal Irradiance, solar radiation received per square meter on a horizontal surface that does not arrive on a direct path from the sun.
  * ModA (W/m²): Measurements from a module or sensor (A), similar to irradiance.
  * ModB (W/m²): Measurements from a module or sensor (B), similar to irradiance.
  * Tamb (°C): Ambient Temperature in degrees Celsius.
  * RH (%): Relative Humidity as a percentage of moisture in the air.
  * WS (m/s): Wind Speed in meters per second.
  * WSgust (m/s): Maximum Wind Gust Speed in meters per second.
  * WSstdev (m/s): Standard Deviation of Wind Speed, indicating variability.
  * WD (°N (to east)): Wind Direction in degrees from north.
  * WDstdev: Standard Deviation of Wind Direction, showing directional variability.
  * BP (hPa): Barometric Pressure in hectopascals.
  * Cleaning (1 or 0): Signifying whether cleaning (possibly of the modules or sensors) occurred.
  * Precipitation (mm/min): Precipitation rate measured in millimeters per minute.
  * TModA (°C): Temperature of Module A in degrees Celsius.
  * TModB (°C): Temperature of Module B in degrees Celsius

## Learning Outcomes

* Skills:
 * * Statistical data visualisation using matplotlib
 * * Understanding the meaning of zscore and outlier detection
* Knowledge:
 * * Probability distributions and their relevance
 * * Time series analysis techniques

## Project Tasks

### Task 1: Git & Environment Setup
 * Initialising Repository
 * Branching and commits and 
 * Basic CI integration
### Task 2: Data Profiling, Cleaning & EDA
 * Summary Statistics and Missing Value Report
 * Outlier Detection & Basic Cleaning
 * Time Series Analysis
 * Cleaning impact
 * Correlation & Relationship Analysis
 * Wind & Distribution Analysis
 * Temperature analysis
 * Bubble chart
### Task 3: Cross-Country Comparison
 * Metric Comparison
  * * Boxplots
  * * Summary Testing
 * Statistical Testing
 * Key observation
 * Visual Summary
##  Prerequisites
- Git
- Python 3.13.3

## Installation setups
- Create a virtual environment
  ```
  python -m venv .venv
  ```
- Activate it
  - Windows: 
    ```
    .venv\Scripts\activate
    ```
  - Mac/Linux: 
    ```
    source .venv/bin/activate
    ```
- Install dependencies
  ```
  pip install -r requirements.txt
  ```
- Verify setup
  ```
  pip list
  ```

  # 🌞 Solar Resource Dashboard  
A simple and interactive Streamlit dashboard for visualizing solar irradiance data (GHI).  
This application demonstrates clean UI design, modular Python structure, and real-time data exploration.

---

## Key Features
- **Interactive Country Selection** (Benin, Sierra Leone, Togo)
- **Metric Selector** (GHI)
- **Boxplot Visualization** using Matplotlib
- **Summary Statistics**
- **Top Regions Table** (if region column exists)
- **Modular Folder Structure** using `app/` and `scripts/`
- **Ready for Deployment** on Streamlit Community Cloud
---

---

## Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd solar-challenge-week0
```
or
### Run app locally
streamlit run app/main.py

## 📁 Project Structure


  ## Author
  Developed by Dibora EyasuE