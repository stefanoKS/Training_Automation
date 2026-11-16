# インストール時のトラブル対処 / Installation troubleshooting

セットアップでつまずいたときの手順書です。
**上から順に** 確認してください。正式な準備手順は [START_HERE](../../START_HERE.md) です。

Use this when setup fails. Work **top to bottom**. The authoritative preflight is
[START_HERE](../../START_HERE.md).

---

<!-- ne:begin doc:48b5707344 -->
### नेपालीमा

setup गर्दा अल्झियो भने यो प्रक्रिया-पुस्तिका हेर्नुहोस्।
**माथिबाट क्रमैसँग** जाँच्नुहोस्। आधिकारिक तयारी प्रक्रिया
[START_HERE](../../START_HERE.md) हो।
<!-- ne:end -->

## 0. まずこれを実行する / Run this first

何かおかしいと感じたら、まず環境を確認します。

Whenever something feels wrong, check the environment first.

エクスプローラーで実際の教材フォルダを開き、アドレス欄に `cmd` と入力して Enter。
以下はそのコマンド プロンプトで実行します。現在地は `cd`、中身は `dir` で確認できます。
ZIP・OneDrive の場合も実際の展開先を使います。

Open the actual course folder in File Explorer, type `cmd` in its address bar and press Enter.
Run these commands in that Command Prompt. Use `cd` to print your location and `dir` to list files.
For ZIP/OneDrive installations use the actual extracted folder too.

```cmd
.\.venv\Scripts\activate.bat
where python
python -c "import sys; print(sys.executable)"
python assets\scripts\verify_environment.py --profile all
```

第5日は新しい CMD 窓で `.venv-anomalib` を有効化して同じ検査をします。
この検査は実行した環境だけが対象です。

For Day 5, activate `.venv-anomalib` in a fresh CMD window and repeat the check.
It checks only the interpreter that runs it.

表示の見方です。

| 表示 / Output | 意味 / Meaning | 対処 / Action |
|---|---|---|
| `Virtual env : YES / はい` | 仮想環境が有効 / venv active | OK |
| `Virtual env : NO` | **仮想環境が無効** / venv inactive | 下の 1 節 / see section 1 |
| `[MISSING] numpy ...` | パッケージ不足 / missing package | 下の 3 節 / see section 3 |
| `[MISS] ... assets` | 素材が未生成 / assets not generated | 下の 6 節 / see section 6 |
| `READY` | 準備完了 / ready | 次へ / continue |

---

<!-- ne:begin doc:d4294fae95 -->
### नेपालीमा

केही अनौठो लाग्यो भने पहिले वातावरण जाँच्नुहोस्।

File Explorer मा वास्तविक सामग्री फोल्डर खोलेर ठेगाना बारमा `cmd` लेखेर Enter थिच्नुहोस्।
तलका आदेश त्यही Command Prompt मा चलाउनुहोस्। अहिलेको ठाउँ `cd` ले, भित्री सामग्री `dir` ले
देखाउँछ। ZIP वा OneDrive भए पनि वास्तविक निकालेको ठाउँ प्रयोग गर्नुहोस्।

```cmd
.\.venv\Scripts\activate.bat
where python
python -c "import sys; print(sys.executable)"
python assets\scripts\verify_environment.py --profile all
```

दिन ५ मा नयाँ CMD झ्यालमा `.venv-anomalib` सक्रिय गरेर उही जाँच गर्नुहोस्।
यो जाँचले चलाएको वातावरण मात्र हेर्छ।

देखाइको अर्थ यसरी पढ्नुहोस्।

| देखिने | अर्थ | के गर्ने |
|---|---|---|
| `Virtual env : YES / はい` | virtual environment सक्रिय छ | ठीक छ |
| `Virtual env : NO` | **virtual environment सक्रिय छैन** | तलको खण्ड 1 |
| `[MISSING] numpy ...` | package नपुग | तलको खण्ड 3 |
| `[MISS] ... assets` | सामग्री बनेको छैन | तलको खण्ड 6 |
| `READY` | तयार छ | अगाडि बढ्नुहोस् |
<!-- ne:end -->

## 1. 仮想環境を有効化できない / Cannot activate the virtual environment

教材フォルダの CMD で `dir .venv\Scripts\python.exe` を実行します。
無ければ [START_HERE ステップ3](../../START_HERE.md) の作成手順に戻ります。
有れば `.\.venv\Scripts\activate.bat` で有効化します。成功すると `(.venv)` が付きます。
実行ポリシーや管理者権限の変更は不要です。組織の制限は IT に相談してください。

In CMD at the course folder, run `dir .venv\Scripts\python.exe`. If missing, return to
[START_HERE Step 3](../../START_HERE.md). Otherwise activate with
`.\.venv\Scripts\activate.bat`; the prompt should start with `(.venv)`.
No execution-policy or administrator changes are needed. Ask IT about organisational restrictions.

有効化せず実行する方法もあります。この場合 `deactivate` は不要です。
You may also call the interpreter directly without activation; then omit `deactivate`.

```cmd
".\.venv\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv-anomalib\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
```

---

<!-- ne:begin doc:f232ffa42e -->
### नेपालीमा

सामग्री फोल्डरको CMD मा `dir .venv\Scripts\python.exe` चलाउनुहोस्।
छैन भने [START_HERE स्टेप 3](../../START_HERE.md) को बनाउने प्रक्रियामा फर्कनुहोस्।
छ भने `.\.venv\Scripts\activate.bat` ले सक्रिय गर्नुहोस्। सफल भए `(.venv)` देखिन्छ।
execution policy वा प्रशासक अधिकार परिवर्तन आवश्यक छैन। संस्थाको बन्देज भए IT सँग सोध्नुहोस्।

सक्रिय नगरी चलाउने तरिका पनि छ। त्यस अवस्थामा `deactivate` आवश्यक छैन।

```cmd
".\.venv\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv-anomalib\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
```
<!-- ne:end -->

## 2. `python` と打つと Microsoft Store が開く / typing `python` opens the Store

**原因 / Cause:** Windows の「アプリ実行エイリアス」が、`python.exe` を横取りしています。
A Windows app-execution alias intercepts `python.exe`.

**対処 / Fix:**

1. Windows の設定を開く / open Windows Settings
2. 「アプリ」→「アプリ実行エイリアス」 / "Apps" -> "App execution aliases"
3. `python.exe` と `python3.exe` を **オフ** / turn both **off**
4. コマンド プロンプトを **閉じて開き直す** / close and reopen Command Prompt

それでも直らない場合は、Python が PATH に入っていません。
[python.org](https://www.python.org/downloads/) のインストーラを実行し、
最初の画面で「**Add python.exe to PATH**」にチェックを入れて「Install Now」を押してください。

If that does not fix it, Python is not on PATH. Run the python.org installer and tick
"**Add python.exe to PATH**" on the first screen before choosing "Install Now".

---

<!-- ne:begin doc:4713166a3d -->
### नेपालीमा

**कारण:** Windows को "app execution alias" ले `python.exe` लाई अगाडि छेक्छ।

**के गर्ने:**

1. Windows Settings खोल्नुहोस्
2. "Apps" → "App execution aliases"
3. `python.exe` र `python3.exe` **बन्द** गर्नुहोस्
4. Command Prompt **बन्द गरेर फेरि खोल्नुहोस्**

त्यसपछि पनि नमिले Python PATH मा छैन।
[python.org](https://www.python.org/downloads/) को installer चलाएर पहिलो स्क्रिनमा
"**Add python.exe to PATH**" मा चिन्ह लगाएर "Install Now" थिच्नुहोस्।
<!-- ne:end -->

## 3. `ModuleNotFoundError: No module named 'numpy'`（ノートブック内）/ inside a notebook

**原因 / Cause は 2 つ / two causes:**

<!-- ne:begin doc:0c74ecc329 -->
### नेपालीमा

**कारण २ वटा छन्:**
<!-- ne:end -->

### 3.1 カーネルが違う / the wrong kernel (most common)

ノートブックが、別の Python を使っています。

**対処 / Fix:**

1. ノートブック右上のカーネル名をクリック / click the kernel name top-right
2. `Python 3 (AI Vision)` を選ぶ / choose it
3. `Kernel` → `Restart Kernel and Run All Cells`

**確認 / Check:** 次のセルの出力が `.venv` を含むか見てください。

```python
import sys
print(sys.executable)
```

<!-- ne:begin doc:11b0721926 -->
### नेपालीमा

नोटबुकले अर्को Python प्रयोग गरिरहेको छ।

**के गर्ने:**

1. नोटबुकको माथि-दायाँको kernel नाममा क्लिक गर्नुहोस्
2. `Python 3 (AI Vision)` छान्नुहोस्
3. `Kernel` → `Restart Kernel and Run All Cells` गर्नुहोस्

**जाँच:** अर्को सेलको output मा `.venv` छ कि हेर्नुहोस्।

```python
import sys
print(sys.executable)
```
<!-- ne:end -->

### 3.2 パッケージが本当に入っていない / the package really is missing

```cmd
.\.venv\Scripts\activate.bat
python -m pip install -r requirements\base.txt
python -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
```

`ipykernel install` を忘れると、Jupyter から見えません。**必ず実行してください。**
Forgetting `ipykernel install` hides the environment from Jupyter.

---

<!-- ne:begin doc:8f59b5a784 -->
### नेपालीमा

```cmd
.\.venv\Scripts\activate.bat
python -m pip install -r requirements\base.txt
python -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
```

`ipykernel install` बिर्सियो भने Jupyter बाट वातावरण देखिँदैन। **अनिवार्य रूपमा चलाउनुहोस्।**
<!-- ne:end -->

## 4. ダウンロードが `Read timed out` で止まる / downloads time out

**原因 / Cause:** ネットワークの一時的な失敗、または社内プロキシ。
Transient network failure, or a corporate proxy.

**対処 / Fix:**

1. **同じコマンドをもう一度実行**（最も効きます）/ **re-run the same command** (most effective)
2. それでもだめなら、プロキシを設定 / if it persists, configure the proxy

次は**架空の例**で、会社の実設定ではありません。IT に確認した値に置き換えてから実行します。
`set` はこの CMD 窓と、その窓から起動したプログラムだけに作用します。
窓を閉じれば設定は消えます。既存の正しい設定を例の値で上書きしないでください。

These are **example addresses, not company configuration**. Replace them with values confirmed
by IT before running. `set` affects only this CMD session and its child processes; closing the
window discards it. Never overwrite a working configuration with these example values.

```cmd
set "HTTP_PROXY=http://proxy.example.co.jp:8080"
set "HTTPS_PROXY=http://proxy.example.co.jp:8080"
python -m pip install -r requirements\base.txt
```

プロキシのアドレスは情報システム部門に確認してください。
Ask IT for the proxy address.

3. 社内ミラーがある場合は `--index-url` を指定 / with an internal mirror:

次のミラーも例です。実際の URL は IT に確認します。
The following mirror is also an example; obtain the actual URL from IT.

```cmd
python -m pip install -r requirements\base.txt --index-url https://pypi.example.co.jp/simple
```

---

<!-- ne:begin doc:f7b0c320c8 -->
### नेपालीमा

**कारण:** network को क्षणिक असफलता, वा कम्पनीको proxy।

**के गर्ने:**

1. **उही आदेश फेरि चलाउनुहोस्** (सबैभन्दा प्रभावकारी)
2. त्यसपछि पनि नभए proxy मिलाउनुहोस्

तलका ठेगाना **काल्पनिक उदाहरण** हुन्, कम्पनीको वास्तविक सेटिङ होइन। IT ले पुष्टि गरेको मानले
बदलेर मात्र चलाउनुहोस्। `set` ले यो CMD झ्याल र त्यसबाट सुरु गरिएका प्रोग्राममा मात्र असर गर्छ।
झ्याल बन्द गरे सेटिङ हराउँछ। पहिलेको ठीक सेटिङलाई उदाहरणको मानले नबदल्नुहोस्।

```cmd
set "HTTP_PROXY=http://proxy.example.co.jp:8080"
set "HTTPS_PROXY=http://proxy.example.co.jp:8080"
python -m pip install -r requirements\base.txt
```

proxy को ठेगाना सूचना प्रणाली विभागसँग सोध्नुहोस्।

3. कम्पनीको mirror छ भने `--index-url` दिनुहोस्:

तलको mirror पनि उदाहरण हो। वास्तविक URL IT सँग सोध्नुहोस्।

```cmd
python -m pip install -r requirements\base.txt --index-url https://pypi.example.co.jp/simple
```
<!-- ne:end -->

## 5. OpenCV がおかしい / OpenCV behaves strangely

**症状 / Symptoms:** 色が反転する、`cv2` の動作が不安定、`findContours` の戻り値が違う。
Colours inverted, unstable `cv2`, unexpected `findContours` return values.

**原因 / Cause:** `opencv-python` と `opencv-python-headless` は**別の配布物**ですが、
どちらも `cv2` を提供します。**同じ環境に両方入れると壊れます。**
Both distributions provide `cv2`; installing both into one environment breaks it.

**確認 / Check:**

```cmd
.\.venv\Scripts\activate.bat
python -m pip list | findstr /I opencv
```

**1 行だけ** 表示されるのが正常です。2 行出たら壊れています。

**Exactly one line** is correct. Two lines means it is broken.

**対処 / Fix:**

```cmd
REM .venv (Days 0-4); direct interpreter, no activation needed.
".\.venv\Scripts\python.exe" -m pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python
".\.venv\Scripts\python.exe" -m pip install opencv-python==4.12.0.88
```

```cmd
REM .venv-anomalib (Day 5); direct interpreter, no activation needed.
".\.venv-anomalib\Scripts\python.exe" -m pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python
".\.venv-anomalib\Scripts\python.exe" -m pip install opencv-python-headless==4.12.0.88
```

2 つの環境を混ぜないでください。どの環境で実行しているかを
プロンプト（`(.venv)` か `(.venv-anomalib)`）で必ず確認してください。

Never mix the two environments. Always check the prompt (`(.venv)` or
`(.venv-anomalib)`) before installing.

---

<!-- ne:begin doc:73f662540c -->
### नेपालीमा

**लक्षण:** रङ उल्टो देखिन्छ, `cv2` अस्थिर हुन्छ, `findContours` को नतिजा फरक आउँछ।

**कारण:** `opencv-python` र `opencv-python-headless` **छुट्टै package** हुन्, तर दुवैले `cv2`
दिन्छन्। **एउटै वातावरणमा दुवै राख्दा बिग्रन्छ।**

**जाँच:**

```cmd
.\.venv\Scripts\activate.bat
python -m pip list | findstr /I opencv
```

**एक लाइन मात्र** देखिनु ठीक हो। दुई लाइन देखियो भने बिग्रेको छ।

**के गर्ने:**

```cmd
REM .venv (Days 0-4); direct interpreter, no activation needed.
".\.venv\Scripts\python.exe" -m pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python
".\.venv\Scripts\python.exe" -m pip install opencv-python==4.12.0.88
```

```cmd
REM .venv-anomalib (Day 5); direct interpreter, no activation needed.
".\.venv-anomalib\Scripts\python.exe" -m pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python
".\.venv-anomalib\Scripts\python.exe" -m pip install opencv-python-headless==4.12.0.88
```

दुई वातावरण नमिसाउनुहोस्। install गर्नुअघि prompt (`(.venv)` वा `(.venv-anomalib)`) मा कुन
वातावरण चलिरहेको छ अनिवार्य जाँच्नुहोस्।
<!-- ne:end -->

## 6. 画像やデータが見つからない / assets or datasets are missing

**症状 / Symptom:** `FileNotFoundError`、`画像がありません`、`data.yaml がありません`。

**対処 / Fix:**

```cmd
.\.venv\Scripts\activate.bat
python assets\scripts\generate_training_assets.py
python assets\scripts\prepare_datasets.py
```

通常は既存データを再利用します。意図的に再生成する場合だけ講師と相談してください。
Normally reuse existing data. Discuss deliberate regeneration with the instructor first.

<!-- ne:begin doc:1775cfdc3c -->
### नेपालीमा

**लक्षण:** `FileNotFoundError`, `画像がありません`, `data.yaml がありません`।

**के गर्ने:**

```cmd
.\.venv\Scripts\activate.bat
python assets\scripts\generate_training_assets.py
python assets\scripts\prepare_datasets.py
```

सामान्यतः पहिलेको डेटा नै पुनः प्रयोग हुन्छ। जानाजान फेरि बनाउने हो भने मात्र प्रशिक्षकसँग सल्लाह
गर्नुहोस्।
<!-- ne:end -->

### 6.1 実写の参考画像が見つからない / the reference photographs are missing

**症状 / Symptom:** `assets/external_samples/open_reference/` に 4 枚そろっていない、
または「参考画像がそろっていません / reference images are incomplete」と表示される。

**対処 / Fix:**

```cmd
.\.venv\Scripts\activate.bat
python assets\scripts\download_reference_images.py --course-root .
```

- 取得するのは **参考画像 4 枚だけ** です（`chelsea.png`・`camera.png`・`brick.png`・`VisA_samples.png`）。
- 何度実行しても、正しく保存済みのファイルはそのまま再利用します（取得は 1 回だけ）。
- 失敗したファイル名が表示されます。**別の画像で代用しないでください。** 接続を確認して
  同じコマンドをもう一度実行します。
- ネットワークを使わずに、保存済みファイルだけを確認できます。

```cmd
python assets\scripts\download_reference_images.py --course-root . --offline
```

Only the four reference photographs are downloaded; valid cached files are reused and the failing
file name is printed. Never substitute a different image: check the connection and rerun the same
command. `--offline` verifies the saved files without any network request.

---

<!-- ne:begin doc:3429cafc62 -->
### नेपालीमा

**लक्षण:** `assets/external_samples/open_reference/` मा ४ वटा पुगेका छैनन्, वा
"参考画像がそろっていません / reference images are incomplete" देखिन्छ।

**के गर्ने:**

```cmd
.\.venv\Scripts\activate.bat
python assets\scripts\download_reference_images.py --course-root .
```

- ल्याइने **सन्दर्भ चित्र ४ वटा मात्र** हुन् (`chelsea.png`, `camera.png`, `brick.png`,
  `VisA_samples.png`)।
- जति पटक चलाए पनि ठीक सुरक्षित भइसकेका फाइल त्यसै प्रयोग हुन्छन् (ल्याउने काम एक पटक मात्र)।
- असफल भएको फाइलको नाम देखिन्छ। **अर्को चित्रले नबदल्नुहोस्।** जडान जाँचेर उही आदेश फेरि
  चलाउनुहोस्।
- network प्रयोग नगरी सुरक्षित फाइल मात्र जाँच्न सकिन्छ।

```cmd
python assets\scripts\download_reference_images.py --course-root . --offline
```
<!-- ne:end -->

## 7. モデルのダウンロードに失敗する / model download fails

授業前の取得・オフライン検査は [START_HERE.md](../../START_HERE.md) ステップ7です。
`preload_models.py` は YOLO の重みと bus の例、Anomalib の resnet18 キャッシュを検査します。
`--offline` はネットワークに接続せず、不足をエラーとして報告します。

Use [START_HERE.md](../../START_HERE.md) Step 7 to preload and verify offline.
`preload_models.py` checks YOLO weights/bus example and Anomalib's resnet18 cache.
`--offline` never requests the network and reports missing inputs as errors.

**症状 / Symptom:** `URLError`、`TimeoutError`、`yolo26n.pt` が取得できない。

**対処 / Fix の順序 / in this order:**

1. **同じセルをもう一度実行**する / re-run the same cell
2. ブラウザで取得する / download manually:

```text
https://github.com/ultralytics/assets/releases
```

`yolo26n.pt`（約 5 MB）をダウンロードし、`assets\models\` に置きます。
Download `yolo26n.pt` (~5 MB) and place it in `assets\models\`.

3. 社内プロキシがある場合は管理者に確認 / ask IT about the proxy

**取得できなかったときに、それらしい結果を作ってはいけません。**
エラーをそのまま記録し、講師に相談してください。

**Never fabricate a result when the download fails.** Record the error and ask the
instructor.

---

<!-- ne:begin doc:23769afbb0 -->
### नेपालीमा

पाठ अघि लिने र अफलाइन जाँच गर्ने काम [START_HERE.md](../../START_HERE.md) को स्टेप 7 हो।
`preload_models.py` ले YOLO को weight र bus को उदाहरण, र Anomalib को resnet18 cache जाँच्छ।
`--offline` ले network मा जोडिँदैन र नपुग भएको कुरा त्रुटिका रूपमा बताउँछ।

**लक्षण:** `URLError`, `TimeoutError`, `yolo26n.pt` लिन सकिएन।

**के गर्ने (यही क्रममा):**

1. **उही सेल फेरि चलाउनुहोस्**
2. ब्राउजरबाट लिनुहोस्:

```text
https://github.com/ultralytics/assets/releases
```

`yolo26n.pt` (करिब 5 MB) डाउनलोड गरेर `assets\models\` मा राख्नुहोस्।

3. कम्पनीको proxy छ भने व्यवस्थापकसँग जाँच्नुहोस्

**लिन नसकेको बेला मिल्दोजुल्दो नतिजा बनाउनु हुँदैन।**
त्रुटि जस्ताको तस्तै अभिलेख गरेर प्रशिक्षकसँग सल्लाह गर्नुहोस्।
<!-- ne:end -->

## 8. `anomalib` が見つからない / `No module named 'anomalib'`

第 5 日のノートブックは、**`aivision-anomalib` カーネル** で実行します。
`anomalib` は `.venv` には **入っていません**（意図的に分けています）。

The Day 5 notebooks run on the **`aivision-anomalib`** kernel. `anomalib` is
**deliberately not** in `.venv`.

**対処 / Fix:**

未作成なら [START_HERE ステップ4〜5](../../START_HERE.md) を実行します。
既存環境の修復は有効化せず、その Python を直接指定できます。

If not yet created, follow [START_HERE Steps 4–5](../../START_HERE.md).
To repair an existing environment, call its Python directly without activation:

```cmd
".\.venv-anomalib\Scripts\python.exe" -m pip install -r requirements\anomalib.txt
".\.venv-anomalib\Scripts\python.exe" -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

---

<!-- ne:begin doc:963898c2dd -->
### नेपालीमा

दिन ५ को नोटबुक **`aivision-anomalib` kernel** मा चलाउनुहोस्।
`anomalib` `.venv` मा **छैन** (जानाजान छुट्याइएको)।

**के गर्ने:**

अझै बनाइएको छैन भने [START_HERE स्टेप 4–5](../../START_HERE.md) चलाउनुहोस्।
पहिलेको वातावरण सुधार्न सक्रिय नगरी त्यसको Python सिधै दिन सकिन्छ।

```cmd
".\.venv-anomalib\Scripts\python.exe" -m pip install -r requirements\anomalib.txt
".\.venv-anomalib\Scripts\python.exe" -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```
<!-- ne:end -->

## 9. `OSError: Error loading "...\torch\lib\c10.dll"`

**原因 / Cause:** `torch==2.10.0` の Windows ホイールが、この環境で import できませんでした。
The `torch==2.10.0` Windows wheel failed to import on the verification machine.

**対処 / Fix:**

```cmd
".\.venv-anomalib\Scripts\python.exe" -m pip uninstall -y torch torchvision
".\.venv-anomalib\Scripts\python.exe" -m pip install torch==2.15.0 torchvision==0.29.2
```

それでも直らない場合は、Microsoft Visual C++ 再頒布可能パッケージを入れ直してください。
If it persists, reinstall the Microsoft Visual C++ Redistributable.

---

<!-- ne:begin doc:738b410c8f -->
### नेपालीमा

**कारण:** `torch==2.10.0` को Windows wheel यो वातावरणमा import हुन सकेन।

**के गर्ने:**

```cmd
".\.venv-anomalib\Scripts\python.exe" -m pip uninstall -y torch torchvision
".\.venv-anomalib\Scripts\python.exe" -m pip install torch==2.15.0 torchvision==0.29.2
```

त्यसपछि पनि नभए Microsoft Visual C++ Redistributable फेरि राख्नुहोस्।
<!-- ne:end -->

## 10. メモリ不足 / out of memory

**症状 / Symptom:** `MemoryError`、`CUDA out of memory`、PC が極端に遅くなる。

**対処 / Fix:**

| 場面 / Situation | 対処 / Fix |
|---|---|
| YOLO の学習 / YOLO training | `BATCH` を 8 → 4、`IMGSZ` を 320 → 224 |
| PatchCore の学習 / PatchCore fit | `train_batch_size` と `eval_batch_size` を 4 に |
| ノートブック全般 / general | 他のアプリを閉じる / close other apps |

---

<!-- ne:begin doc:0ee59211dd -->
### नेपालीमा

**लक्षण:** `MemoryError`, `CUDA out of memory`, PC अत्यधिक ढिलो हुन्छ।

| अवस्था | के गर्ने |
|---|---|
| YOLO को सिकाइ | `BATCH` 8 → 4, `IMGSZ` 320 → 224 |
| PatchCore को सिकाइ | `train_batch_size` र `eval_batch_size` 4 बनाउने |
| नोटबुक सामान्य | अरू अनुप्रयोग बन्द गर्ने |
<!-- ne:end -->

## 11. スライダーが動かない / the sliders do nothing

スライダーは **生きているカーネル** でしか動きません。GitHub のプレビューや
静的な HTML では動きません。それは故障ではありません。

Sliders only work with a **live kernel**. They do nothing in GitHub previews or static HTML;
that is not a fault.

| 症状 / Symptom | 原因 / Cause | 対処 / Fix |
|---|---|---|
| 何も表示されない / nothing appears | `ipywidgets` が入っていない / not installed | `python -m pip install -r requirements\base.txt` を実行し、カーネルを再起動 / install, then restart the kernel |
| `ipywidgets が見つかりません` と出る | 同上 / same | 下の「パラメータセル」で同じ実験ができます / use the parameter cell below it |
| スライダーは出るが図が変わらない / the slider appears, the figure does not change | カーネルが古い / stale kernel | **Kernel → Restart & Run All** |
| 前の図が残って増えていく / figures pile up | 出力が消えていない / outputs not cleared | そのセルの出力を消して再実行 / clear the cell output and re-run |

`ipywidgets` は **必修ではありません**。どのデモにも、ウィジェットを使わない
「パラメータセル」が用意してあります。時間がないときは、そちらを使ってください。

`ipywidgets` is **not required**. Every demo has a parameter cell that needs no widget. If time is
short, use that.

---

<!-- ne:begin doc:417c667bd7 -->
### नेपालीमा

slider **चलिरहेको kernel** मा मात्र चल्छ। GitHub preview वा स्थिर HTML मा चल्दैन। त्यो बिग्रेको होइन।

| लक्षण | कारण | के गर्ने |
|---|---|---|
| केही देखिँदैन | `ipywidgets` छैन | `python -m pip install -r requirements\base.txt` चलाएर kernel restart गर्ने |
| `ipywidgets が見つかりません` देखिन्छ | उही | तलको "parameter सेल" मा उही प्रयोग गर्न सकिन्छ |
| slider देखिन्छ तर चित्र बदलिँदैन | kernel पुरानो छ | **Kernel → Restart & Run All** |
| अघिल्लो चित्र थपिँदै जान्छ | output मेटिएको छैन | त्यो सेलको output मेटाएर फेरि चलाउने |

`ipywidgets` **अनिवार्य छैन**। हरेक demo मा widget नचाहिने "parameter सेल" तयार छ।
समय कम भए त्यही प्रयोग गर्नुहोस्।
<!-- ne:end -->

## 12. それでも解決しないとき / when nothing works

次の 4 つをメモして講師に伝えてください。これがあると解決が早くなります。

1. **どのノートブックの、どのセル** か（`In [ ]` の番号でも可）
2. **エラーメッセージ**（最後の 3 行をコピー）
3. `python assets\scripts\verify_environment.py --profile all` の出力
4. **すでに試したこと** と、その結果

Note these four things for the instructor; they make diagnosis much faster.

1. which notebook and which cell (the `In [ ]` number is fine)
2. the error message (copy the last three lines)
3. the output of `verify_environment.py --profile all`
4. what you already tried, and what happened

CMD の `where python` と、両環境それぞれの検査結果も添えてください。
プロキシの認証情報や秘密情報は貼り付けないでください。

Include CMD's `where python` and the separate check results for both environments.
Do not paste proxy credentials or other secrets.

<!-- ne:begin doc:685a646f53 -->
### नेपालीमा

तलका ४ कुरा टिपेर प्रशिक्षकलाई भन्नुहोस्। यी भए समस्या छिटो समाधान हुन्छ।

1. **कुन नोटबुकको कुन सेल** (`In [ ]` को नम्बर भए पनि हुन्छ)
2. **त्रुटि सन्देश** (अन्तिम ३ लाइन कपी)
3. `python assets\scripts\verify_environment.py --profile all` को output
4. **पहिले प्रयास गरेका कुरा** र तिनको नतिजा

CMD को `where python` र दुवै वातावरणको छुट्टै जाँच नतिजा पनि संलग्न गर्नुहोस्।
proxy को प्रमाण (credential) वा गोप्य जानकारी नटाँस्नुहोस्।
<!-- ne:end -->
