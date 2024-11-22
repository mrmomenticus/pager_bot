import logging
import yaml


import argparse


def load_config(path):
    try:
        with open(path, "r") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logging.critical(f"Error loading config: {e}")


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="path to config file")
args = parser.parse_args()
cfg = load_config(args.config)

