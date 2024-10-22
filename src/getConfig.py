# get data from config yaml file
import logging
import os.path
import yaml


def get_config(x):
    logging.debug("Getting config...")
    config_path = os.path.join(os.path.dirname(__file__), "../config/config.yaml")
    with open(os.path.abspath(config_path), "r") as file:
        data = yaml.safe_load(file)
    logging.debug("File closed")
    return data.get(x)
