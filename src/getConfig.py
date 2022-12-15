# get data from config yaml file
import os.path
import yaml


def get_config(x):
    with open(os.path.abspath("../config/config.yaml"), "r") as file:
        data = yaml.safe_load(file)
    return data.get(x)
