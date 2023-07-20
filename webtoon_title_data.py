import subprocess
import time
from tqdm import tqdm

def execute_script(script_path):
    retry_limit = 3  # Number of retries
    retry_delay = 5  # Delay between retries in seconds

    for _ in range(retry_limit):
        try:
            subprocess.check_call(["python", script_path])
            return True
        except subprocess.CalledProcessError:
            print(f"Error executing {script_path}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    return False

# Specify the file paths for webtoon.py and webtoon_additional_data.py
webtoon_script_path = "D:/Files/Project/WebtoonTitleScrap\WebtoonIDTitleScrap/webtoon.py"
additional_data_script_path = "D:/Files/Project/WebtoonTitleScrap\WebtoonIDTitleScrap/webtoon_additional_data.py"

# Execute webtoon.py
print("Executing webtoon.py...")
if execute_script(webtoon_script_path):
    print("webtoon.py execution successful")
else:
    print("webtoon.py execution failed")

# Execute webtoon_additional_data.py
print("Executing webtoon_additional_data.py...")
if execute_script(additional_data_script_path):
    print("webtoon_additional_data.py execution successful")
else:
    print("webtoon_additional_data.py execution failed")
