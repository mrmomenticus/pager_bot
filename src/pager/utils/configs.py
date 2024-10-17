import yaml


def load_config():
    try:
        with open("config/config_test.yaml", "r") as file: #TODO Поменять на config.yaml
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")


cfg = load_config()
