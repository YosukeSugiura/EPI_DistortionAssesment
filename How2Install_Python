# How to install Python

ここでは Python と開発環境である PyCharm の導入方法を説明します．  
ついでにおすすめの Python モジュールを紹介しておきます．

This repository explains how to install Python and development environment (PyCharm) in Windows PC.  
This is for **Sharing Knowledge in [Shimamura Laboratory](http://www.sie.ics.saitama-u.ac.jp)**.

# Procedure of Installation

We introfuce installation by `pip`, it's not `Anaconda`.
Please follow the below procedure.

> **I strongly recommend to use pip instead of Anaconda !!**

## 1.  Python Installation

Firstly, install Python.

  1. Download `.exe` of Python from [official site](https://www.python.org/downloads/windows/).  **Recommended version is Python 3.6 !**
  If Windows 10, please click `Windows x86-64 executable installer` in that page.  
  <img src="https://github.com/Shimamura-Lab-SU/How-to-setting-Python/blob/master/python_page.jpg" width="500px">
  
  2. Execute downloaded `.exe` file.  
  When wondow is opened, **Must turn on check box of `Add Python 3.X to Path`!** And click `Install Now`.  
  <img src="https://github.com/Shimamura-Lab-SU/How-to-setting-Python/blob/master/python_path.jpg" width="500px">
  
## 2.  PyCharm Installation

Next, install PyCharm that is an strong development environment.

  1.  Donload **Community version of Pycharm** from [https://www.jetbrains.com/pycharm/download/#section=windows](https://www.jetbrains.com/pycharm/download/#section=windows). 
  
  2. Execute it and click `Next`.
  
## 3.  PyCharm Setting

   The following is almost the same as [here](https://akiyoko.hatenablog.jp/entry/2017/03/10/082912).

### 1. Memory Release Indicator
 To enable to release memory usage, show memory indicator.  
From `[File]` > `[Settings]` > `[Appearance & Behavior]` > `[Appearance]` , turn on `Show memory indicator`.    
<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/a/akiyoko/20170310/20170310003158.png" width="700px">  
@akiyoko blog : PyCharm のオレオレ最強設定

Then you can **release memory by clicking memory indicator** on the lower right corner like this.  
<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/a/akiyoko/20170310/20170310003752.png" width="300px">  
@akiyoko blog : PyCharm のオレオレ最強設定

#### 2. Heap Memory Allocation

From `[Help]` > `[Edit Custom VM Options]`, 
you can open `pycharm64` file.

From 
```
# custom PyCharm VM options

-Xms128m
-Xmx750m
-XX:ReservedCodeCacheSize=240m
-XX:+UseCompressedOops
```
you can increase the upper-bound of memory usage by 
```
# custom PyCharm VM options

-Xms2000m
-Xmx4000m
-XX:ReservedCodeCacheSize=240m
-XX:+UseCompressedOops
```
 > Of cause, memory limit is as you like, but must be set to match your PC environment!

## 4.  Python Module Installation

The following modules are my recommendations to install.
Basically, you can install & update them by command prompt. Please command 
```
pip install (***module name***) --upgrade 
```

### [Fundamentals]

Firstly, **Please update `pip`** in command prompt by the following command :
  ```
  pip install pip --upgrade
  ```
- **numpy**  
  many usable calculation functions
- **scipy**  
  file loader, writer, signal processing tools
- **scikit-learn**  
  powerful machine learning tools
- **matplotlib**  
  graph tools
- **numba**  
   for @jit compile


### [Audio]

- **soundfile**  
  wav IO tools

- **pyaudio**  
  real-time audio processor

### [Image]
- **Pillow**  
  image IO tools
