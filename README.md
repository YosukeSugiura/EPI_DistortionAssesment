# EPI画像の自動歪評価

**EPIの歪評価を自動で行う**プログラムです．  
手っ取り早く実行したいなら，**# 実行方法** からご覧ください．

以下の論文を参考に作成しました．

**[原著]**  
金子瑶平ら "差分面積を用いたEPIの歪評価," 日磁医誌 第36巻3号（2016). → [[PDF Link]](https://paperzz.com/doc/5939340/原著-差分面積を用いた-epi-の歪評価)

# 概要

## 動作

歪のない画像(DICOM形式)と，それに対応した歪みのある画像(DICOM形式)を用意します．  
このプログラムは，それらを読み込んで２値化処理を行い，Geometric Distortion Ratio (GDR)を計算します．  
計算したGDRはCSVファイルに保存します．

> Geometric Distortion Ratio  
> 　歪のないファントム領域を A，歪のあるファントム領域を B とすると，以下の式でGDRを計算する．  
> 　GDR = area( ( A - B ) ∪ ( B - A ) ) / area( A )

## ファイル構成

**フォルダ内にデバッグ用のDICOM，JPGファイルが入っています．消してください．**

- `Geometric_Distortion_ratio_v1.py`  
   メインの実行ファイルです．
   
- `Distortion`  
   評価対象のDICOMファイルをこのフォルダに保存してください．  
   **シングルフレーム**のみ対応です．マルチフレーム(Enhanced DICOM)に対応してほしい場合は申し付けください．  
   また，DICOMに保存されている**画像形式によってはエラーが出ます**．エラーが出た場合には連絡ください．
   
- `Distortion_binary`  
   ２値化後の歪みのある画像(JPEG)を保存するフォルダです．
   
- `Standard`  
   基準となるDICOMファイルをこのフォルダに保存してください．  
   **シングルフレーム**のみ対応です．マルチフレーム(Enhanced DICOM)に対応してほしい場合は申し付けください．  
   また，DICOMに保存されている**画像形式によってはエラーが出ます**．エラーが出た場合には連絡ください．
   
- `Standard_binary`  
   ２値化後の歪みのない画像(JPEG)を保存するフォルダです．
   
- `GDR.csv`  
   GDRを記録したCSVファイルです．


## 要件

以下の Python と Pythonモジュール，ソフトウェアをインストールしてください．

**[Python]**  

- `Python 3.6.8`

 → Check [[How to install Python in mac]](https://github.com/YosukeSugiura/EPI_DistortionAssesment/blob/master/How2Install_Python.md)

**[Module]**  

- `numpy`
- `opencv-python`
- `pillow`
- `pydicom`
- `natsort`

 → Check [[How to install Modules]](https://github.com/YosukeSugiura/EPI_DistortionAssesment/blob/master/How2Install_Python.md)
 
**[Environment]** 

- `PyCharm`

 → Check [[How to install PyCharm]](https://github.com/YosukeSugiura/EPI_DistortionAssesment/blob/master/How2Install_Python.md)

# 実行方法

## 1. 準備

1. 上の要件に従って必要なものをインストールしてください．

2. トップページの右上にある緑色のボタン`Clone or download`→`Download ZIP`を押して，適当なフォルダにリポジトリをダウンロード&解凍してください．

3. 各フォルダ内にデバッグ用のDICOM，JPGファイルが入っています．**自身のデータで実行する場合には不要ですので消してください．**

4. 基準となるDICOMファイルと評価対象のDICOMファイルを用意し，それぞれ`Standard`フォルダと`Distortion`フォルダに入れてください．  

   **マルチフレーム(Enhanced DICOM)には対応していません．また画像形式によっては読み込みエラーが発生します．** 対応が必要な場合には申し付けください．


## 2. 実行

1. PyCahrmで`Geometric_Distortion_ratio_v1.py`を開いてください．

2. 実行してください．(通常，PyCharmのウィンドウ右上の実行ボタン(緑色の矢印)を押す or メニューバーから`Run`→`Run`，コンテクストメニューから`Geometric_Distortion_ratio_v1`を選択．)

## 3. 結果

1. ２値化前の基準画像(.jpg)を`Standard`に保存します．２値化後の基準画像(.jpg)を`Standard_binary`に保存します．

2. ２値化前の評価対象画像(.jpg)を`Distortion`に保存します．２値化後の評価対象画像(.jpg)を`Distortion_binary`に保存します．

3. GDRの結果を`GDR.csv`として保存します．


# 設定

いくつかのパラメータが制御可能です．

- **２値化を行う際のしきい値**  
  `Geometric_Distortion_ratio_v1.py`の37行目より，２値化処理のしきい値を変更できます．**0~1**の間で指定してください．
  
  ``` 
  T = 0.5 
  ```
