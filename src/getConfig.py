# get data from config yaml file
import yaml


def getConfig(x):
    with open("../config/config.yaml", "r") as file:
        data = yaml.safe_load(file)
    return data.get(x)
