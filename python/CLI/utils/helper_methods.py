import json
import os
import logging

logger = logging.getLogger("emp_logger")
logger.setLevel(logging.DEBUG)
logger.propagate = False

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "actions.log")
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

file_handler.setFormatter(logging.Formatter(
    '%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | line:%(lineno)d | %(message)s'
))

if not logger.handlers:
    logger.addHandler(file_handler)


def save_to_json(data,file):
    try:
       with open(file,"w") as f:
          json.dump(data,f,indent=4)
    except Exception as e:
        logger.info(f"data saved successfully from {file}")


def load_from_json(file):
    try:
        if not os.path.exists(file):
            logger.warning("file not found  ")
            return []
        with open(file,"r") as f:
            return json.load(f)
        logger.info("file found successfully")
    except Exception as e:
        logger.info(f"data loaded from the {file} successfully"),200