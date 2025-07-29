import os 
import logging
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%H_%S')}.log"

#for saving paths of my logs

log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)

#getcwd = get current working directory

LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

logging.basicConfig(level=logging.INFO,
        filename=LOG_FILEPATH,
        format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s')