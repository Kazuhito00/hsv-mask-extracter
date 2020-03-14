#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import cv2 as cv


class DebugGui:
    """
    [summary]
    Debug情報表示ウィンドウクラス
    [description]
    -
    """

    _window_position = [0, 0]

    _frame1 = None
    _frame2 = None

    _window_name = ''

    def __init__(self, window_name='DEBUG', window_position=[0, 0]):
        self._window_name = window_name
        cv.namedWindow(self._window_name)

        self._window_position = window_position

    def update(self, frame1, frame2):
        """
        [summary]
          描画内容更新
        """
        self._frame1 = copy.deepcopy(frame1)
        self._frame2 = copy.deepcopy(frame2)

    def show(self):
        """
        [summary]
          描画
        """
        if (self._frame1 is not None) and (self._frame1 is not None):
            debug_image = cv.hconcat([self._frame1, self._frame2])
            debug_image = cv.line(
                debug_image, (int(debug_image.shape[1] / 2), 0),
                (int(debug_image.shape[1] / 2), debug_image.shape[0]),
                (255, 255, 255),
                thickness=2)
            cv.imshow(self._window_name, debug_image)
        elif (self._frame1 is not None):
            cv.imshow(self._window_name, self._frame1)
        elif (self._frame2 is not None):
            cv.imshow(self._window_name, self._frame2)

        cv.moveWindow(self._window_name, self._window_position[0],
                      self._window_position[1])
