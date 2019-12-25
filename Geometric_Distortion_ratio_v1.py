from __future__ import absolute_import
from six.moves import range


# ========================
#   モジュールのインポート
# ========================

# 標準
import os
import glob

# 拡張
import cv2
import numpy as np


# ========================
#   設定
# ========================

#   処理するファイルが入っているフォルダの指定
Dir_standard = './Standard/'
Dir_distortion = './Distortion/'

#   処理後のファイルが入っているフォルダの指定
Dir_standard_save = './Standard_binary/'
Dir_distortion_save = './Distortion_binary/'

#   ２値化のしきい値 ( 0 ~ 256 )
Th = 128


# ========================
#   メイン関数
# ========================
if __name__ == '__main__':

    # ------------------------
    #   ファイル名の読み取り
    # ------------------------
    fn_std = glob.glob(Dir_standard + '*.jpg')   # 基準ファイル名
    fn_dst = glob.glob(Dir_distortion + '*.jpg')   # EPI画像ファイル名

    #   GDRの配列
    GDR = np.zeros(len(fn_std))

    # ------------------------
    #   ファイルごとの画像処理
    # ------------------------
    for i, (fn_std_, fn_dst_) in enumerate(zip(fn_std, fn_dst)):

        #   画像の読み込み
        img_std = cv2.imread(fn_std_, 0)
        img_dst = cv2.imread(fn_dst_, 0)

        #   ２値化
        binary_std = cv2.threshold(img_std, Th, 255, cv2.THRESH_BINARY)[1].astype('float32')
        binary_dst = cv2.threshold(img_dst, Th, 255, cv2.THRESH_BINARY)[1].astype('float32')

        #   画像間のずれを検出
        d, _ = cv2.phaseCorrelate(binary_dst, binary_std)

        #   ずれを補正
        # M = np.float32([[1, 0, d[0]], [0, 1, d[1]]])
        # rows, cols = binary_dst.shape
        # binary_dst = cv2.warpAffine(binary_dst, M, (cols, rows))

        #   GDRの計算
        GDR[i] = np.sum(np.abs(binary_std - binary_dst)) / np.sum(binary_std)

        #   バイナリ画像の保存
        fn_std_save = Dir_standard_save + os.path.basename(fn_std_)
        fn_dst_save = Dir_distortion_save + os.path.basename(fn_dst_)
        cv2.imwrite(fn_std_save, binary_std.astype('uint8'))
        cv2.imwrite(fn_dst_save, binary_dst.astype('uint8'))

    # ------------------------
    #   CSVファイルへの保存
    # ------------------------
    np.savetxt('GDR.csv', GDR, delimiter=',')

