#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
[summary]
  HSV値によるマスク処理プログラム
[description]
  -
"""

import os
import argparse

import numpy as np
import cv2 as cv

from gui.frame_gui import FrameGui
from gui.debug_gui import DebugGui
from gui.setting_gui import SettingGui


def get_args():
    """
    [summary]
        引数解析
    Parameters
    ----------
    None
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--device",
                        type=int,
                        help='camera device number',
                        default=0)
    parser.add_argument("--width",
                        help='capture width',
                        type=int,
                        default=1280)
    parser.add_argument("--height",
                        help='capture height',
                        type=int,
                        default=720)
    parser.add_argument("--waittime",
                        help='waitkey time(ms)',
                        type=int,
                        default=10)
    parser.add_argument("--pos_offset",
                        help='window position offset',
                        type=int,
                        default=50)

    args = parser.parse_args()

    return args


def main():
    """
    [summary]
        main()
    Parameters
    ----------
    None
    """
    # 引数解析 #################################################################
    args = get_args()
    cap_device = args.device
    cap_width = args.width
    cap_height = args.height
    waittime = args.waittime
    pos_offset = args.pos_offset

    # カメラ準備 ###############################################################
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # 画像保存先準備 ###########################################################
    path_save_image = os.path.join('capture', 'image')
    path_save_mask = os.path.join('capture', 'mask')
    path_save_cutoutimage = os.path.join('capture', 'maskimage')
    os.makedirs(path_save_image, exist_ok=True)
    os.makedirs(path_save_mask, exist_ok=True)
    os.makedirs(path_save_cutoutimage, exist_ok=True)

    # 画像ファイル名用番号
    capture_count = len(os.listdir(path_save_image))

    # GUI準備 #################################################################
    setting_gui = SettingGui(window_position=[pos_offset, pos_offset])
    debug_gui = DebugGui(window_position=[pos_offset, pos_offset + 500])
    frame_gui = FrameGui(window_position=[pos_offset + 430, pos_offset])

    # HSVマスク 上限下限保持用変数
    lower_hsv = [0, 0, 0]
    upper_hsv = [0, 0, 0]

    while True:
        # カメラキャプチャ #####################################################
        ret, frame = cap.read()
        if not ret:
            continue
        resize_frame = cv.resize(frame,
                                 (int(cap_width / 2), int(cap_height / 2)))
        hsv_frame = cv.cvtColor(resize_frame, cv.COLOR_BGR2HSV)

        # マウス左クリック時にHSV初期値を設定 ###################################
        click_point = frame_gui.get_mouse_l_click_point()
        if click_point is not None:
            lower_hsv, upper_hsv = set_hsv_point_value(click_point, hsv_frame)

            # SETTING GUIにHSV初期値を設定
            setting_gui.set_hsv_param(lower_hsv[0] * 2, upper_hsv[0] * 2,
                                      lower_hsv[1], upper_hsv[1], lower_hsv[2],
                                      upper_hsv[2])

        # SETTING GUIから設定値を取得 ########################################
        lower_h, upper_h = setting_gui.get_h_param()
        lower_s, upper_s = setting_gui.get_s_param()
        lower_v, upper_v = setting_gui.get_v_param()
        closing_kernel_size = setting_gui.get_closing_kernel_size_param()
        top_area_number = setting_gui.get_top_area_number_param()
        is_reverse = setting_gui.get_is_reverse_param()

        # HSV閾値をOpenCV処理用に格納 ※Hの有効範囲は通常0~360だがOpenCVでは0～180
        lower_hsv = [int(lower_h / 2), int(lower_s), int(lower_v)]
        upper_hsv = [int(upper_h / 2), int(upper_s), int(upper_v)]

        # HSV値でのマスクを取得
        mask = process_hsv_extract(hsv_frame, lower_hsv, upper_hsv,
                                   closing_kernel_size, top_area_number,
                                   is_reverse)

        # HSVマスクでの切り抜き画像生成
        cutout_image = cv.bitwise_and(resize_frame, mask)

        # GUI描画更新
        setting_gui.update()
        frame_gui.update(resize_frame)
        debug_gui.update(mask, cutout_image)
        setting_gui.show()
        debug_gui.show()
        frame_gui.show()

        # キー入力(ESC:プログラム終了、C:キャプチャ) ############################
        # ※SETTING GUIの「CONTINUOUS CAPTURE」を有効時には
        #   C押下に関わらず、連続キャプチャを実施
        key = cv.waitKey(waittime)
        is_continuous = setting_gui.get_is_continuous_param()
        if key == 99 or is_continuous:  # C
            path_image_file = os.path.join(path_save_image,
                                           '{:05}.png'.format(capture_count))
            cv.imwrite(path_image_file, frame)

            path_mask_file = os.path.join(path_save_mask,
                                          '{:05}.png'.format(capture_count))
            mask = cv.resize(mask, (frame.shape[1], frame.shape[0]))
            cv.imwrite(path_mask_file, mask)

            path_mask_file = os.path.join(path_save_cutoutimage,
                                          '{:05}.png'.format(capture_count))
            cutout_image = cv.bitwise_and(frame, mask)
            cv.imwrite(path_mask_file, cutout_image)

            print('capture:', '{:05}.png'.format(capture_count))

            capture_count += 1
        if key == 27:  # ESC
            break


def set_hsv_point_value(point, hsv_frame):
    """
    [summary]
        指定箇所のHSV値からHSVマスク用の閾値を取得
    Parameters
    ----------
    point : [[int, int]]
        [description]
            指定箇所
    hsv_frame : [frame]
        [description]
            HSV変換後画像
    """
    lower_hsv = [0, 0, 0]
    upper_hsv = [0, 0, 0]

    hsv_value = hsv_frame[point[1], point[0]]

    lower_hsv[0] = max(0, int(hsv_value[0] - 10))
    lower_hsv[1] = max(0, int(hsv_value[1] - 30))
    lower_hsv[2] = max(0, int(hsv_value[2] - 30))
    upper_hsv[0] = min(180, int(hsv_value[0] + 10))
    upper_hsv[1] = min(255, int(hsv_value[1] + 90))
    upper_hsv[2] = min(255, int(hsv_value[2] + 90))

    return lower_hsv, upper_hsv


def process_hsv_extract(hsv_frame, lower_hsv, upper_hsv, closing_kernel_size,
                        top_area_number, is_reverse):
    """
    [summary]
        指定箇所のHSV値からHSVマスク用の閾値を取得
    Parameters
    ----------
    hsv_frame : [frame]
        [description]
            HSV変換後画像
    lower_hsv : [[int, int, int]]
        [description]
            H, S, Vの下限値
    upper_hsv : [[int, int, int]]
        [description]
            H, S, Vの上限値
    closing_kernel_size : [int]
        [description]
            クロージング処理時のカーネルサイズ
    top_area_number : [int]
        [description]
            マスク領域について、大きいサイズの領域を上位いくつ表示するか
    is_reverse : [bool]
        [description]
            マスク結果の反転有無
    """
    # HSVマスク画像生成
    mask_hsv = cv.inRange(hsv_frame, np.array(lower_hsv), np.array(upper_hsv))

    # クロージング処理による粒ノイズ除去
    kernel = np.ones((closing_kernel_size, closing_kernel_size), np.uint8)
    mask_hsv = cv.morphologyEx(mask_hsv, cv.MORPH_CLOSE, kernel)

    # 大きい領域の上位のみマスク画像として描画する
    mask = np.zeros(hsv_frame.shape, np.uint8)
    contours = cv.findContours(mask_hsv, cv.RETR_EXTERNAL,
                               cv.CHAIN_APPROX_SIMPLE)[0]
    contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)
    for i, controur in enumerate(contours):
        if i < top_area_number:
            mask = cv.drawContours(mask, [controur],
                                   -1,
                                   color=(255, 255, 255),
                                   thickness=-1)

    # マスク反転
    if is_reverse:
        mask = cv.bitwise_not(mask)

    return mask


if __name__ == '__main__':
    main()
