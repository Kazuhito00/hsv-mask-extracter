#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import cv2 as cv


class FrameGui:
    """
    [summary]
    カメラキャプチャ表示ウィンドウクラス
    [description]
    -
    """

    _window_position = [0, 0]

    _frame = None
    _click_point = None

    _window_name = ''

    def __init__(self, window_name='CAPTURE FRAME', window_position=[0, 0]):
        self._click_point = None

        self._window_name = window_name
        cv.namedWindow(self._window_name)
        cv.setMouseCallback(self._window_name, self._mouse_callback)

        self._window_position = window_position

    def _mouse_callback(self, event, x, y, flags, param):
        """
        [summary]
          マウス左クリック時のコールバック
        """
        self._click_point
        if event == cv.EVENT_LBUTTONDOWN:
            self._click_point = [x, y]

    def update(self, frame):
        """
        [summary]
          描画内容更新
        """
        self._frame = copy.deepcopy(frame)

    def show(self):
        """
        [summary]
          描画
        """
        if self._frame is not None:
            cv.imshow(self._window_name, self._frame)

        cv.moveWindow(self._window_name, self._window_position[0],
                      self._window_position[1])

    def get_mouse_l_click_point(self):
        """
        [summary]
          マウス左クリック座標を取得(一度のみ)
        """
        click_point = self._click_point
        self._click_point = None
        return click_point
