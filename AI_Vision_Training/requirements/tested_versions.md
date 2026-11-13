# 検証済みバージョン / Tested versions

このファイルは「**実際にインストールして、動かして確認した**」バージョンだけを記録します。
推測や「たぶん動く」は書きません。

This file records **only versions that were actually installed and executed**. No
guesses, no "should work".

---

## 1. 検証した環境 / The verification environment

| 項目 / Item | 値 / Value |
|---|---|
| OS | Windows 11 (64-bit) |
| CPU | この研修用 PC（GPU なし / no GPU） |
| GPU | なし / none — `torch.cuda.is_available()` は `False` |
| Python | **3.11.4** (CPython, 64-bit) |
| 仮想環境 / venv | `.venv` と `.venv-anomalib` の 2 つ / two environments |
| 検証日 / Date | 2026 年 11 月 / November 2026 |

Python 3.12 でも動作する可能性は高いですが、**この記録は 3.11.4 のものです。**
3.12 で使う場合は、`pandas` / `pillow` / `numpy` が新しい版を要求する点に注意してください。

Python 3.12 probably works, but **these results are for 3.11.4**. On 3.12 note that
`pandas`, `pillow` and `numpy` will resolve to newer builds.

---

## 2. `.venv`（第0〜4日）/ Base + YOLO environment (Days 0-4)

| パッケージ / Package | バージョン / Version | 用途 / Purpose |
|---|---|---|
| numpy | 2.2.6 | 数値計算 / numerics |
| matplotlib | 3.11.2 | 可視化 / plotting |
| pillow | 13.0.0 | 画像 I/O / image I/O |
| pandas | 3.1.1 | 表 / tables |
| opencv-python | **4.12.0.88** | 画像処理 / image processing |
| scikit-image | 0.26.0 | 補助的な画像処理 / auxiliary image ops |
| scipy | 1.17.1 | scikit-image の依存 / dependency |
| torch | **2.15.0** (CPU) | 深層学習 / deep learning |
| torchvision | 0.29.2 | torch 用画像変換 / transforms |
| ultralytics | **8.4.211** | YOLO |
| jupyterlab | 4.6.6 | ノートブック環境 / notebook UI |
| ipykernel | 7.4.0 | カーネル / kernel |
| nbclient | 0.11.0 | 自動実行 / automated execution |
| nbformat / nbconvert | 5.11.1 / 7.17.2 | ノートブック I/O |
| **ipywidgets** | **8.1.9** | 対話デモ / interactive demos（任意 / optional） |
| pytest | 9.2.0 | テスト / tests |

`ipywidgets` は `jupyterlab_widgets 3.0.17` と `widgetsnbextension 4.0.16` を一緒に入れます。
**どちらの環境でも同じ版** を使います。ウィジェットは「あると便利」なだけで、
無くても各ノートブックのパラメータセルで同じ実験ができます。

`ipywidgets` also pulls in `jupyterlab_widgets 3.0.17` and `widgetsnbextension 4.0.16`.
**Both course environments use the same version.** The widgets are a convenience only; the parameter
cell in each notebook runs the same experiment without them.

`torch` と `torchvision` は PyPI の Windows ホイール（CPU 版）です。
GPU を使う場合は `https://download.pytorch.org/whl/cu126` から入れ替えてください。

`torch` and `torchvision` come from the PyPI Windows wheels (CPU build). For a GPU,
install from `https://download.pytorch.org/whl/cu126` instead.

---

## 3. `.venv-anomalib`（第5日）/ Anomalib environment (Day 5)

| パッケージ / Package | バージョン / Version | 用途 / Purpose |
|---|---|---|
| anomalib | **2.7.0** | 異常検知 / anomaly detection |
| torch | **2.15.0** (CPU) | 深層学習 / deep learning |
| torchvision | 0.29.2 | 画像変換 / transforms |
| lightning | 2.6.6 | 学習ループ / training loop |
| kornia | 0.9.0 | anomalib の依存 / dependency |
| timm | 1.0.31 | バックボーン / backbones |
| torchmetrics | 1.9.0 | 指標 / metrics |
| opencv-python-**headless** | **4.12.0.88** | 画像処理 / image processing |
| ipywidgets | **8.1.9** | 対話デモ / interactive demos（任意 / optional） |
| numpy | 2.2.6 | |
| pandas | 3.1.1 | |

---

## 4. 重要な判断と、その理由 / Key decisions and why

### 4.1 なぜ環境を 2 つに分けたか / Why two environments

公式の依存関係を確認したところ、**避けられない衝突** がありました。

| パッケージ / Package | 要求する OpenCV / Requires |
|---|---|
| `anomalib==2.7.0` | `opencv-python-headless>=4.5.3.56` |
| `ultralytics==8.4.211` | `opencv-python>=4.7.0` |

2 つは別の配布物ですが、どちらも `cv2` を提供します。同じ環境に入れると
どちらかが上書きされ、OpenCV が壊れます。したがって **環境を分ける** のが正解です。

These are different distributions that both provide `cv2`. Installing both into one
environment overwrites one of them and breaks OpenCV. Separating the environments is the correct
answer. The conflict is visible in the package metadata, not a guess.

### 4.2 OpenCV を 4.12.0.88 に固定した理由 / Why OpenCV is pinned to 4.12

検証時点の最新版は `opencv-python 5.0.0.93`（メジャー新版）でした。
新しいメジャー版は API の変更を含む可能性があり、教材のコードと実機検証が
その版に対して十分ではありません。**4.12 系は安定して動作しました。**

At verification time the newest release was `opencv-python 5.0.0.93`, a brand-new major
version. A new major may change APIs, and the course code has not been verified against it.
**4.12 worked reliably**, so it is pinned.

### 4.3 torch 2.10.0 を使わなかった理由 / Why not torch 2.10.0

`anomalib 2.7.0` の CPU extras は `torch>=2.10.0` を要求します。
しかし **`torch==2.10.0` の Windows ホイールは、この検証環境で
`OSError: Error loading "...\torch\lib\c10.dll"` により import できませんでした。**

`torch==2.15.0` は同じ環境で正常に動作し、anomalib の要求（`>=2.10`）も満たします。
そこで **2.15.0** を採用しました。この事実は隠さず記録します。

`anomalib 2.7.0`'s CPU extras require `torch>=2.10.0`. However the **`torch==2.10.0`
Windows wheel could not be imported on the verification machine** (`OSError` while loading
`c10.dll`). `torch==2.15.0` imports and runs correctly there and still satisfies `>=2.10`. We
therefore use 2.15.0 and record the failure rather than hide it.

### 4.4 バックボーンを ResNet-18 にした理由 / Why ResNet-18

PatchCore の論文の既定は `wide_resnet50_2` ですが、CPU では 1 回の fit に
非常に長い時間がかかります。研修では **`resnet18` + `layers=[layer2, layer3]`** を使いました。
**アルゴリズムは同じ** で、精度はやや低くなります。

The PatchCore paper defaults to `wide_resnet50_2`, which takes far too long to fit on a
CPU. The course uses **`resnet18` with `layers=[layer2, layer3]`**: the **same algorithm**, somewhat
lower accuracy.

### 4.5 Lightning の経過表示を切った理由 / Why the Lightning progress display is off

Windows の Jupyter カーネル内で、`rich` ベースの経過表示が
`RecursionError` を起こす場合がありました。`enable_progress_bar=False` と
`enable_model_summary=False` にして、自分で開始・終了を表示しています。
**学習の計算内容は変わりません。**

Inside the Windows Jupyter kernel the `rich`-based progress display occasionally raised
`RecursionError`. We set `enable_progress_bar=False` and `enable_model_summary=False` and print our own
start/finish messages. **The computation is unchanged.**

---

## 5. 実測した結果 / Measured results

以下は、この環境で **実際に実行して得られた** 数値です。
合成データに対する値であり、**製品の検査精度ではありません**。

The values below were **actually produced** in this environment on synthetic data.
They are **not** product inspection accuracy.

### 5.1 YOLO（第4日）/ YOLO (Day 4)

`yolo26n.pt` を合成データセット（train 64 / val 16 / test 16）で
15 エポック、`imgsz=320`、`batch=8`、CPU で学習しました。

| 指標 / Metric | 試験データ / test split |
|---|---|
| precision | 0.872 |
| recall | 0.889 |
| mAP50 | 0.918 |
| mAP50-95 | 0.609 |

**学習時間 / Training time:** 数分（ハードウェア依存 / hardware dependent）。

### 5.2 PatchCore（第5日）/ PatchCore (Day 5)

`resnet18`、`coreset_sampling_ratio=0.1`、`num_neighbors=9`、CPU。

| 指標 / Metric | 値 / Value |
|---|---|
| image_AUROC | 1.000 |
| image_F1Score | 0.974 |
| pixel_AUROC | 0.984 |
| pixel_F1Score | 0.386 |

正常品スコアの最大は **0.356**、異常品スコアの最小は **0.473** で、
その間にしきい値を置けば分離できました。**合成画像では分離が容易** だということです。
実際の PVC では、これほどきれいには分かれません。

The maximum normal score was **0.356** and the minimum abnormal score **0.473**, so a
threshold in between separates them. **Synthetic images are easy**; real PVC will not separate this
cleanly.

### 5.3 YOLO と PatchCore の共通画像での比較 / Shared-set comparison

共通の 26 枚（256×256、YOLO の学習には未使用）で比較しました。

| 手法 / Method | precision | recall | 正解数 / correct | accuracy |
|---|---|---|---|---|
| YOLO | 1.000 | 0.550 | 17 / 26 | 0.654 |
| PatchCore | 1.000 | 1.000 | 26 / 26 | 1.000 |

ただし **PatchCore のしきい値は、この比較データ自身から決めている** ため、
PatchCore 側は **楽観的** です。この表だけで「PatchCore のほうが優れている」と
結論づけることはできません（第5日ノートブック03 の Part 4 に明記）。

Note that **the PatchCore threshold was derived from this very comparison set**, so its
numbers are **optimistic**. The table alone does not justify "PatchCore is better"; Day 5 Notebook 03,
Part 4 states this explicitly.

---

## 6. 既知の問題 / Known issues

| 問題 / Issue | 状態 / Status | 回避策 / Workaround |
|---|---|---|
| `torch==2.10.0` の Windows ホイールが import できない / the 2.10.0 Windows wheel fails to import | 再現 / reproduced | `torch==2.15.0` を使う / use 2.15.0 |
| Lightning の経過表示が稀に `RecursionError` / progress display raises `RecursionError` | 再現 / reproduced | `enable_progress_bar=False` |
| コンソールに日本語が化ける（cp932）/ Japanese is garbled in the console | OS 依存 / OS dependent | スクリプトのコンソール出力は英字のみ / CLI output is ASCII-only |
| YOLO の共通画像での recall が低い（0.55）/ low YOLO recall on the shared set | 想定内 / expected | 解像度と分布の違い。第4日ノートブック03 で考察 / discussed in Day 4 Notebook 03 |
| Anomalib の評価データが半分に分かれる / half of the eval data is used | 仕様 / by design | `val_split_mode="from_test"` |
