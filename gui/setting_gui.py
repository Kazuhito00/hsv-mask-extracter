#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv
import gui.cvui as cvui


class SettingGui:
    """
    [summary]
    設定ウィンドウクラス
    [description]
    -
    """
    _window_position = [0, 0]

    _lower_h, _upper_h = [0.0], [0.0]
    _lower_s, _upper_s = [0.0], [0.0]
    _lower_v, _upper_v = [0.0], [0.0]
    _is_reverse = [False]
    _top_area_number = [1]
    _closing_kernel_size = [3]
    _is_continuous = [False]

    _cvuiframe = None

    _window_name = ''

    def __init__(self, window_name='SETTING', window_position=[0, 0]):
        self._lower_h[0], self._upper_h[0] = 0.0, 0.0
        self._lower_s[0], self._upper_s[0] = 0.0, 0.0
        self._lower_v[0], self._upper_v[0] = 0.0, 0.0
        self._is_reverse[0] = False
        self._top_area_number[0] = 1
        self._closing_kernel_size[0] = 3

        self._cvuiframe = np.zeros((390, 400, 3), np.uint8)
        self._cvuiframe[:] = (49, 52, 49)

        self._window_name = window_name
        cvui.init(self._window_name)

        self._window_position = window_position

    def update(self):
        """
        [summary]
          描画内容更新
        """
        self._cvuiframe[:] = (49, 52, 49)

        # トラックバー：H閾値指定用
        cvui.trackbar2(self._cvuiframe, 90, 30, 300, self._lower_h,
                       self._upper_h, 0, 360, 1, '%.0Lf')
        cvui.printf(self._cvuiframe, 10, 40, 0.4, 0xffffff, 'H MAX : %d',
                    self._upper_h[0])
        cvui.printf(self._cvuiframe, 10, 60, 0.4, 0xffffff, 'H MIN : %d',
                    self._lower_h[0])

        # トラックバー：S閾値指定用
        cvui.trackbar2(self._cvuiframe, 90, 100, 300, self._lower_s,
                       self._upper_s, 0, 255, 1, '%.0Lf')
        cvui.printf(self._cvuiframe, 10, 110, 0.4, 0xffffff, 'S MAX : %d',
                    self._upper_s[0])
        cvui.printf(self._cvuiframe, 10, 130, 0.4, 0xffffff, 'S MIN : %d',
                    self._lower_s[0])

        # トラックバー：V閾値指定用
        cvui.trackbar2(self._cvuiframe, 90, 170, 300, self._lower_v,
                       self._upper_v, 0, 255, 1, '%.0Lf')
        cvui.printf(self._cvuiframe, 10, 180, 0.4, 0xffffff, 'V MAX : %d',
                    self._upper_v[0])
        cvui.printf(self._cvuiframe, 10, 200, 0.4, 0xffffff, 'V MIN : %d',
                    self._lower_v[0])

        # カウンター：大きいサイズの領域をいくつ残すか
        cvui.printf(self._cvuiframe, 10, 260, 0.4, 0xffffff, 'TOP AREA NUMBER')
        cvui.counter(self._cvuiframe, 160, 255, self._top_area_number)
        self._top_area_number[0] = max(1, self._top_area_number[0])
        self._top_area_number[0] = min(100, self._top_area_number[0])

        # カウンター：クロージング処理用カーネルサイズ
        cvui.printf(self._cvuiframe, 10, 300, 0.4, 0xffffff,
                    'CLOSING KERNEL SIZE')
        cvui.counter(self._cvuiframe, 160, 295, self._closing_kernel_size, 2)
        self._closing_kernel_size[0] = max(1, self._closing_kernel_size[0])
        self._closing_kernel_size[0] = min(25, self._closing_kernel_size[0])

        # チェックボックス：マスク反転用
        cvui.checkbox(self._cvuiframe, 10, 340, 'MASK REVERSE',
                      self._is_reverse)

        # チェックボックス：連写
        cvui.checkbox(self._cvuiframe, 160, 340, 'CONTINUOUS CAPTURE',
                      self._is_continuous)

        cvui.update()

    def show(self):
        """
        [summary]
          描画
        """
        cv.imshow(self._window_name, self._cvuiframe)
        cv.moveWindow(self._window_name, self._window_position[0],
                      self._window_position[1])

    def set_hsv_param(self, h_min, h_max, s_min, s_max, v_min, v_max):
        """
        [summary]
          HSV閾値設定
        """
        self._lower_h[0], self._upper_h[0] = h_min, h_max
        self._lower_s[0], self._upper_s[0] = s_min, s_max
        self._lower_v[0], self._upper_v[0] = v_min, v_max

    def get_h_param(self):
        """
        [summary]
          H閾値取得
        """
        return self._lower_h[0], self._upper_h[0]

    def get_s_param(self):
        """
        [summary]
          S閾値取得
        """
        return self._lower_s[0], self._upper_s[0]

    def get_v_param(self):
        """
        [summary]
          V閾値取得
        """
        return self._lower_v[0], self._upper_v[0]

    def get_is_reverse_param(self):
        """
        [summary]
          マスク反転フラグ取得
        """
        return self._is_reverse[0]

    def get_top_area_number_param(self):
        """
        [summary]
          領域最大数取得
        """
        return self._top_area_number[0]

    def get_closing_kernel_size_param(self):
        """
        [summary]
          クロージングカーネルサイズ取得
        """
        return self._closing_kernel_size[0]

    def get_is_continuous_param(self):
        """
        [summary]
         連写設定取得
        """
        return self._is_continuous[0]
