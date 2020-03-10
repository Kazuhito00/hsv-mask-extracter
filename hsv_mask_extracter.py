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

    cvui.init('cvui')

    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    cv.namedWindow('image')
    cv.setMouseCallback('image', mouse_callback)

    hsv_point = None

    lower_hsv = [0, 0, 0]
    upper_hsv = [0, 0, 0]

    lower_h, upper_h = [0.0], [0.0]
    lower_s, upper_s = [0.0], [0.0]
    lower_v, upper_v = [0.0], [0.0]
    while True:
        cvuiframe = np.zeros((300, 600, 3), np.uint8)
        cvuiframe[:] = (49, 52, 49)
        cvui.trackbar2(cvuiframe, 30, 30, 300, lower_h, upper_h, 0, 360, 1,
                       '%.0Lf')
        cvui.trackbar2(cvuiframe, 30, 130, 300, lower_s, upper_s, 0, 255, 1,
                       '%.0Lf')
        cvui.trackbar2(cvuiframe, 30, 230, 300, lower_v, upper_v, 0, 255, 1,
                       '%.0Lf')
        cvui.update()
        cv.imshow('cvui', cvuiframe)

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

            kernel = np.ones((5, 5), np.uint8)
            mask_hsv = cv.morphologyEx(mask_hsv, cv.MORPH_CLOSE, kernel)

            contours = cv.findContours(mask_hsv, cv.RETR_EXTERNAL,
                                       cv.CHAIN_APPROX_SIMPLE)[0]
            contours = sorted(
                contours, key=lambda x: cv.contourArea(x), reverse=True)
            out = np.zeros_like(mask_hsv)
            mask = None
            for i, controur in enumerate(contours):
                if i < 1:
                    mask = cv.drawContours(
                        out, [controur], -1, color=255, thickness=-1)

            cv.imshow('mask', mask_hsv)
            if mask is not None:
                cv.imshow('mask2', mask)

        cv.imshow('image', frame)
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break


if __name__ == '__main__':
    main()
