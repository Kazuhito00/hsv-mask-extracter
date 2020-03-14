# hsv-mask-extracter
 hsv-mask-extracterはHSV値を閾値にしたマスク画像を生成するプログラムです。

## 動作例(Youtube)
[![](https://img.youtube.com/vi/R-w-efaOKbY/0.jpg)](https://www.youtube.com/watch?v=R-w-efaOKbY)

# Requirement
 
* OpenCV 3.4.2(or later)
 
# Installation
 
ディレクトリを丸ごとコピーして実行してください。
 
# Usage
 
サンプルの実行方法は以下です。
 
```bash
python hsv_mask_extracter.py
```

以下のコマンドラインオプションがあります。

--device：OpenCVのVideoCapture()で開くカメラデバイスorファイル

--width：カメラキャプチャサイズ(幅)

--height：カメラキャプチャサイズ(高さ)

--waittime：処理フレーム間スリープ時間

「CAPTURE FRAME」ウィンドウの任意のポイントをマウス左クリックすることで、ポイント箇所のHSV値を元にマスク画像を生成します。

また、「C」を押すことで、入力画像、マスク画像、切り抜き画像を保存します。

・capture/image

・capture/mask

・capture/maskimage
 
# Setting(GUI)

![2020-03-14](https://user-images.githubusercontent.com/37477845/76676149-d2746580-6603-11ea-8c96-808e036dc2e2.png)

3本のトラックバーでH、S、Vの閾値を指定できます。

HSV閾値は、「CAPTURE FRAME」ウィンドウの任意のポイントをマウス左クリックした際に初期値がセットされます。

その他は以下の指定地です。

TOP AREA NUMBER：マスクとして採用する領域の上位数(サイズ順)

CLOSING KERNEL SIZE：クロージング処理のカーネルサイズ(N×N)

MASK REVERSE：生成したマスク画像を反転

CONTINUOUS CAPTURE：



# Author
高橋かずひと(https://twitter.com/KzhtTkhs)
 
# License 
cvoverlayimg is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).

# cvui License

設定用のGUIにはcvuiを改造したものを利用しています。

The original part of cvui is distributed under the MIT license.

I pay tribute to his wonderful work.

Copyright (c) 2016 Fernando Bevilacqua. Licensed under the [MIT license](LICENSE.md).

