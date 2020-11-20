import os
import logging.config

import yaml
def setup_logging(
        default_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.yaml'),
        default_level=logging.INFO):
    """Setup logging configuration
    """
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def get_logger(name):
    return logging.getLogger(name)
