import pandas as pd
import yaml
import os

# create a function to load a yaml file
def load_yaml(file):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(project_root, "config", file)
    with open(file_path) as f:
        return yaml.safe_load(f)

# function to load a csv file from the data folder
def load_csv(file):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(project_root,"data", file)
    return pd.read_csv(file_path, index_col="timestep", parse_dates=["timestep"])