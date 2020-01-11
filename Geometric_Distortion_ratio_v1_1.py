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
import pydicom as dcm
from natsort import natsorted

# ========================
#   設定
# ========================

#   DICOMファイルが入っているフォルダ
Dir_std = './Standard/'
Dir_dst = './Distortion/'

#   処理前の画像(jpg)を保存するフォルダ
Dir_std_jpg = './Standard_jpg/'
Dir_dst_jpg = './Distortion_jpg/'

#   処理前の画像(jpg)を保存するフォルダ
Dir_std_bn = './Standard_binary_jpg/'
Dir_dst_bn = './Distortion_binary_jpg/'

#   差分画像(jpg)を保存するフォルダ
Dir_dif = './Difference_jpg/'

#   ２値化のしきい値 ( 0 ~ 1 )
T = 0.1

# ========================
#   一意に決まるパラメータ
# ========================
#   ディレクトリ群
Dirs = [Dir_std_jpg, Dir_dst_jpg, Dir_std_bn, Dir_dst_bn, Dir_dif]

# ========================
#   メイン関数
# ========================
if __name__ == '__main__':

    # ------------------------
    #   ファイル名の読み取り
    # ------------------------
    fn_std = natsorted(glob.glob(Dir_std + '*.dcm'))  # 基準ファイル名
    fn_dst = natsorted(glob.glob(Dir_dst + '*.dcm'))  # EPIファイル名

    # ------------------------
    #   フォルダの作成
    # ------------------------
    for dir_ in Dirs:
        if not os.path.exists(dir_):
            os.mkdir(dir_)

    # ------------------------
    #   空配列の作成
    # ------------------------
    GDR = np.zeros(len(fn_std))  # GDRの配列
    Name_std = []  # ファイル名の配列
    Name_dst = []
    Area_std = np.zeros(len(fn_std))  # 基準画像の面積の配列
    Area_dst = np.zeros(len(fn_std))  # 評価画像の面積の配列
    Area_dif = np.zeros(len(fn_std))  # 差分画像の面積の配列

    # ------------------------
    #   ファイルごとの画像処理
    # ------------------------
    for i, (fn_std_, fn_dst_) in enumerate(zip(fn_std, fn_dst)):
        #   画像の読み込み
        ds_std = dcm.dcmread(fn_std_, force=True)
        ds_dst = dcm.dcmread(fn_dst_, force=True)
        img_std = ds_std.pixel_array
        img_dst = ds_dst.pixel_array

        #   オブジェクトの読み取り
        fov_std = ds_std[0x0018, 0x1100].value  # 基準画像のFOV
        fov_dst = ds_dst[0x0018, 0x1100].value  # 評価画像のFOV

        #   最大値で正規化
        img_std = 1 / np.max(img_std) * img_std
        img_dst = 1 / np.max(img_dst) * img_dst

        #   リサイズして歪画像を基準画像と同じ大きさに
        img_dst = cv2.resize(img_dst, img_std.shape,  interpolation = cv2.INTER_CUBIC)

        #   ２値化
        binary_std = cv2.threshold(img_std, T, 1, cv2.THRESH_BINARY)[1].astype('float32')
        binary_dst = cv2.threshold(img_dst, T, 1, cv2.THRESH_BINARY)[1].astype('float32')

        #   GDRの計算
        binary_dif = np.abs(binary_std - binary_dst)  # 差分画像
        GDR[i] = np.sum(np.abs(binary_std - binary_dst)) / np.sum(binary_std)

        #   各領域の面積を計算
        Area_per_pix_std = (img_std.shape[0] / fov_std) * (img_std.shape[1] / fov_std)  # 基準画像の1ピクセルあたりの面積[mm^2]
        Area_per_pix_dst = (img_dst.shape[0] / fov_std) * (img_dst.shape[1] / fov_std)  # 基準画像の1ピクセルあたりの面積[mm^2]
        Area_std[i] = Area_per_pix_std * np.count_nonzero(binary_std)
        Area_dst[i] = Area_per_pix_dst * np.count_nonzero(binary_dst)
        Area_dif[i] = Area_per_pix_dst * np.count_nonzero(binary_dif)  # 2枚の画像で1ピクセルあたりの面積は同じと仮定

        # ------------------------
        #   ファイルへの保存
        # ------------------------
        #   ファイル名の取得
        base_std = os.path.splitext(os.path.basename(fn_std_))[0]  # 基準画像のファイル名(拡張子なし)
        base_dst = os.path.splitext(os.path.basename(fn_dst_))[0]  # 評価画像のファイル名(拡張子なし)
        Name_std.append(base_std +'.dcm')  # csvで保存する際の名前列
        Name_dst.append(base_dst +'.dcm')  # csvで保存する際の名前列

        #   ２値化前の画像の保存
        fn_std_fl = Dir_std_jpg + base_std + '.jpg'
        fn_dst_fl = Dir_dst_jpg + base_dst + '.jpg'
        cv2.imwrite(fn_std_fl, (255 * img_std).astype('uint8'))
        cv2.imwrite(fn_dst_fl, (255 * img_dst).astype('uint8'))

        #   バイナリ画像の保存
        fn_std_bn = Dir_std_bn + base_std + '.jpg'
        fn_dst_bn = Dir_dst_bn + base_dst + '.jpg'
        cv2.imwrite(fn_std_bn, (255 * binary_std).astype('uint8'))
        cv2.imwrite(fn_dst_bn, (255 * binary_dst).astype('uint8'))

        #   差分画像の保存
        fn_dif = Dir_dif + base_std + '-' + base_dst + '.jpg'
        cv2.imwrite(fn_dif, (255 * binary_dif).astype('uint8'))

    # ------------------------
    #   CSVファイルへの保存
    # ------------------------
    Data = np.vstack([Name_std, Name_dst, Area_std, Area_dst, Area_dif, GDR]).T
    Data = np.vstack([['File_standard', 'File_distortion', 'Area_of_standard_phantom [mm^2]', 'Area_of_distortion_phantom [mm^2]',
                       'Area_of_difference [mm^2]', 'GDR'], Data])
    np.savetxt('GDR.csv', Data, delimiter=',', fmt="%s")
