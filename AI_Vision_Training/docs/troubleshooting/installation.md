# インストール時のトラブル対処 / Installation troubleshooting

セットアップでつまずいたときの手順書です。
**上から順に** 確認してください。正式な準備手順は [START_HERE](../../START_HERE.md) です。

Use this when setup fails. Work **top to bottom**. The authoritative preflight is
[START_HERE](../../START_HERE.md).

---

<!-- ne:begin doc:48b5707344 -->
### Nepali ma

setup garda aljhiyo bhane yo prakriya-pustika hernuhos.
**mathibat kramaisang** jaanchnuhos. adhikarik tayari prakriya
[START_HERE](../../START_HERE.md) ho.
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
### Nepali ma

kehi anautho lagyo bhane pahile batabaran jaanchnuhos.

File Explorer ma bastabik samagri folder kholer thegana barama `cmd` lekher Enter thichnuhos.
talaka adesh tyahi Command Prompt ma chalaunuhos. ahileko thaun `cd` le, bhitri samagri `dir` le
dekhaunchha. ZIP wa OneDrive bhae pani bastabik nikaleko thaun prayog garnuhos.

```cmd
.\.venv\Scripts\activate.bat
where python
python -c "import sys; print(sys.executable)"
python assets\scripts\verify_environment.py --profile all
```

din 5 ma nayan CMD jhyalama `.venv-anomalib` sakriya garera uhi jaanch garnuhos.
yo jaanchle chalaeko batabaran matra herchha.

dekhaiko arth yasari padhnuhos.

| dekhine | arth | ke garne |
|---|---|---|
| `Virtual env : YES / はい` | virtual environment sakriya chha | thik chha |
| `Virtual env : NO` | **virtual environment sakriya chhaina** | talako khand 1 |
| `[MISSING] numpy ...` | package napug | talako khand 3 |
| `[MISS] ... assets` | samagri baneko chhaina | talako khand 6 |
| `READY` | tayar chha | agadi badhnuhos |
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
### Nepali ma

samagri folderko CMD ma `dir .venv\Scripts\python.exe` chalaunuhos.
chhaina bhane [START_HERE step 3](../../START_HERE.md) ko banaune prakriyama pharkanuhos.
chha bhane `.\.venv\Scripts\activate.bat` le sakriya garnuhos. saphal bhae `(.venv)` dekhinchha.
execution policy wa prashasak adhikar paribartan aawashyak chhaina. sansthako bandej bhae IT sang sodhnuhos.

sakriya nagari chalaune tarika pani chha. tyas abastha ma `deactivate` aawashyak chhaina.

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
### Nepali ma

**karan:** Windows ko "app execution alias" le `python.exe` lai agadi chhekchha.

**ke garne:**

1. Windows Settings kholnuhos
2. "Apps" → "App execution aliases"
3. `python.exe` ra `python3.exe` **banda** garnuhos
4. Command Prompt **banda garera feri kholnuhos**

tyaspachhi pani namile Python PATH ma chhaina.
[python.org](https://www.python.org/downloads/) ko installer chalaer pahilo skrinama
"**Add python.exe to PATH**" ma chinh lagaer "Install Now" thichnuhos.
<!-- ne:end -->

## 3. `ModuleNotFoundError: No module named 'numpy'`（ノートブック内）/ inside a notebook

**原因 / Cause は 2 つ / two causes:**

<!-- ne:begin doc:0c74ecc329 -->
### Nepali ma

**karan 2 bata chhan:**
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
### Nepali ma

notebookle arko Python prayog gariraheko chha.

**ke garne:**

1. notebookko mathi-dayanko kernel naam ma klik garnuhos
2. `Python 3 (AI Vision)` chhannuhos
3. `Kernel` → `Restart Kernel and Run All Cells` garnuhos

**jaanch:** arko cellko output ma `.venv` chha ki hernuhos.

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
### Nepali ma

```cmd
.\.venv\Scripts\activate.bat
python -m pip install -r requirements\base.txt
python -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
```

`ipykernel install` birsiyo bhane Jupyter baat batabaran dekhindain. **aniwarya rupama chalaunuhos.**
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
### Nepali ma

**karan:** network ko kshanik asaphalata, wa kampaniko proxy.

**ke garne:**

1. **uhi adesh feri chalaunuhos** (sabaibhanda prabhabakari)
2. tyaspachhi pani nabhae proxy milaunuhos

talaka thegana **kalpanik udaharan** hun, kampaniko bastabik setting hoina. IT le pushti gareko maanle
badaler matra chalaunuhos. `set` le yo CMD jhyal ra tyas baat suru garieka programama matra asar garchha.
jhyal banda gare setting haraunchha. pahileko thik setting lai udaharanko maanle nabadalnuhos.

```cmd
set "HTTP_PROXY=http://proxy.example.co.jp:8080"
set "HTTPS_PROXY=http://proxy.example.co.jp:8080"
python -m pip install -r requirements\base.txt
```

proxy ko thegana suchana pranali bibhagasang sodhnuhos.

3. kampaniko mirror chha bhane `--index-url` dinuhos:

talako mirror pani udaharan ho. bastabik URL IT sang sodhnuhos.

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
### Nepali ma

**lakshan:** rang ulto dekhinchha, `cv2` asthir hunchha, `findContours` ko natija farak aaunchha.

**karan:** `opencv-python` ra `opencv-python-headless` **chhuttai package** hun, tar dubaile `cv2`
dinchhan. **eutai batabaran ma dubai rakhda bigranchha.**

**jaanch:**

```cmd
.\.venv\Scripts\activate.bat
python -m pip list | findstr /I opencv
```

**ek line matra** dekhinu thik ho. dui line dekhiyo bhane bigreko chha.

**ke garne:**

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

dui batabaran namisaunuhos. install garnuaghi prompt (`(.venv)` wa `(.venv-anomalib)`) ma kun
batabaran chaliraheko chha aniwarya jaanchnuhos.
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
### Nepali ma

**lakshan:** `FileNotFoundError`, `画像がありません`, `data.yaml がありません`.

**ke garne:**

```cmd
.\.venv\Scripts\activate.bat
python assets\scripts\generate_training_assets.py
python assets\scripts\prepare_datasets.py
```

samanyatah pahileko data nai punah prayog hunchha. janajan feri banaune ho bhane matra prashikshakasang sallah
garnuhos.
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
### Nepali ma

**lakshan:** `assets/external_samples/open_reference/` ma 4 bata pugeka chhainan, wa
"参考画像がそろっていません / reference images are incomplete" dekhinchha.

**ke garne:**

```cmd
.\.venv\Scripts\activate.bat
python assets\scripts\download_reference_images.py --course-root .
```

- lyaine **sandarbha chitra 4 bata matra** hun (`chelsea.png`, `camera.png`, `brick.png`,
  `VisA_samples.png`).
- jati patak chalae pani thik surakshit bhaisakeka file tyasai prayog hunchhan (lyaune kaam ek patak matra).
- asaphal bhaeko fileko naam dekhinchha. **arko chitrale nabadalnuhos.** jadan jancher uhi adesh feri
  chalaunuhos.
- network prayog nagari surakshit file matra jaanchna sakinchha.

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
### Nepali ma

paath aghi line ra aphalain jaanch garne kaam [START_HERE.md](../../START_HERE.md) ko step 7 ho.
`preload_models.py` le YOLO ko weight ra bus ko udaharan, ra Anomalib ko resnet18 cache janchchha.
`--offline` le network ma jodindain ra napug bhaeko kura trutika rupama bataunchha.

**lakshan:** `URLError`, `TimeoutError`, `yolo26n.pt` lina sakien.

**ke garne (yahi kram ma):**

1. **uhi cell feri chalaunuhos**
2. braujarabat linuhos:

```text
https://github.com/ultralytics/assets/releases
```

`yolo26n.pt` (karib 5 MB) daunalod garera `assets\models\` ma rakhnuhos.

3. kampaniko proxy chha bhane byabasthapakasang jaanchnuhos

**lina nasakeko bela mildojuldo natija banaunu hundaina.**
truti jastako tastai abhilekh garera prashikshakasang sallah garnuhos.
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
### Nepali ma

din 5 ko notebook **`aivision-anomalib` kernel** ma chalaunuhos.
`anomalib` `.venv` ma **chhaina** (janajan chhutyaieko).

**ke garne:**

ajhai banaiyeko chhaina bhane [START_HERE step 4–5](../../START_HERE.md) chalaunuhos.
pahileko batabaran sudharn sakriya nagari tyasko Python sidhai din sakinchha.

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
### Nepali ma

**karan:** `torch==2.10.0` ko Windows wheel yo batabaran ma import huna saken.

**ke garne:**

```cmd
".\.venv-anomalib\Scripts\python.exe" -m pip uninstall -y torch torchvision
".\.venv-anomalib\Scripts\python.exe" -m pip install torch==2.15.0 torchvision==0.29.2
```

tyaspachhi pani nabhae Microsoft Visual C++ Redistributable feri rakhnuhos.
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
### Nepali ma

**lakshan:** `MemoryError`, `CUDA out of memory`, PC atyadhik dhilo hunchha.

| abastha | ke garne |
|---|---|
| YOLO ko sikai | `BATCH` 8 → 4, `IMGSZ` 320 → 224 |
| PatchCore ko sikai | `train_batch_size` ra `eval_batch_size` 4 banaune |
| notebook samanya | aru anuprayog banda garne |
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
### Nepali ma

slider **chaliraheko kernel** ma matra chalchha. GitHub preview wa sthir HTML ma chaldain. tyo bigreko hoina.

| lakshan | karan | ke garne |
|---|---|---|
| kehi dekhindain | `ipywidgets` chhaina | `python -m pip install -r requirements\base.txt` chalaer kernel restart garne |
| `ipywidgets が見つかりません` dekhinchha | uhi | talako "parameter cell" ma uhi prayog garna sakinchha |
| slider dekhinchha tar chitra badalindain | kernel purano chha | **Kernel → Restart & Run All** |
| aghillo chitra thapindai janchha | output metieko chhaina | tyo cellko output metaer feri chalaune |

`ipywidgets` **aniwarya chhaina**. harek demo ma widget nachahine "parameter cell" tayar chha.
samay kam bhae tyahi prayog garnuhos.
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
### Nepali ma

talaka 4 kura tiper prashikshakalai bhannuhos. yi bhae samasya chhito samadhan hunchha.

1. **kun notebookko kun cell** (`In [ ]` ko number bhae pani hunchha)
2. **truti sandesh** (antim 3 line kapi)
3. `python assets\scripts\verify_environment.py --profile all` ko output
4. **pahile prayas gareka kura** ra tinako natija

CMD ko `where python` ra dubai batabaranko chhuttai jaanch natija pani sanlagn garnuhos.
proxy ko praman (credential) wa gopy jankari natansnuhos.
<!-- ne:end -->
