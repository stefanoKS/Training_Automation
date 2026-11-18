<!--
Nepali anuwad / Nepali translation source for
requirements/tested_versions.md

Version numbers, package names and measured values are copied unchanged.
-->
# tested_versions — Nepali anuwad

<!-- ne-doc: requirements/tested_versions.md -->

<!-- ne-section: Tested versions -->
### Nepali ma

yo filele "**bastabama install garera, chalaer janchieka**" sanskaran matra abhilekh garchha.
anuman wa "challa jasto chha" lekhindain.

<!-- ne-section: ## 1. 検証した環境 -->
### Nepali ma

| bishay | maan |
|---|---|
| OS | Windows 11 (64-bit) |
| CPU | yo talimko PC (GPU chhaina) |
| GPU | chhaina — `torch.cuda.is_available()` le `False` dinchha |
| Python | **3.11.4** (CPython, 64-bit) |
| virtual environment | `.venv` ra `.venv-anomalib` gari 2 bata |
| janchieko miti | 2026 nobhembar |

Python 3.12 ma pani chalne sambhabana uchcha chha, tar **yo abhilekh 3.11.4 ko ho.**
3.12 prayog garda `pandas`, `pillow`, `numpy` le nayan sanskaran magne kura ma dhyan dinuhos.

<!-- ne-section: ## 2. `.venv` -->
### Nepali ma

mathiko talika ma din 0–4 ma prayog hune package ra tinako sanskaran chha. sanskaran jastako tastai rakhieko chha,
kinabhane yahi sanskaranama natija napieko ho.

`ipywidgets` sangai `jupyterlab_widgets 3.0.17` ra `widgetsnbextension 4.0.16` pani parchhan.
**dubai batabaran ma uhi sanskaran** prayog hunchha. widget "bhae ramro" matra ho; nabhae pani pratyek
notebookko parameter cellle uhi prayog garna dinchha.

`torch` ra `torchvision` PyPI ko Windows wheel (CPU sanskaran) hun.
GPU prayog garne bhae `https://download.pytorch.org/whl/cu126` baat badalnuhos.

<!-- ne-section: ## 3. `.venv-anomalib` -->
### Nepali ma

din 5 ma prayog hune batabaranko package ra sanskaran mathiko talika ma chha. yahan OpenCV ko
**headless** sanskaran prayog bhaeko chha; yahi karan batabaran duibata banaiyeko ho.

<!-- ne-section: ## 4. 重要な判断と、その理由 -->
### Nepali ma

talaka nirnaya anumanle hoina, maapan wa adhikarik dependency jankari baat garieka hun.

<!-- ne-section: ### 4.1 -->
### Nepali ma

adhikarik dependency janchda **chhaln nasakine dbandb** bhetiyo.

| package | magne OpenCV |
|---|---|
| `anomalib==2.7.0` | `opencv-python-headless>=4.5.3.56` |
| `ultralytics==8.4.211` | `opencv-python>=4.7.0` |

dubai chhuttai package hun tar dubaile `cv2` dinchhan. eutai batabaran ma rakhda eutale arkolai obhararait
garera OpenCV bigranchha. tyasaile **batabaran chhutyaunu** nai sahi uttar ho.

<!-- ne-section: ### 4.2 -->
### Nepali ma

jaanch gardako sabaibhanda nayan sanskaran `opencv-python 5.0.0.93` (nayan major) thiyo.
nayan major le API badalna sakchha ra talimko kod tyas ma janchieko chhaina. **4.12 le sthir rupama kaam gar‍yo**,
tyasaile tyahi rakhieko ho.

<!-- ne-section: ### 4.3 -->
### Nepali ma

`anomalib 2.7.0` ko CPU extras le `torch>=2.10.0` magchha.
tar **`torch==2.10.0` ko Windows wheel yo batabaran ma
`OSError: Error loading "...\torch\lib\c10.dll"` ka karan import huna saken.**

`torch==2.15.0` uhi batabaran ma thik chalyo ra anomalib ko mag (`>=2.10`) pani pura garchha.
tyasaile **2.15.0** rakhiyo. yo tathy lukaieko chhaina, abhilekh garieko chha.

<!-- ne-section: ### 4.4 -->
### Nepali ma

PatchCore ko kagajatako purbanirdharit backbone `wide_resnet50_2` ho, tar CPU ma ek patak fit garna
dherai lamo samay lagchha. talim ma **`resnet18` + `layers=[layer2, layer3]`** prayog gariyo.
**elgoridam uhi** ho, shuddhata alikati kam hunchha.

<!-- ne-section: ### 4.5 -->
### Nepali ma

Windows ko Jupyter kernel bhitr `rich` ma adharit pragati dekhaile kahilekahin
`RecursionError` dinthyo. `enable_progress_bar=False` ra
`enable_model_summary=False` rakher suru ra antya aphain dekhaieko chha.
**sikai ko hisabama kunai paribartan chhaina.**

<!-- ne-section: ## 5. 実測した結果 -->
### Nepali ma

talaka sankhya yo batabaran ma **bastabama chalaer paieka** hun.
ti kritrim dataka maan hun ra **utpadan nirikshanko shuddhata hoinan**.

<!-- ne-section: ### 5.1 -->
### Nepali ma

`yolo26n.pt` lai kritrim dataset (train 64 / val 16 / test 16) ma 15 epoch, `imgsz=320`,
`batch=8`, CPU ma sikaieko. maapan mathiko talika ma chha (precision, recall, mAP50, mAP50-95).
**sikai samay:** kehi minet (hardware ma nirbhar).

<!-- ne-section: ### 5.2 -->
### Nepali ma

`resnet18`, `coreset_sampling_ratio=0.1`, `num_neighbors=9`, CPU ma chalaiyo.
maapan mathiko talika ma chha (image_AUROC, image_F1Score, pixel_AUROC, pixel_F1Score).

samanya utpadanako adhikatam score **0.356** ra asamanyako nyoonatam **0.473** thiyo; bichama threshold
rakhda chhutyaun sakinthyo. **kritrim chitra ma chhutyaun sajilo** hunchha bhanne yahi ho.
bastabik PVC ma yati sapha chhutyaundain.

<!-- ne-section: ### 5.3 -->
### Nepali ma

sajha 26 chitra (256×256, YOLO ko sikai ma napareka) ma tulna gariyo; natija mathiko talika ma chha.

tar **PatchCore ko threshold yahi tulna detabatai tay garieko** hunale PatchCore paksh
**ashabadi** chha. yo talika matra herer "PatchCore ramro" bhanne nishkarsh nikaln mildaina
(din 5 notebook 03 ko Part 4 ma spasht lekhieko chha).

<!-- ne-section: ## 6. 既知の問題 -->
### Nepali ma

| samasya | abastha | bato |
|---|---|---|
| `torch==2.10.0` ko Windows wheel import hundaina | dohoriyo | `torch==2.15.0` prayog garne |
| Lightning ko pragati dekhaile kahilekahin `RecursionError` dinchha | dohoriyo | `enable_progress_bar=False` |
| console ma Japani akshar bigranchha (cp932) | OS ma nirbhar | skriptako console output Angreji ma matra |
| sajha chitra ma YOLO ko recall kam (0.55) | apekshit | resolution ra bitaranko farak. din 4 notebook 03 ma chhalaphal |
| Anomalib ko mulyankan data adha bandinchha | dijainaanusar | `val_split_mode="from_test"` |
