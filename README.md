# EPIの自動歪評価

歪みのない基準画像と歪みのあるEPI画像を比較し，**EPIの歪評価を自動で行う**プログラムです．  
手っ取り早く実行したいなら，**# 実行方法** からご覧ください．

以下の論文を参考に作成しました．

**[原著]**  
金子瑶平ら "差分面積を用いたEPIの歪評価," 日磁医誌 第36巻3号（2016). → [[PDF Link]](https://paperzz.com/doc/5939340/原著-差分面積を用いた-epi-の歪評価)

# 概要

## 動作

<img src="https://github.com/YosukeSugiura/EPI_DistortionAssesment/blob/master/flow.png" width="680px">  

  1. **読み込み**  
  `Standard`，`Distortion`のDICOMファイルから画像データを読み込む．

  2. **画素値の正規化**  
  それぞれの画像で，最大の画素値が`255`となるように画素値を正規化する．数式で表すと以下の通り．  
  <a href="https://www.codecogs.com/eqnedit.php?latex=\dpi{200}&space;\tiny&space;\hat{X}_{i,j}&space;=&space;255\frac{X_{i,j}}{\max&space;[&space;X_{i,j}]}" target="_blank"><img src="https://latex.codecogs.com/png.latex?\dpi{200}&space;\tiny&space;\hat{X}_{i,j}&space;=&space;255\frac{X_{i,j}}{\max&space;[&space;X_{i,j}]}" title="\tiny \hat{X}_{i,j} = 255\frac{X_{i,j}}{\max [ X_{i,j}]}" /></a>
  
  3. **画像のリサイズ**  
  歪み画像と基準画像で画素マトリックスサイズが異なる場合，画素マトリックスサイズが等しくなるように歪み画像をリサイズする．  
  
  4. **２値化**  
  基準画像と歪み画像を，Minimim法に基づき２値化する．具体的な処理は`scikit-image`の[`skimage.filters.threshold_minimum`](https://scikit-image.org/docs/dev/api/skimage.filters.html#threshold-minimum)の項を参照のこと．この手法の原著は下の通り．  
  > C. A. Glasbey, “An analysis of histogram-based thresholding algorithms,” CVGIP: Graphical Models and Image Processing, vol. 55, pp. 532-537, 1993.
  
  5. **差分画像の面積の導出**  
  ２値化された基準画像と歪み画像の差分により，差分画像を求める．
  
  6. **GDRの算出**  
  まず，FOVと画素マトリックスの値から1ピクセルあたりの面積を求める．算出式は次の通り．  
  <a href="https://www.codecogs.com/eqnedit.php?latex=\dpi{120}&space;\small&space;{\rm&space;Area&space;\&space;per&space;\&space;Pixel}&space;\&space;{\rm&space;[mm^2/pixel]}&space;=&space;\frac{{\rm&space;(FOV)^2&space;\&space;[mm^2]}}{{\rm&space;Number&space;\&space;of&space;\&space;Pixels}&space;\&space;[{\rm&space;pixels}]}" target="_blank"><img src="https://latex.codecogs.com/png.latex?\dpi{120}&space;\small&space;{\rm&space;Area&space;\&space;per&space;\&space;Pixel}&space;\&space;{\rm&space;[mm^2/pixel]}&space;=&space;\frac{{\rm&space;(FOV)^2&space;\&space;[mm^2]}}{{\rm&space;Number&space;\&space;of&space;\&space;Pixels}&space;\&space;[{\rm&space;pixels}]}" title="\small {\rm Area \ per \ Pixel} \ {\rm [mm^2/pixel]} = \frac{{\rm (FOV)^2 \ [mm^2]}}{{\rm Number \ of \ Pixels} \ [{\rm pixels}]}" /></a>  
  次に，差分画像と基準画像におけるファントム領域の面積をそれぞれ求め，それらの面積比から幾何歪み比(Geometric Distortion Ratio : GDR)を算出する．算出式は，   歪のない領域を A，歪のある領域を B とすると，以下の通りである．  
  <a href="https://www.codecogs.com/eqnedit.php?latex=\dpi{120}&space;\small&space;GDR&space;=&space;\frac{{\rm&space;area}\big[(&space;A&space;-&space;B&space;)&space;\cup&space;(&space;B&space;-&space;A&space;)\big]&space;}{&space;{\rm&space;area}[A]&space;}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\dpi{120}&space;\small&space;GDR&space;=&space;\frac{{\rm&space;area}\big[(&space;A&space;-&space;B&space;)&space;\cup&space;(&space;B&space;-&space;A&space;)\big]&space;}{&space;{\rm&space;area}[A]&space;}" title="\small GDR = \frac{{\rm area}\big[( A - B ) \cup ( B - A )\big] }{ {\rm area}[A] }" /></a>
  
  7. **保存**  
  各画像データをbmp形式で保存する．GDRデータをcsv形式で保存する．


[PDFファイル](https://github.com/YosukeSugiura/EPI_DistortionAssesment/blob/master/Details_20191225.pdf)もご参考ください．

## ファイル構成

**Distorsionフォルダ，StandardフォルダにDICOMファイルを入れてください．**

- `Geometric_Distortion_ratio_v1.py`  
   メインの実行ファイルです．

- `Difference_bmp`  
   差分画像(bmp)を保存するフォルダです．自動で生成されます．

- `Distortion`  
   評価対象のDICOMファイルをこのフォルダに保存してください．  
   **シングルフレーム**のみ対応です．マルチフレーム(Enhanced DICOM)に対応してほしい場合は申し付けください．  
   また，DICOMに保存されている**画像形式によってはエラーが出ます**．エラーが出た場合には連絡ください．
   
- `Distortion_binary_bmp`  
   ２値化後の評価対象画像(bmp)を保存するフォルダです．自動で生成されます．
   
- `Distortion_bmp`  
   ２値化前の評価対象画像(bmp)を保存するフォルダです．自動で生成されます．
   
- `Standard`  
   基準となるDICOMファイルをこのフォルダに保存してください．  
   **シングルフレーム**のみ対応です．マルチフレーム(Enhanced DICOM)に対応してほしい場合は申し付けください．  
   また，DICOMに保存されている**画像形式によってはエラーが出ます**．エラーが出た場合には連絡ください．
   
- `Standard_binary_bmp`  
   ２値化後の基準画像(bmp)を保存するフォルダです．自動で生成されます．
   
- `Standard_bmp`  
   ２値化前の基準画像(bmp)を保存するフォルダです．自動で生成されます．
   
- `GDR.csv`  
   GDRを記録したCSVファイルです．  
   下は各列の説明です．
   
| File_standard | File_distortion | Area_of_standard_phantom[mm^2] | Area_of_distortion[mm^2] | Area_of_difference[mm^2] | GDR |
|---|---|---|---|---|---|
| ファイル名(基準画像) | ファイル名(評価画像) | 基準画像のファントム面積[mm^2] | 評価画像のファントム面積[mm^2] | 差分ファントム面積[mm^2] | 幾何歪比(GDR) |

## 要件

以下の Python と Pythonモジュール，ソフトウェアをインストールしてください．

**[Python]**  

- `Python 3.6.8`  
  
  → こちらも確認 [[Python Installation in mac]](https://github.com/YosukeSugiura/EPI_DistortionAssesment/blob/master/How2Install_Python.md#1--python-installation)

**[Module]**  

- `numpy`
- `opencv-python`
- `pillow`
- `pydicom`
- `scikit-image`
- `natsort`  

  → こちらも確認 [[How to install Modules]](https://github.com/YosukeSugiura/EPI_DistortionAssesment/blob/master/How2Install_Python.md#2--python-module-installation)
 
**[Environment]** 

- `PyCharm`  
  
  → こちらも確認 [[How to install PyCharm]](https://github.com/YosukeSugiura/EPI_DistortionAssesment/blob/master/How2Install_Python.md#3--pycharm-installation)

# 実行方法

## 1. 準備

1. 上の要件に従って必要なものをインストールしてください．

2. このリポジトリのトップページの右上にある緑色のボタン`Clone or download`→`Download ZIP`を押して，適当なフォルダにリポジトリをダウンロード&解凍してください．  
   
   <img src="https://github.com/YosukeSugiura/EPI_DistortionAssesment/blob/master/download.png" width="420px">  

3. 解凍したファイル内にあるフォルダ`Distortion`，`Standard`の中にデバッグ用のDICOMファイルがあります．また，`Difference_bmp`，`Distortion_binary_bmp`，`Distortiony_bmp`，`Standard_binary_bmp`，`Standard_bmp`の中にデバッグ用のBMPファイルが入っています．**自身のデータで実行する場合にはこれらデバッグ用ファイルは不要ですので消してください．**

4. 基準DICOMファイルを`Standard`フォルダに，評価対象DICOMファイルを`Distortion`フォルダに入れてください．  

   **マルチフレーム(Enhanced DICOM)には対応していません．また画像形式によっては読み込みエラーが発生します．** 対応が必要な場合には申し付けください．


## 2. 実行

1. PyCahrmで`Geometric_Distortion_ratio_v1.py`を開いてください．  
   具体的な作業は[こちらの説明](https://github.com/YosukeSugiura/EPI_DistortionAssesment/blob/pycharm/how_to_use_pycharm.md)を見てください．

2. 実行してください．(通常，PyCharmのウィンドウ右上の実行ボタン(緑色の矢印)を押す or メニューバーから`Run`→`Run`，コンテクストメニューから`Geometric_Distortion_ratio_v1`を選択．)

## 3. 結果

1. ２値化前の基準画像(.bmp)を`Standard_bmp`に保存します．２値化後の基準画像(.bmp)を`Standard_binary_bmp`に保存します．

2. ２値化前の評価対象画像(.bmp)を`Distortion_bmp`に保存します．２値化後の評価対象画像(.bmp)を`Distortion_binary_bmp`に保存します．

3. ２枚の画像の差分画像(.bmp)を`Difference_bmp`に保存します．

4. GDRの結果を`GDR.csv`として保存します．


# 設定

いくつかのパラメータが制御可能です．

- **差分画像に輪郭線を描写する**  
  差分画像に輪郭線を描写したい場合，`Geometric_Distortion_ratio_v1_4.py`のパラメータ`boder_display`を`True`にしてください．
  `False`の場合，輪郭線を描写しません．
  ``` 
  boder_display = True
  ```
  - 赤の輪郭線 : 基準画像の輪郭線  
  - 緑の輪郭線 : 歪画像の輪郭線  
  
  <img src="https://github.com/YosukeSugiura/EPI_DistortionAssesment/blob/master/diff_with_contour.bmp" width="680px">  
