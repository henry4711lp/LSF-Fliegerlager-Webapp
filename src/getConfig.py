# get data from config yaml file
import logging
import os.path
import yaml


def get_config(x):
    logging.debug("Getting config...")
    with open(os.path.abspath("../config/config.yaml"), "r") as file:
        data = yaml.safe_load(file)
    logging.debug("File closed")
    return data.get(x)
