from datetime import datetime
import time
import logging
import os

def generate_default_filename():
    now = datetime.now()
    if not os.path.exists("reports"):
        os.mkdir("reports")
    return f"reports/report-{now.strftime('%Y-%m-%d-%H-%M')}.xlsx"

def keep_logging():
    while True:
        time.sleep(5)
        logging.info("Still running...")
