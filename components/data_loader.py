import requests
import os
import pandas as pd
import streamlit as st

# Function to fetch file from GitHub
def fetch_file_from_github(filepath, is_csv=True):
    # Load GitHub token and repo details from Streamlit secrets
    github_token = st.secrets["github"]["token"]
    repo = st.secrets["github"]["repo"]
    branch = st.secrets["github"]["branch"]

    # Construct the GitHub API URL
    file_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{filepath}"
    headers = {"Authorization": f"token {github_token}"}

    # Fetch the file
    response = requests.get(file_url, headers=headers)

    if response.status_code == 200:
        if is_csv:
            # If the file is CSV, load into a DataFrame
            data = pd.read_csv(filepath_or_buffer=response.content.decode('utf-8'))
            return data
        else:
            # For other files, return the raw content
            return response.content
    else:
        st.error(f"Failed to fetch file from GitHub: {response.status_code}")
        return None

# Example usage: Fetch sensor data CSV
def get_sensor_data():
    return fetch_file_from_github("data/sensor_data.csv")

# Example usage: Fetch energy data CSV
def get_energy_data():
    return fetch_file_from_github("data/energy_data.csv")

# Example usage: Fetch Teachable Machine model
def get_teachable_machine_model():
    model_data = fetch_file_from_github("models/teachable_machine/model.h5", is_csv=False)
    model_path = "./temp_model.h5"
    with open(model_path, "wb") as f:
        f.write(model_data)
    return model_path
