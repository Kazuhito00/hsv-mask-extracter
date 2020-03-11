#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv
import cvui

click_point = None


def mouse_callback(event, x, y, flags, param):
    global click_point
    if event == cv.EVENT_LBUTTONDOWN:
        click_point = [x, y]


def main():
    global click_point

    setting_window_name = 'SETTING'
    image_window_name = 'IMAGE'
    mask_window_name = 'MASK'

    cvui.init(setting_window_name)

    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    cv.namedWindow(image_window_name)
    cv.setMouseCallback(image_window_name, mouse_callback)

    hsv_point = None

    lower_hsv = [0, 0, 0]
    upper_hsv = [0, 0, 0]
    lower_h, upper_h = [0.0], [0.0]
    lower_s, upper_s = [0.0], [0.0]
    lower_v, upper_v = [0.0], [0.0]
    is_reverse = [False]
    top_area_number = [1]
    kernel_size = [3]
    while True:
        cvuiframe = np.zeros((390, 400, 3), np.uint8)
        cvuiframe[:] = (49, 52, 49)

        cvui.trackbar2(cvuiframe, 90, 30, 300, lower_h, upper_h, 0, 360, 1,
                       '%.0Lf')
        cvui.printf(cvuiframe, 10, 40, 0.4, 0xffffff, 'H MAX : %d', upper_h[0])
        cvui.printf(cvuiframe, 10, 60, 0.4, 0xffffff, 'H MIN : %d', lower_h[0])

        cvui.trackbar2(cvuiframe, 90, 100, 300, lower_s, upper_s, 0, 255, 1,
                       '%.0Lf')
        cvui.printf(cvuiframe, 10, 110, 0.4, 0xffffff, 'S MAX : %d',
                    upper_s[0])
        cvui.printf(cvuiframe, 10, 130, 0.4, 0xffffff, 'S MIN : %d',
                    lower_s[0])

        cvui.trackbar2(cvuiframe, 90, 170, 300, lower_v, upper_v, 0, 255, 1,
                       '%.0Lf')
        cvui.printf(cvuiframe, 10, 180, 0.4, 0xffffff, 'V MAX : %d',
                    upper_v[0])
        cvui.printf(cvuiframe, 10, 200, 0.4, 0xffffff, 'V MIN : %d',
                    lower_v[0])

        cvui.printf(cvuiframe, 10, 260, 0.4, 0xffffff, 'TOP AREA NUMBER')
        cvui.counter(cvuiframe, 160, 255, top_area_number)
        top_area_number[0] = max(1, top_area_number[0])
        top_area_number[0] = min(100, top_area_number[0])

        cvui.printf(cvuiframe, 10, 300, 0.4, 0xffffff, 'CLOSE KERNEL SIZE')
        cvui.counter(cvuiframe, 160, 295, kernel_size, 2)
        kernel_size[0] = max(1, kernel_size[0])
        kernel_size[0] = min(25, kernel_size[0])

        cvui.checkbox(cvuiframe, 10, 340, 'MASK REVERSE', is_reverse)

        # cvui.button(cvuiframe, 160, 337, 'Capture')

        cvui.update()
        cv.imshow(setting_window_name, cvuiframe)

        # カメラキャプチャ ########################################################
        ret, frame = cap.read()
        if not ret:
            continue

        if click_point is not None:
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            hsv_point = hsv[click_point[1], click_point[0]]

            lower_hsv[0] = max(0, int(hsv_point[0] - 10))
            lower_hsv[1] = max(0, int(hsv_point[1] - 30))
            lower_hsv[2] = max(0, int(hsv_point[2] - 30))
            upper_hsv[0] = min(180, int(hsv_point[0] + 10))
            upper_hsv[1] = min(255, int(hsv_point[1] + 90))
            upper_hsv[2] = min(255, int(hsv_point[2] + 90))
            lower_h[0] = lower_hsv[0] * 2
            lower_s[0] = lower_hsv[1]
            lower_v[0] = lower_hsv[2]
            upper_h[0] = upper_hsv[0] * 2
            upper_s[0] = upper_hsv[1]
            upper_v[0] = upper_hsv[2]

            click_point = None

        if hsv_point is not None:
            lower_hsv[0] = int(lower_h[0] / 2)
            lower_hsv[1] = int(lower_s[0])
            lower_hsv[2] = int(lower_v[0])
            upper_hsv[0] = int(upper_h[0] / 2)
            upper_hsv[1] = int(upper_s[0])
            upper_hsv[2] = int(upper_v[0])

            hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask_hsv = cv.inRange(hsv_frame, np.array(lower_hsv),
                                  np.array(upper_hsv))

            kernel = np.ones((kernel_size[0], kernel_size[0]), np.uint8)
            mask_hsv = cv.morphologyEx(mask_hsv, cv.MORPH_CLOSE, kernel)

            contours = cv.findContours(mask_hsv, cv.RETR_EXTERNAL,
                                       cv.CHAIN_APPROX_SIMPLE)[0]
            contours = sorted(
                contours, key=lambda x: cv.contourArea(x), reverse=True)
            out = np.zeros_like(mask_hsv)
            mask = None
            for i, controur in enumerate(contours):
                if i < top_area_number[0]:
                    mask = cv.drawContours(
                        out, [controur], -1, color=255, thickness=-1)

            if mask is not None:
                if is_reverse[0]:
                    mask = cv.bitwise_not(mask)
                cv.imshow(mask_window_name, mask)

        cv.imshow(image_window_name, frame)
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break


if __name__ == '__main__':
    main()
