import json
import time
import numpy as np
import cv2
from bot_logic import generate_task_list, execute_jobs
import adb_functions as ADB


def get_screenshot() -> np.array:
    raw_ss = device.exec_out('screencap -p', decode=False)
    image_np = np.frombuffer(raw_ss, np.uint8)

    return cv2.imdecode(image_np, cv2.IMREAD_COLOR)


def main():
    JSON_FILENAME = 'full_test.json'
    with open(JSON_FILENAME, 'r') as json_file:
        logic = json.load(json_file)

    jobs = generate_task_list(logic)

    while True:
        execute_jobs(jobs)
        time.sleep(5)

    # run_fl_cycle()


if __name__ == "__main__":
    # Initialize the connection

    SCREENSHOT = False
    if SCREENSHOT is True:
        device = ADB.get_device()

        screenshot = get_screenshot()
        cv2.imwrite('screenshot.png', screenshot)

    main()
