# ディレクトリ centrality
グラフを扱うPythonライブラリの計算速度比較を行なう。

# ディレクトリ centrality_boost
グラフを扱うC++ライブラリboost::graphを試す。入力ファイルgraphmlを読み込めず断念。

# ディレクトリ extractor 
OpenCascadeを使いstepファイルなどのモデルファイルからグラフ構造を作成しようと試みた。結局その必要がないことがわかり放棄。

# ディレクトリ nauty_graph 
CライブラリnautyをPythonでラップしたモジュールをテストする。

# ディレクトリ nauty_sample 
## nauty_sample
Cライブラリnautyを実際に使用したサンプル集。

## nauty_graph
CライブラリnautyをC++クラスにまとめたもの。

## nauty_class
CライブラリnautyをC++クラスにまとめたものをPythonでラップする。

###ubuntu-14.04.1上でnauty_classをコンパイルする手順

#### gcc-4.9のインストール

```
$ sudo add-apt-repository ppa:ubuntu-toolchain-r/test
$ sudo apt-get update
$ sudo apt-get install gcc-4.9
$ sudo apt-get install g++-4.9
```

#### boost-pythonのインストール

```
$ sudo apt-get install libboost-python1.55-dev
```

#### nautyのインストール
https://cct-inc.backlog.jp/wiki/IMAGE_SEARCHER/graph+tool%2Fnauty%2Finstall
を参照。

#### make
最初に以下のフォルダを作成する。
- nauty_sample/lib
- nauty_sample/obj/nauty_class/nauty_class

Makefileを用意してあるのでこれを使ってmakeする。

# ディレクトリ patchy-san 
文献の実装。

# ディレクトリ receptive field(不要)
文献の実装の前準備


