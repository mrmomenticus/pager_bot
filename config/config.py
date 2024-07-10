from venv import logger
import yaml

def load_config():
    try:
        with open('config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            logger.debug("Loaded config")
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None


cfg = load_config()
logger.setLevel(cfg["log_level"])