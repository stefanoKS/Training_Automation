# 参考資料 / Reference materials

この研修で参照した公式ドキュメントと、追加で学ぶための資料です。
**必ず公式ドキュメントを優先** してください。ブログ記事は古いことがあります。

Official documentation used by this course, plus material for further study.
**Always prefer the official documentation**; blog posts are often out of date.

---

<!-- ne:begin doc:2312673778 -->
### नेपालीमा

यो तालिममा हेरिएका आधिकारिक कागजात र थप सिकाइका सामग्री हुन्।
**सधैं आधिकारिक कागजातलाई प्राथमिकता दिनुहोस्।** blog लेख पुरानो हुन सक्छ।
<!-- ne:end -->

## 0. この研修の解説資料 / This course's own explanations

| 内容 / Topic | 場所 / Where | 使い方 / How to use |
|---|---|---|
| 第 1〜5 日の解説 PDF / explanation PDFs for Days 1–5 | `docs/pdf/Day0N_explanation_ja_en.pdf` | ノートブックの説明をそのまま組んだ冊子。オフラインで読む / offline reading |
| 第 1 週まとめ PDF / the whole week | `docs/pdf/Week1_explanation_ja_en.pdf` | 復習と印刷 / revision and printing |
| PDF の作り直し方 / how to rebuild | `docs/pdf/README.md` | `python assets\scripts\export_explanations_pdf.py` |
| 図の出所 / figure provenance | `assets/reference_outputs/README.md` | 実測図と模式図の区別 / measured versus schematic |

PDF は Markdown から自動生成しているので、ノートブックを直せば同じコマンドで追随できます。
The PDFs are generated from the notebooks' Markdown, so correcting a notebook and re-running the
export keeps both in step. The export never executes the notebooks and never downloads a model.

---

<!-- ne:begin doc:d4294fae95 -->
### नेपालीमा

| विषय | ठाउँ | कसरी प्रयोग गर्ने |
|---|---|---|
| दिन 1–5 को व्याख्या PDF | `docs/pdf/Day0N_explanation_ja_ne.pdf` (वा पहिलेको `*_ja_en.pdf`) | नोटबुकको व्याख्या जस्ताको तस्तै बनाइएको पुस्तिका। अफलाइन पढ्न |
| हप्ता १ को सारांश PDF | `docs/pdf/Week1_explanation_ja_ne.pdf` | दोहोर्याउन र छाप्न |
| PDF फेरि बनाउने तरिका | `docs/pdf/README.md` | `python assets\scripts\export_trilingual_pdf.py` |
| चित्रको स्रोत | `assets/reference_outputs/README.md` | मापन गरिएका चित्र र योजनाबद्ध चित्रको फरक |

PDF नोटबुकको Markdown बाट स्वतः बन्छ, त्यसैले नोटबुक सुधारेपछि उही आदेशले दुवै मिलाउन सकिन्छ।
export ले नोटबुक चलाउँदैन र model डाउनलोड गर्दैन।
<!-- ne:end -->

## 1. コア（必須）/ Core (required reading)

| 内容 / Topic | リンク / Link | どこで使う / Used in |
|---|---|---|
| Python 公式チュートリアル（日本語） | <https://docs.python.org/ja/3/tutorial/> | 第2日 01・02 |
| Python 標準ライブラリ | <https://docs.python.org/ja/3/library/> | 全体 / throughout |
| Jupyter 公式 | <https://jupyter.org/> | 第0日 |
| NumPy 入門 | <https://numpy.org/doc/stable/user/absolute_beginners.html> | 第1日 02 |
| NumPy 配列の作成 | <https://numpy.org/doc/stable/user/basics.creation.html> | 第1日 02 |
| Matplotlib `imshow` | <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html> | 第1日〜第5日 |
| Matplotlib フォント設定 | <https://matplotlib.org/stable/users/explain/text/fonts.html> | 日本語表示 / Japanese text |
| Pillow リファレンス | <https://pillow.readthedocs.io/en/stable/reference/Image.html> | 第1日 02 |
| pandas 入門 | <https://pandas.pydata.org/docs/user_guide/10min.html> | 第3日〜第5日 |

---

<!-- ne:begin doc:02dde07497 -->
### नेपालीमा

पहिले यही तालिकाका लिङ्क पढ्नुहोस्। Python, Jupyter, NumPy, Matplotlib, Pillow र pandas का
आधिकारिक कागजात हुन्। जापानी अनुवाद भएका पृष्ठ पनि छन्; अङ्ग्रेजी मूलसँग मिलाएर हेर्दा राम्रो हुन्छ।
<!-- ne:end -->

## 2. OpenCV

| 内容 / Topic | リンク / Link |
|---|---|
| OpenCV-Python チュートリアル（目次） | <https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html> |
| 画像の読み込み・表示・保存 | <https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html> |
| 色空間の変換（BGR↔GRAY↔RGB） | <https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html> |
| しきい値処理 | <https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html> |
| 輪郭（contours） | <https://docs.opencv.org/4.x/d3/d05/tutorial_py_table_of_contents_contours.html> |
| カメラ校正の考え方 | <https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html> |

第2日で扱う内容は、上の 5 つでほぼすべてです。
`cv2.findContours` は **OpenCV 4 系では 2 つ**（contours, hierarchy）を返します。
3 系の記事（3 つ返す）と混同しないでください。

Day 2 is covered by the five links above. Note that `cv2.findContours` returns **two**
values in OpenCV 4 (contours, hierarchy); articles written for OpenCV 3 return three.

---

<!-- ne:begin doc:d6ee1135a2 -->
### नेपालीमा

दिन २ मा सम्हालिने कुरा माथिका ५ लिङ्कले लगभग सबै ढाक्छन्।
`cv2.findContours` ले **OpenCV 4 मा दुई** मान (contours, hierarchy) फर्काउँछ।
OpenCV 3 का लेख (तीन मान फर्काउने) सँग नमिसाउनुहोस्।
<!-- ne:end -->

## 3. PyTorch

| 内容 / Topic | リンク / Link |
|---|---|
| ローカルインストール（CPU/GPU の選び方） | <https://pytorch.org/get-started/locally/> |
| 60 分でわかる PyTorch | <https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html> |
| 学習ループの基礎 | <https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html> |
| torchvision のモデル一覧 | <https://pytorch.org/vision/stable/models.html> |

インストールページは、**OS・パッケージマネージャ・計算プラットフォーム** を
選ぶとコマンドが変わります。この研修のコマンドは Windows + pip + CPU のものです。

The install page generates a different command depending on OS, package manager and
compute platform. This course's commands are Windows + pip + CPU.

---

<!-- ne:begin doc:6fe4a10cdc -->
### नेपालीमा

दिन 4–5 मा model भित्र के हुन्छ बुझ्न यी लिङ्क उपयोगी छन्। तर यो तालिममा PyTorch को कोड
आफैं लेख्नु पर्दैन; ultralytics र anomalib ले सम्हाल्छन्।
<!-- ne:end -->

## 4. Ultralytics YOLO

| 内容 / Topic | リンク / Link |
|---|---|
| ドキュメント（全体） | <https://docs.ultralytics.com/> |
| 物体検出タスク | <https://docs.ultralytics.com/tasks/detect/> |
| Predict モード（推論） | <https://docs.ultralytics.com/modes/predict/> |
| Train モード（学習） | <https://docs.ultralytics.com/modes/train/> |
| Val モード（評価） | <https://docs.ultralytics.com/modes/val/> |
| データセット形式 | <https://docs.ultralytics.com/datasets/detect/> |
| モデル一覧 | <https://docs.ultralytics.com/models/> |
| 学習のヒント | <https://docs.ultralytics.com/guides/model-training-tips/> |

モデル名は版によって変わります。本教材は `ultralytics 8.4.211` で
**`yolo26n.pt`**（既定の nano モデル）を使用しています。古い記事の `yolov5*.pt` や
`yolov8*.pt` をそのまま使わないでください。

Model names change between releases. This course uses `ultralytics 8.4.211` with
**`yolo26n.pt`** (the default nano model). Do not copy `yolov5*.pt` / `yolov8*.pt` names from older
articles without checking.

---

<!-- ne:begin doc:2db47eeb35 -->
### नेपालीमा

दिन 3–4 मा प्रयोग हुने YOLO का आधिकारिक पृष्ठ हुन्। predict, train, val का विकल्प र
नतिजाको अर्थ यहीँबाट जाँच्नुहोस्। **Ultralytics का model र कोड AGPL-3.0** हुन्;
उत्पादनमा राख्नुअघि लाइसेन्स जाँच्नुहोस्।
<!-- ne:end -->

## 5. Anomalib

| 内容 / Topic | リンク / Link |
|---|---|
| ドキュメント（全体） | <https://anomalib.readthedocs.io/> |
| PatchCore | <https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/models/image/patchcore.html> |
| Folder データモジュール | <https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/data/image/folder.html> |
| Engine | <https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/engine.html> |
| リリースノート | <https://github.com/open-edge-platform/anomalib/releases> |

本教材は **Anomalib 2.7.0** で検証しています。
**1.x 系のサンプルコードは動きません**（`anomalib.data.Folder` など 2.x で API が変わっています）。

Verified with **Anomalib 2.7.0**. **1.x sample code does not run**: the API changed in
2.x (for example `anomalib.data.Folder`). Do not mix versions.

---

<!-- ne:begin doc:7d17b05ff9 -->
### नेपालीमा

दिन ५ को PatchCore का आधिकारिक कागजात हुन्। संस्करण 2.7.0 प्रयोग भएको छ; पुरानो संस्करणको
लेख हेर्दा API फरक हुन सक्छ भन्ने ध्यान दिनुहोस्।
<!-- ne:end -->

## 6. データセットと評価の考え方 / Datasets and evaluation

| 内容 / Topic | リンク / Link |
|---|---|
| COCO データセット（80 クラス） | <https://cocodataset.org/#explore> |
| COCO の評価指標 | <https://cocodataset.org/#detection-eval> |
| MVTec AD（異常検知の標準データセット） | <https://www.mvtec.com/company/research/datasets/mvtec-ad> |
| scikit-learn: 混同行列 | <https://scikit-learn.org/stable/modules/model_evaluation.html#confusion-matrix> |
| scikit-learn: precision / recall | <https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics> |
| PatchCore 論文 | <https://arxiv.org/abs/2106.08265> |

MVTec AD は、異常検知の研究で最もよく使われる公開データセットです。
**工業製品の画像が公開されており、ライセンスも明記** されています。第 2 週以降の参考になります。

MVTec AD is the standard public dataset for anomaly detection research, with real
industrial images and a clearly stated licence. It is a useful reference for Week 2.

---

<!-- ne:begin doc:a7ce198326 -->
### नेपालीमा

डेटासेटको बनावट, train/val/test को बाँडफाँट र मापन (precision, recall, AUROC) को अर्थ बुझ्न
यी लिङ्क हेर्नुहोस्। मापनको नाम जस्ताको तस्तै राख्नुहोस्; नेपाली अनुवाद गर्दा अर्थ नबिग्रियोस्।
<!-- ne:end -->

## 7. ライセンスの確認 / Licence checks

教材・モデル・データを使うときは、必ずライセンスを確認してください。
**教育目的の利用が、そのまま製品への利用を許可するわけではありません。**

| 対象 / Item | ライセンス / Licence | 注意 / Caution |
|---|---|---|
| Python, NumPy, Matplotlib, Pillow, pandas | PSF / BSD 系 / BSD-like | 比較的自由 / relatively permissive |
| OpenCV | Apache 2.0 | 可 / fine |
| PyTorch, torchvision | BSD 系 / BSD-like | 可 / fine |
| **Ultralytics（YOLO）** | **AGPL-3.0** | **製品組み込みは要確認** / **review before embedding in a product** |
| **COCO 事前学習の重み** | Ultralytics の配布条件に従う / per Ultralytics terms | 同上 / same as above |
| **Anomalib** | Apache 2.0 | 可 / fine |
| ImageNet 事前学習の重み（torchvision） | モデルごとに条件あり / per-model terms | 用途を確認 / check intended use |
| scikit-image のサンプル写真（`chelsea`・`camera`・`brick`） | CC0 1.0 | 出所表示は任意だが、この教材では明記 / attribution kept anyway |
| VisA データセットの概要図 | CC BY 4.0（VisA データセット） | 出所表示が必要 / attribution required |

YOLO を社内システムに組み込む場合は、**AGPL-3.0 の扱いを法務・情報システム部門に
確認** してください。この研修の範囲（学習・評価）では問題ありません。

Before embedding YOLO in an internal system, **have Legal/IT review AGPL-3.0**. Within
this course's scope (learning and evaluation) there is no issue.

---

<!-- ne:begin doc:b85373a910 -->
### नेपालीमा

सामग्री प्रयोग गर्नुअघि लाइसेन्स जाँच्नुहोस्। सिकाइमा प्रयोग गर्नु र उत्पादनमा राख्नु फरक कुरा हो।
यो तालिममा प्रयोग भएका बाह्य सामग्रीको स्रोत
[`assets/external_samples/PROVENANCE.md`](../assets/external_samples/PROVENANCE.md) मा अभिलेख छ।
<!-- ne:end -->

## 8. 実写の参考画像 / Reference photographs

レッスンの一部では、実写の参考画像を **ローカルのファイル** として表示します。表示のたびに
インターネットへ取りに行くのではなく、**設置時に一度だけ取得**します。

基本環境を有効化したコマンド プロンプトで、教材ルートから実行します（[START_HERE](../START_HERE.md)）。
Run from the course root in Command Prompt with the base environment activated (see [START_HERE](../START_HERE.md)).

```cmd
python assets\scripts\download_reference_images.py --course-root .
python assets\scripts\download_reference_images.py --course-root . --offline
```

| ファイル / File | 内容 / What it is | 出所 / Source | ライセンス / Licence |
|---|---|---|---|
| `chelsea.png` | 実写のカラー写真 / a real colour photograph | [scikit-image `chelsea`](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.chelsea)（Stefan van der Walt） | CC0 1.0 |
| `camera.png` | 実写のグレースケール写真 / a real greyscale photograph | [scikit-image `camera`](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.camera)（Lav Varshney） | CC0 1.0 |
| `brick.png` | 模様のある背景 / repeated texture | [scikit-image `brick`](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.brick)（CC0Textures を加工） | CC0 1.0 |
| `VisA_samples.png` | 産業用異常検知データの概要 / industrial anomaly-dataset overview | [amazon-science/spot-diff（VisA）](https://github.com/amazon-science/spot-diff/tree/2a692ab575001cbde74d402d897a7286086c6199) | CC BY 4.0 |

- 取得したファイルは改変せず、`assets/external_samples/open_reference/manifest.json` と
  `ATTRIBUTION.md` に出所・ライセンス・SHA-256 を記録します。
- 参考画像は授業で見るためのもので、**学習・較正・試験のデータには使いません**。
- VisA の図は実在の産業製品の写真で、この研修の塩ビ製品でも、この研修のモデルの出力でもありません。

Downloaded once at installation, unchanged, with `manifest.json` and `ATTRIBUTION.md` (source,
licence, SHA-256) stored beside them. The photographs are teaching references only and are never
used for training, calibration or test data. The VisA overview shows real industrial objects; it is
neither a photograph of this factory's PVC products nor an output of this course's models.

<!-- ne:begin doc:1aebfb55c3 -->
### नेपालीमा

सन्दर्भ फोटो लाइसेन्स भएका मूल फाइल हुन्, कारखानाको मापन नतिजा होइनन्। ती **सिकाइ, क्यालिब्रेसन वा
परीक्षणको डेटामा प्रयोग हुँदैनन्**। लिने र जाँच्ने तरिका
[START_HERE.md](../START_HERE.md) को स्टेप 7 मा छ।
<!-- ne:end -->
