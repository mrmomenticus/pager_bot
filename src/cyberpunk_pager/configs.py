import yaml

def load_config():
    try:
        with open('config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")


cfg = load_config()