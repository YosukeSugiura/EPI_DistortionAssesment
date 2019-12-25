# EPI画像の自動歪評価

**EPIの歪評価を自動で行う**プログラムを実装しました．  
以下の論文を参考に作成しました．

**[原著]**  
金子瑶平ら "差分面積を用いたEPIの歪評価," 日磁医誌 第36巻3号（2016). → [[PDF Link]](https://paperzz.com/doc/5939340/原著-差分面積を用いた-epi-の歪評価)

# 動作

歪のない画像( A )と，それに対応した歪みのある画像( B )を用意します．  
それらに２値化処理を行い，Geometric Distortion Ratio (GDR)を計算します．  
計算したGDRはCSVファイルに保存します．

> Geometric Distortion Ratio  
> 　歪のないファントム領域を A，歪のあるファントム領域を B とすると，以下の式でGDRを計算する．  
> 　GDR = area( A - B ) ∪ ( B - A ) / area( A )

# 要件

以下の Python と Pythonモジュール，ソフトウェアをインストールしてください．

**[Python]**  

- `Python 3.6.8`

 → Check [[How to install Python in mac]]()

**[Module]**  

- `numpy`
- `opencv-python`
- `pydicom`

 → Check [[How to install Modules]]()
 
**[Environment]** 

- `PyCharm`

 → Check [[How to install PyCharm]]()

# 準備

1. 上の要件に従って必要なものをインストールしてください．

2. トップページの右上にある緑色のボタン`Clone or download`→`Download ZIP`を押して，適当なフォルダにリポジトリをダウンロード&解凍してください．


# 実行と結果

1. PyCahrmで`Geometric_Distortion_ratio_v1.py`を開いてください．

2. 実行してください．(通常，右上の実行ボタンを押す or メニューバーから`Run`→`Run`，コンテクストメニューから`Geometric_Distortion_ratio_v1`を選択．)

3. 実行結果が
