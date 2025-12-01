import os
import json

CONFIG_FILE = "app_config.json"
VERSION = "2.0.0"

DEFAULT_CONFIG = {
    "model_repo_id": "distilbert-base-uncased",
    "chunk_size": 500,
    "chunk_overlap": 50,
    "num_search_results": 5,
    "top_k": 10,
    "dimension": 768
}


def load_config():
    """Load configuration from file or return defaults"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Ensure all default keys exist
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        except:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_version():
    """Get application version"""
    return VERSION

