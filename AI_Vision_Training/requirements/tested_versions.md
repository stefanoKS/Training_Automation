# 検証済みバージョン / Tested versions

このファイルは「**実際にインストールして、動かして確認した**」バージョンだけを記録します。
推測や「たぶん動く」は書きません。

This file records **only versions that were actually installed and executed**. No
guesses, no "should work".

---

<!-- ne:begin doc:2289ef6651 -->
### नेपालीमा

यो फाइलले "**वास्तवमा install गरेर, चलाएर जाँचिएका**" संस्करण मात्र अभिलेख गर्छ।
अनुमान वा "चल्ला जस्तो छ" लेखिँदैन।
<!-- ne:end -->

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

<!-- ne:begin doc:bd9be6f545 -->
### नेपालीमा

| विषय | मान |
|---|---|
| OS | Windows 11 (64-bit) |
| CPU | यो तालिमको PC (GPU छैन) |
| GPU | छैन — `torch.cuda.is_available()` ले `False` दिन्छ |
| Python | **3.11.4** (CPython, 64-bit) |
| virtual environment | `.venv` र `.venv-anomalib` गरी २ वटा |
| जाँचिएको मिति | 2026 नोभेम्बर |

Python 3.12 मा पनि चल्ने सम्भावना उच्च छ, तर **यो अभिलेख 3.11.4 को हो।**
3.12 प्रयोग गर्दा `pandas`, `pillow`, `numpy` ले नयाँ संस्करण माग्ने कुरामा ध्यान दिनुहोस्।
<!-- ne:end -->

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

<!-- ne:begin doc:5a7721fc02 -->
### नेपालीमा

माथिको तालिकामा दिन 0–4 मा प्रयोग हुने package र तिनको संस्करण छ। संस्करण जस्ताको तस्तै राखिएको छ,
किनभने यही संस्करणमा नतिजा नापिएको हो।

`ipywidgets` सँगै `jupyterlab_widgets 3.0.17` र `widgetsnbextension 4.0.16` पनि पर्छन्।
**दुवै वातावरणमा उही संस्करण** प्रयोग हुन्छ। widget "भए राम्रो" मात्र हो; नभए पनि प्रत्येक
नोटबुकको parameter सेलले उही प्रयोग गर्न दिन्छ।

`torch` र `torchvision` PyPI को Windows wheel (CPU संस्करण) हुन्।
GPU प्रयोग गर्ने भए `https://download.pytorch.org/whl/cu126` बाट बदल्नुहोस्।
<!-- ne:end -->

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

<!-- ne:begin doc:7dbe52e927 -->
### नेपालीमा

दिन ५ मा प्रयोग हुने वातावरणको package र संस्करण माथिको तालिकामा छ। यहाँ OpenCV को
**headless** संस्करण प्रयोग भएको छ; यही कारण वातावरण दुईवटा बनाइएको हो।
<!-- ne:end -->

## 4. 重要な判断と、その理由 / Key decisions and why

<!-- ne:begin doc:3fb8e163b8 -->
### नेपालीमा

तलका निर्णय अनुमानले होइन, मापन वा आधिकारिक dependency जानकारीबाट गरिएका हुन्।
<!-- ne:end -->

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

<!-- ne:begin doc:0f07feafa6 -->
### नेपालीमा

आधिकारिक dependency जाँच्दा **छल्न नसकिने द्वन्द्व** भेटियो।

| package | माग्ने OpenCV |
|---|---|
| `anomalib==2.7.0` | `opencv-python-headless>=4.5.3.56` |
| `ultralytics==8.4.211` | `opencv-python>=4.7.0` |

दुवै छुट्टै package हुन् तर दुवैले `cv2` दिन्छन्। एउटै वातावरणमा राख्दा एउटाले अर्कोलाई ओभरराइट
गरेर OpenCV बिग्रन्छ। त्यसैले **वातावरण छुट्याउनु** नै सही उत्तर हो।
<!-- ne:end -->

### 4.2 OpenCV を 4.12.0.88 に固定した理由 / Why OpenCV is pinned to 4.12

検証時点の最新版は `opencv-python 5.0.0.93`（メジャー新版）でした。
新しいメジャー版は API の変更を含む可能性があり、教材のコードと実機検証が
その版に対して十分ではありません。**4.12 系は安定して動作しました。**

At verification time the newest release was `opencv-python 5.0.0.93`, a brand-new major
version. A new major may change APIs, and the course code has not been verified against it.
**4.12 worked reliably**, so it is pinned.

<!-- ne:begin doc:e63c9200b5 -->
### नेपालीमा

जाँच गर्दाको सबैभन्दा नयाँ संस्करण `opencv-python 5.0.0.93` (नयाँ major) थियो।
नयाँ major ले API बदल्न सक्छ र तालिमको कोड त्यसमा जाँचिएको छैन। **4.12 ले स्थिर रूपमा काम गर्‍यो**,
त्यसैले त्यही राखिएको हो।
<!-- ne:end -->

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

<!-- ne:begin doc:50fa972cfc -->
### नेपालीमा

`anomalib 2.7.0` को CPU extras ले `torch>=2.10.0` माग्छ।
तर **`torch==2.10.0` को Windows wheel यो वातावरणमा
`OSError: Error loading "...\torch\lib\c10.dll"` का कारण import हुन सकेन।**

`torch==2.15.0` उही वातावरणमा ठीक चल्यो र anomalib को माग (`>=2.10`) पनि पूरा गर्छ।
त्यसैले **2.15.0** राखियो। यो तथ्य लुकाइएको छैन, अभिलेख गरिएको छ।
<!-- ne:end -->

### 4.4 バックボーンを ResNet-18 にした理由 / Why ResNet-18

PatchCore の論文の既定は `wide_resnet50_2` ですが、CPU では 1 回の fit に
非常に長い時間がかかります。研修では **`resnet18` + `layers=[layer2, layer3]`** を使いました。
**アルゴリズムは同じ** で、精度はやや低くなります。

The PatchCore paper defaults to `wide_resnet50_2`, which takes far too long to fit on a
CPU. The course uses **`resnet18` with `layers=[layer2, layer3]`**: the **same algorithm**, somewhat
lower accuracy.

<!-- ne:begin doc:de865f17a1 -->
### नेपालीमा

PatchCore को कागजातको पूर्वनिर्धारित backbone `wide_resnet50_2` हो, तर CPU मा एक पटक fit गर्न
धेरै लामो समय लाग्छ। तालिममा **`resnet18` + `layers=[layer2, layer3]`** प्रयोग गरियो।
**एल्गोरिदम उही** हो, शुद्धता अलिकति कम हुन्छ।
<!-- ne:end -->

### 4.5 Lightning の経過表示を切った理由 / Why the Lightning progress display is off

Windows の Jupyter カーネル内で、`rich` ベースの経過表示が
`RecursionError` を起こす場合がありました。`enable_progress_bar=False` と
`enable_model_summary=False` にして、自分で開始・終了を表示しています。
**学習の計算内容は変わりません。**

Inside the Windows Jupyter kernel the `rich`-based progress display occasionally raised
`RecursionError`. We set `enable_progress_bar=False` and `enable_model_summary=False` and print our own
start/finish messages. **The computation is unchanged.**

---

<!-- ne:begin doc:b817e527e2 -->
### नेपालीमा

Windows को Jupyter kernel भित्र `rich` मा आधारित प्रगति देखाइले कहिलेकाहीँ
`RecursionError` दिन्थ्यो। `enable_progress_bar=False` र
`enable_model_summary=False` राखेर सुरु र अन्त्य आफैं देखाइएको छ।
**सिकाइको हिसाबमा कुनै परिवर्तन छैन।**
<!-- ne:end -->

## 5. 実測した結果 / Measured results

以下は、この環境で **実際に実行して得られた** 数値です。
合成データに対する値であり、**製品の検査精度ではありません**。

The values below were **actually produced** in this environment on synthetic data.
They are **not** product inspection accuracy.

<!-- ne:begin doc:ac5a026591 -->
### नेपालीमा

तलका सङ्ख्या यो वातावरणमा **वास्तवमा चलाएर पाइएका** हुन्।
ती कृत्रिम डेटाका मान हुन् र **उत्पादन निरीक्षणको शुद्धता होइनन्**।
<!-- ne:end -->

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

<!-- ne:begin doc:31b3e29b1a -->
### नेपालीमा

`yolo26n.pt` लाई कृत्रिम डेटासेट (train 64 / val 16 / test 16) मा 15 epoch, `imgsz=320`,
`batch=8`, CPU मा सिकाइएको। मापन माथिको तालिकामा छ (precision, recall, mAP50, mAP50-95)।
**सिकाइ समय:** केही मिनेट (hardware मा निर्भर)।
<!-- ne:end -->

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
実際の塩ビでは、これほどきれいには分かれません。

The maximum normal score was **0.356** and the minimum abnormal score **0.473**, so a
threshold in between separates them. **Synthetic images are easy**; real PVC will not separate this
cleanly.

<!-- ne:begin doc:a14446100a -->
### नेपालीमा

`resnet18`, `coreset_sampling_ratio=0.1`, `num_neighbors=9`, CPU मा चलाइयो।
मापन माथिको तालिकामा छ (image_AUROC, image_F1Score, pixel_AUROC, pixel_F1Score)।

सामान्य उत्पादनको अधिकतम score **0.356** र असामान्यको न्यूनतम **0.473** थियो; बीचमा threshold
राख्दा छुट्याउन सकिन्थ्यो। **कृत्रिम चित्रमा छुट्याउन सजिलो** हुन्छ भन्ने यही हो।
वास्तविक PVC मा यति सफा छुट्याउँदैन।
<!-- ne:end -->

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

<!-- ne:begin doc:59274e4625 -->
### नेपालीमा

साझा 26 चित्र (256×256, YOLO को सिकाइमा नपरेका) मा तुलना गरियो; नतिजा माथिको तालिकामा छ।

तर **PatchCore को threshold यही तुलना डेटाबाटै तय गरिएको** हुनाले PatchCore पक्ष
**आशावादी** छ। यो तालिका मात्र हेरेर "PatchCore राम्रो" भन्ने निष्कर्ष निकाल्न मिल्दैन
(दिन ५ नोटबुक ०३ को Part 4 मा स्पष्ट लेखिएको छ)।
<!-- ne:end -->

## 6. 既知の問題 / Known issues

| 問題 / Issue | 状態 / Status | 回避策 / Workaround |
|---|---|---|
| `torch==2.10.0` の Windows ホイールが import できない / the 2.10.0 Windows wheel fails to import | 再現 / reproduced | `torch==2.15.0` を使う / use 2.15.0 |
| Lightning の経過表示が稀に `RecursionError` / progress display raises `RecursionError` | 再現 / reproduced | `enable_progress_bar=False` |
| コンソールに日本語が化ける（cp932）/ Japanese is garbled in the console | OS 依存 / OS dependent | スクリプトのコンソール出力は英字のみ / CLI output is ASCII-only |
| YOLO の共通画像での recall が低い（0.55）/ low YOLO recall on the shared set | 想定内 / expected | 解像度と分布の違い。第4日ノートブック03 で考察 / discussed in Day 4 Notebook 03 |
| Anomalib の評価データが半分に分かれる / half of the eval data is used | 仕様 / by design | `val_split_mode="from_test"` |

<!-- ne:begin doc:b08ee06b39 -->
### नेपालीमा

| समस्या | अवस्था | बाटो |
|---|---|---|
| `torch==2.10.0` को Windows wheel import हुँदैन | दोहोरियो | `torch==2.15.0` प्रयोग गर्ने |
| Lightning को प्रगति देखाइले कहिलेकाहीँ `RecursionError` दिन्छ | दोहोरियो | `enable_progress_bar=False` |
| console मा जापानी अक्षर बिग्रन्छ (cp932) | OS मा निर्भर | स्क्रिप्टको console output अङ्ग्रेजीमा मात्र |
| साझा चित्रमा YOLO को recall कम (0.55) | अपेक्षित | resolution र वितरणको फरक। दिन ४ नोटबुक ०३ मा छलफल |
| Anomalib को मूल्याङ्कन डेटा आधा बाँडिन्छ | डिजाइनअनुसार | `val_split_mode="from_test"` |
<!-- ne:end -->
