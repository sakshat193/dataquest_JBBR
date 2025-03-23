# TerraShieldRepository

## Overview

TerraShield is a comprehensive project focused on earthquake data analysis and alert prediction. This repository is organized into distinct folders, each serving a specific purpose in the data processing and modeling pipeline.

## Folder Structure

### 1. Notebooks

This directory contains Jupyter notebooks dedicated to data preprocessing, exploratory data analysis (EDA), and model development. The notebooks are organized as follows:

- **train1:** Preprocessing of location and country data, including cleaning and handling missing values.
- **train2:** Preprocessing of continent data, utilizing geocoding techniques to fill missing entries.
- **train2(EDA):** Exploratory data analysis and preprocessing of the alert column, establishing initial alert classifications.
- **train3:** Development of the alert prediction model using XGBoost, training on key features to predict alert levels.
- **train4:** Application of the alert prediction model for imputing missing alert values and evaluating model performance. This notebook also underpins the alert evaluation feature in the web application.
- **EDA/EDA_aishwarya:** Contains all the EDA which was presented in the report

#### Subdirectories:

- **Models:** Contains serialized trained models in pickle format, ready for deployment and inference.
- **Predictions_training:** Houses scripts for model building and fitting. Each script is named to reflect its specific function and also contains pickle files of few models

### 2. Datasets

This folder includes all versions of the dataset in CSV format, documenting the progression from raw data through various preprocessing stages to the finalized, cleaned datasets.

### 3. Streamlit

Contains all necessary files for the web application, including Streamlit scripts, configuration files, and associated resources required for deployment.

## Usage

1. **Data Preprocessing and Model Training:** Begin with the notebooks in the **Notebooks** directory to understand the data cleaning, preprocessing, and model development processes.
2. **Datasets Access:** Refer to the **Datasets** folder for raw and processed data files utilized throughout the project.
3. **Web Application Deployment:** Use the files in the **Streamlit** directory to set up and run the web application for interactive data analysis and model evaluation.

This structured organization facilitates a clear workflow, enabling efficient navigation through the project's components and supporting seamless collaboration and development.
