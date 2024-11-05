from DotDict import DotDict
from job import Role
from adb_functions import device as ADB
import cv2
import numpy as np
import time

DEFAULT_DRAG_DURATION = 1500
DEFAULT_CLICK_DURATION = 100


def generate_task_list(input_data: DotDict) -> list:
    role_list = [DotDict(role) for role in input_data]
    roles = [Role(role) for role in role_list]

    return roles


def execute_action(action, device=ADB):
    if len(action) == 2:
        x, y = action
        command = f'input tap {x} {y}'
    elif len(action) == 4:
        x1, y1, x2, y2 = action
        command = f'input swipe {x1} {y1} {x2} {y2} {DEFAULT_DRAG_DURATION}'

    else:
        return

    device.shell(command)


def execute_job(job):
    # print(job.next)
    if isinstance(job, list):
        execute_jobs(job)
    else:
        if job.trigger is not None and check_condition(job.trigger) is False:
            return
        else:
            # print(job.description)
            execute_action(job.click)
            time.sleep(1.5)
            # if job.new_screen is not None:
            if job.next is not None:
                execute_job(job.next)


def execute_jobs(job_list, device=ADB):
    for role in job_list:
        for job in role.tasks:
            execute_job(job)

    print("Finished running jobs.")


def convert_rgb_to_bgr(hex_color):
    # Remove the '#' if it's included in the hex code
    hex_color = hex_color.lstrip('#')

    # Split hex color into RGB components and convert each to an integer
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # Return BGR as a tuple
    bgr_color = (b, g, r)
    return bgr_color


def check_trigger(image, target_color):
    # Convert the hex color to BGR
    bgr_color = convert_rgb_to_bgr(target_color)

    # Convert the target color from BGR to HSV
    target_color_hsv = cv2.cvtColor(
        np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
    target_hue = target_color_hsv[0]

    # Define hue range with wrapping
    # target_lower = int(target_hue)
    lower_hue = target_hue - 5
    upper_hue = target_hue + 5

# Create lower and upper bounds for the hue range
    if lower_hue < upper_hue:
        lower_bound = np.array([lower_hue, 50, 50], dtype=np.uint8)
        upper_bound = np.array([upper_hue, 255, 255], dtype=np.uint8)
    else:
        # Handle the wrapping case by creating two ranges
        lower_bound1 = np.array([0, 50, 50], dtype=np.uint8)
        upper_bound1 = np.array([upper_hue, 255, 255], dtype=np.uint8)
        lower_bound2 = np.array([lower_hue, 50, 50], dtype=np.uint8)
        upper_bound2 = np.array([179, 255, 255], dtype=np.uint8)

    # Convert the image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create the mask for the hue range
    if lower_hue < upper_hue:
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    else:
        # Combine two masks for wrapped hue range
        mask1 = cv2.inRange(hsv_image, lower_bound1, upper_bound1)
        mask2 = cv2.inRange(hsv_image, lower_bound2, upper_bound2)
        mask = cv2.bitwise_or(mask1, mask2)

    # Find contours in the mask
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    valid_contours = [cv2.contourArea(contour)
                      for contour in contours
                      if cv2.contourArea(contour) > (hsv_image.shape[0]
                                                     * hsv_image.shape[1]
                                                     * .6)
                      ]
    # Draw contours on the original image (for visualization)
    # output_image = image.copy()
    # cv2.drawContours(output_image, contours, -1, (0, 255, 0), 2)

    # Display the result
    # cv2.imshow("Contours", output_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return len(valid_contours) > 0


def check_condition(trigger):
    screenshot = get_screenshot()
    bounds = trigger.area
    check_area = screenshot[bounds[1]:bounds[3], bounds[0]:bounds[2]]

    return check_trigger(check_area, trigger.color)


def get_screenshot() -> np.array:
    raw_ss = ADB.exec_out('screencap -p', decode=False)
    image_np = np.frombuffer(raw_ss, np.uint8)

    return cv2.imdecode(image_np, cv2.IMREAD_COLOR)


if __name__ == "__main__":
    test_action = [500, 500, 950, 1800]
    test_tap = [500, 500]
    # execute_action(test_tap)
