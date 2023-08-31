import subprocess
import logging
import json

class TrivyScanner:

    @staticmethod
    def scan(target):
        try:
            result = subprocess.run(['trivy', target, '-f', 'json', "--exit-code", "1"], capture_output=True, text=True)
            if result.returncode == 1:
                return result.stdout
            else:
                logging.error(json.loads(result.stderr))
                return None
        except Exception as e:
            logging.error(f"An error occurred while scanning: {str(e)}")
            return None
