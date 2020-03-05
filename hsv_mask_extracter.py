#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv

click_point = None


def mouse_callback(event, x, y, flags, param):
    global click_point
    if event == cv.EVENT_LBUTTONDOWN:
        click_point = [x, y]


def main():
    global click_point

    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    cv.namedWindow('image')
    cv.setMouseCallback('image', mouse_callback)

    hsv_point = None

    lower_hsv = [0, 0, 0]
    upper_hsv = [0, 0, 0]

    while True:
        # カメラキャプチャ ########################################################
        ret, frame = cap.read()
        if not ret:
            continue

        if click_point is not None:
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            hsv_point = hsv[click_point[1], click_point[0]]
            click_point = None

        if hsv_point is not None:
            lower_hsv[0] = max(0, int(hsv_point[0] - 30))
            lower_hsv[1] = max(0, int(hsv_point[1] - 30))
            lower_hsv[2] = max(0, int(hsv_point[2] - 30))
            upper_hsv[0] = min(180, int(hsv_point[0] + 30))
            upper_hsv[1] = min(255, int(hsv_point[1] + 90))
            upper_hsv[2] = min(255, int(hsv_point[2] + 90))
            print(hsv_point, lower_hsv, upper_hsv)

            hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask_hsv = cv.inRange(hsv_frame, np.array(lower_hsv),
                                  np.array(upper_hsv))

            kernel = np.ones((15, 15), np.uint8)
            mask_hsv = cv.morphologyEx(mask_hsv, cv.MORPH_CLOSE, kernel)

            cv.imshow('mask', mask_hsv)

        cv.imshow('image', frame)
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break


if __name__ == '__main__':
    main()
