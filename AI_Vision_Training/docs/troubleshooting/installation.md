# インストール時のトラブル対処 / Installation troubleshooting

セットアップでつまずいたときの手順書です。
**上から順に** 確認してください。9 割は最初の 3 つで解決します。

Use this when setup fails. Work **top to bottom**; the first three sections solve about
90 % of cases.

---

## 0. まずこれを実行する / Run this first

何かおかしいと感じたら、まず環境を確認します。

Whenever something feels wrong, check the environment first.

```powershell
cd "$HOME\Documents\AI_Vision_Training"
.\.venv\Scripts\Activate.ps1
python assets\scripts\verify_environment.py --profile all
```

表示の見方です。

| 表示 / Output | 意味 / Meaning | 対処 / Action |
|---|---|---|
| `Virtual env : YES / はい` | 仮想環境が有効 / venv active | OK |
| `Virtual env : NO` | **仮想環境が無効** / venv inactive | 下の 1 節 / see section 1 |
| `[MISSING] numpy ...` | パッケージ不足 / missing package | 下の 3 節 / see section 3 |
| `[MISS] ... assets` | 素材が未生成 / assets not generated | 下の 6 節 / see section 6 |
| `READY` | 準備完了 / ready | 次へ / continue |

---

## 1. `Activate.ps1 cannot be loaded because running scripts is disabled`

**原因 / Cause:** Windows の実行ポリシーが、PowerShell スクリプトの実行を止めています。
Windows policy blocks running PowerShell scripts.

**対処 / Fix:**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

組織が許可する場合だけ現在の窓で設定し、もう一度有効化します。管理者権限は不要です。
ポリシーを変えられなければ `.\.venv\Scripts\python.exe` を直接使います。
Only if permitted by your organisation, apply this to the current window and activate again.
No administrator is needed. Otherwise call `.\.venv\Scripts\python.exe` directly.

```powershell
.\.venv\Scripts\Activate.ps1
```

成功すると、プロンプトの先頭に `(.venv)` が付きます。
On success the prompt starts with `(.venv)`.

---

## 2. `python` と打つと Microsoft Store が開く / typing `python` opens the Store

**原因 / Cause:** Windows の「アプリ実行エイリアス」が、`python.exe` を横取りしています。
A Windows app-execution alias intercepts `python.exe`.

**対処 / Fix:**

1. Windows の設定を開く / open Windows Settings
2. 「アプリ」→「アプリ実行エイリアス」 / "Apps" -> "App execution aliases"
3. `python.exe` と `python3.exe` を **オフ** / turn both **off**
4. PowerShell を **閉じて開き直す** / close and reopen PowerShell

それでも直らない場合は、Python が PATH に入っていません。
[python.org](https://www.python.org/downloads/) のインストーラを実行し、
最初の画面で「**Add python.exe to PATH**」にチェックを入れて「Install Now」を押してください。

If that does not fix it, Python is not on PATH. Run the python.org installer and tick
"**Add python.exe to PATH**" on the first screen before choosing "Install Now".

---

## 3. `ModuleNotFoundError: No module named 'numpy'`（ノートブック内）/ inside a notebook

**原因 / Cause は 2 つ / two causes:**

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

### 3.2 パッケージが本当に入っていない / the package really is missing

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements\base.txt
python -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
```

`ipykernel install` を忘れると、Jupyter から見えません。**必ず実行してください。**
Forgetting `ipykernel install` hides the environment from Jupyter.

---

## 4. ダウンロードが `Read timed out` で止まる / downloads time out

**原因 / Cause:** ネットワークの一時的な失敗、または社内プロキシ。
Transient network failure, or a corporate proxy.

**対処 / Fix:**

1. **同じコマンドをもう一度実行**（最も効きます）/ **re-run the same command** (most effective)
2. それでもだめなら、プロキシを設定 / if it persists, configure the proxy

```powershell
$env:HTTP_PROXY  = "http://proxy.example.co.jp:8080"
$env:HTTPS_PROXY = "http://proxy.example.co.jp:8080"
python -m pip install -r requirements\base.txt
```

プロキシのアドレスは情報システム部門に確認してください。
Ask IT for the proxy address.

3. 社内ミラーがある場合は `--index-url` を指定 / with an internal mirror:

```powershell
python -m pip install -r requirements\base.txt --index-url https://pypi.example.co.jp/simple
```

---

## 5. OpenCV がおかしい / OpenCV behaves strangely

**症状 / Symptoms:** 色が反転する、`cv2` の動作が不安定、`findContours` の戻り値が違う。
Colours inverted, unstable `cv2`, unexpected `findContours` return values.

**原因 / Cause:** `opencv-python` と `opencv-python-headless` は**別の配布物**ですが、
どちらも `cv2` を提供します。**同じ環境に両方入れると壊れます。**
Both distributions provide `cv2`; installing both into one environment breaks it.

**確認 / Check:**

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip list | Select-String "opencv"
```

**1 行だけ** 表示されるのが正常です。2 行出たら壊れています。

**Exactly one line** is correct. Two lines means it is broken.

**対処 / Fix:**

```powershell
# .venv（第0〜4日）/ .venv (Days 0-4)
python -m pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python
python -m pip install opencv-python==4.12.0.88
```

```powershell
# .venv-anomalib（第5日）/ .venv-anomalib (Day 5)
python -m pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python
python -m pip install opencv-python-headless==4.12.0.88
```

2 つの環境を混ぜないでください。どの環境で実行しているかを
プロンプト（`(.venv)` か `(.venv-anomalib)`）で必ず確認してください。

Never mix the two environments. Always check the prompt (`(.venv)` or
`(.venv-anomalib)`) before installing.

---

## 6. 画像やデータが見つからない / assets or datasets are missing

**症状 / Symptom:** `FileNotFoundError`、`画像がありません`、`data.yaml がありません`。

**対処 / Fix:**

```powershell
.\.venv\Scripts\Activate.ps1
python assets\scripts\generate_training_assets.py
python assets\scripts\prepare_datasets.py
```

通常は既存データを再利用します。意図的に再生成する場合だけ講師と相談してください。
Normally reuse existing data. Discuss deliberate regeneration with the instructor first.

### 6.1 実写の参考画像が見つからない / the reference photographs are missing

**症状 / Symptom:** `assets/external_samples/open_reference/` に 4 枚そろっていない、
または「参考画像がそろっていません / reference images are incomplete」と表示される。

**対処 / Fix:**

```powershell
.\.venv\Scripts\Activate.ps1
python assets\scripts\download_reference_images.py --course-root .
```

- 取得するのは **参考画像 4 枚だけ** です（`chelsea.png`・`camera.png`・`brick.png`・`VisA_samples.png`）。
- 何度実行しても、正しく保存済みのファイルはそのまま再利用します（取得は 1 回だけ）。
- 失敗したファイル名が表示されます。**別の画像で代用しないでください。** 接続を確認して
  同じコマンドをもう一度実行します。
- ネットワークを使わずに、保存済みファイルだけを確認できます。

```powershell
python assets\scripts\download_reference_images.py --course-root . --offline
```

Only the four reference photographs are downloaded; valid cached files are reused and the failing
file name is printed. Never substitute a different image: check the connection and rerun the same
command. `--offline` verifies the saved files without any network request.

---

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

## 8. `anomalib` が見つからない / `No module named 'anomalib'`

第 5 日のノートブックは、**`aivision-anomalib` カーネル** で実行します。
`anomalib` は `.venv` には **入っていません**（意図的に分けています）。

The Day 5 notebooks run on the **`aivision-anomalib`** kernel. `anomalib` is
**deliberately not** in `.venv`.

**対処 / Fix:**

```powershell
python -m venv .venv-anomalib
.\.venv-anomalib\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements\anomalib.txt
python -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

---

## 9. `OSError: Error loading "...\torch\lib\c10.dll"`

**原因 / Cause:** `torch==2.10.0` の Windows ホイールが、この環境で import できませんでした。
The `torch==2.10.0` Windows wheel failed to import on the verification machine.

**対処 / Fix:**

```powershell
.\.venv-anomalib\Scripts\Activate.ps1
python -m pip uninstall -y torch torchvision
python -m pip install torch==2.15.0 torchvision==0.29.2
```

それでも直らない場合は、Microsoft Visual C++ 再頒布可能パッケージを入れ直してください。
If it persists, reinstall the Microsoft Visual C++ Redistributable.

---

## 10. メモリ不足 / out of memory

**症状 / Symptom:** `MemoryError`、`CUDA out of memory`、PC が極端に遅くなる。

**対処 / Fix:**

| 場面 / Situation | 対処 / Fix |
|---|---|
| YOLO の学習 / YOLO training | `BATCH` を 8 → 4、`IMGSZ` を 320 → 224 |
| PatchCore の学習 / PatchCore fit | `train_batch_size` と `eval_batch_size` を 4 に |
| ノートブック全般 / general | 他のアプリを閉じる / close other apps |

---

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
