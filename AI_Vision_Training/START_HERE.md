# はじめかた / START HERE

これは Windows 11 / PowerShell の**正式な準備手順**です。第1日より前に、授業時間外で
上から順に進めます。インストールが終わってから準備ノートブックを開きます。

This is the **authoritative Windows 11 / PowerShell preflight sequence**. Complete it before
Day 1, outside lesson hours. Open the preparatory notebook after installation.

## ステップ 1　取得してフォルダを開く / Download and open the folder

GitHub の Code → Download ZIP を展開するか、Git がある場合は次を実行します。
Use Code → Download ZIP on GitHub and extract it, or use Git:

```powershell
Set-Location "$HOME\Documents"
git clone https://github.com/stefanoKS/Training_Automation.git
Set-Location .\Training_Automation\AI_Vision_Training
Get-ChildItem
```

ZIP の場合は展開先の `AI_Vision_Training` に移動します。以後のコマンドはすべて
`README.md` と `requirements` があるこのフォルダで実行します。

For a ZIP, move into the extracted `AI_Vision_Training` folder. Run all following commands
there, where `README.md` and `requirements` are visible.

## ステップ 2　Python 3.11 を確認する / Check Python 3.11

```powershell
py -3.11 --version
```

検証済みの系列は **Python 3.11** です。3.12 など他の系列は未検証です。
詳細は [tested_versions.md](requirements/tested_versions.md) を参照してください。
`py` が無ければ python.org の Python 3.11 を入れ、Add python.exe to PATH を選び、
PowerShell を開き直します。`python --version` が 3.11 なら以後の `py -3.11` を
`python` に置き換えられます。

**Python 3.11** is the tested series; 3.12 and other series are unverified.
See [tested_versions.md](requirements/tested_versions.md). If `py` is missing, install
Python 3.11 from python.org, select Add python.exe to PATH, and reopen PowerShell.
If `python --version` reports 3.11, substitute `python` for `py -3.11` below.

## ステップ 3　基本環境を作る / Create the base environment

仮想環境は研修用の道具箱です。他の仕事の Python と分けます。
A virtual environment is a course toolbox, separate from Python used for other work.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements\base.txt
python -m pip install -r requirements\yolo.txt
```

有効化が禁止されている場合、最も狭い回避策は有効化せず
`.\.venv\Scripts\python.exe` を直接使うことです。組織が許可する場合だけ、
現在の PowerShell 窓に限って次を設定して再度有効化します。管理者権限は不要です。

If activation is blocked, the narrowest workaround is to call
`.\.venv\Scripts\python.exe` directly without activating. Only if your organisation permits it,
apply the following to this PowerShell window and activate again. No administrator is needed.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## ステップ 4　Anomalib 環境を作る / Create the Anomalib environment

第5日は別の道具箱を使います。**標準手順では第1日前に両方を準備**します。
Day 5 uses another toolbox. **The default is to prepare both before Day 1.**

```powershell
deactivate
py -3.11 -m venv .venv-anomalib
.\.venv-anomalib\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements\anomalib.txt
```

有効化せず直接 Python を使っている場合は `deactivate` は不要です。
If you use Python executables directly, omit `deactivate`.

## ステップ 5　両方のカーネルを登録する / Register both kernels

カーネルはノートブックのコードを実行する Python です。
A kernel is the Python process that executes notebook code.

```powershell
.\.venv\Scripts\python.exe -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
.\.venv-anomalib\Scripts\python.exe -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

## ステップ 6　教材とデータを作る / Generate teaching assets and datasets

**基本環境 `.venv`** に戻ります。`--force` や `--clean` は不要です。
既存の提出物や保存済みモデル出力を再生成しません。

Return to **the base `.venv`**. Do not use `--force` or `--clean`. Do not regenerate
student submissions or saved model outputs.

```powershell
deactivate
.\.venv\Scripts\Activate.ps1
python assets\scripts\generate_training_assets.py
python assets\scripts\prepare_datasets.py
python assets\scripts\generate_teaching_diagrams.py
python assets\scripts\generate_svg_figures.py
```

## ステップ 7　オフライン授業の素材を先に取得する / Preload offline lesson inputs

参考写真はライセンス付きの原本です。合成画像や工場の実測結果ではありません。
重みも授業前に取得します。初回はネットワークが必要です。

Reference photographs are licensed originals, not synthetic images or factory measurements.
Download weights before lessons too. The initial download needs network access.

```powershell
python assets\scripts\download_reference_images.py --course-root .
python assets\scripts\preload_models.py --profile yolo
.\.venv-anomalib\Scripts\python.exe assets\scripts\preload_models.py --profile anomalib
python assets\scripts\download_reference_images.py --course-root . --offline
python assets\scripts\preload_models.py --profile yolo --offline
.\.venv-anomalib\Scripts\python.exe assets\scripts\preload_models.py --profile anomalib --offline
```

重みの配布・使用条件は提供元（Ultralytics / timm / torchvision）を確認してください。
取得に失敗したら授業前に講師へ連絡します。参考結果は
`assets/reference_outputs/`、受講者が実行して保存する結果は `submissions/` です。

Check the providers' licence terms (Ultralytics / timm / torchvision) before redistribution/use.
Report download failures before class. Supplied references live in `assets/reference_outputs/`;
students' live outputs go into `submissions/`.

## ステップ 8　環境と教材を確認する / Verify environments and assets

`--profile all` は**実行した環境だけ**を検査します。両方で実行してください。
`--profile all` checks **only the current environment**. Run it in both.

```powershell
.\.venv\Scripts\python.exe assets\scripts\verify_environment.py --profile all
.\.venv-anomalib\Scripts\python.exe assets\scripts\verify_environment.py --profile all
python assets\scripts\validate_notebooks.py
python -m jupyter kernelspec list
```

終了コード 0 に加え、表示された素材の不足がないことも確認します。
Check exit code 0 **and** that the printed asset list contains no missing items.

## ステップ 9　JupyterLab を起動する / Launch JupyterLab

```powershell
.\.venv\Scripts\python.exe -m jupyter lab
```

ブラウザが開かなければ表示された localhost の URL を開きます。
`notebooks` → `00_Setup` → `00_Environment_Setup.ipynb` を開き、
`Python 3 (AI Vision)` を選びます。第5日だけ `Python 3 (AI Vision Anomalib)` を選びます。

If no browser opens, open the printed localhost URL. Open
`notebooks` → `00_Setup` → `00_Environment_Setup.ipynb`, select `Python 3 (AI Vision)`.
Only Day 5 uses `Python 3 (AI Vision Anomalib)`.

## ステップ 10　準備完了を確認する / Complete preflight

第1日前に準備ノートブックを上から実行します。意図的なエラーの練習は説明どおり直します。
第1日 09:00–09:10 は準備済みの状態を再確認する時間で、インストール時間ではありません。

Run the setup notebook before Day 1; repair the deliberate error exercise as instructed.
Day 1 09:00–09:10 rechecks readiness; it is not installation time.

- [ ] 両カーネルが選べる / both kernels selectable
- [ ] 両環境の検査が成功し、素材に不足がない / both environment checks pass, no missing assets
- [ ] オフライン写真・重み検査が成功 / offline photo and weight checks pass
- [ ] Day01_02 Part 1 で画像が出る / Day01_02 Part 1 displays an image
- [ ] 図の日本語が四角に化けない / Japanese labels are not missing-glyph squares
- [ ] `submissions/day00/` に準備レポートを保存 / setup report saved in `submissions/day00/`

間に合わなければ [COURSE_SYLLABUS.md](COURSE_SYLLABUS.md) の回復手順を使います。
Use the recovery procedure in [COURSE_SYLLABUS.md](COURSE_SYLLABUS.md) if preflight is incomplete.

## ステップ 11　授業を始める / Start lessons

セルを選んで Shift+Enter、保存は Ctrl+S。セルは上から順番に実行します。
値はカーネルに残ります。順序を見失ったら Kernel → Restart Kernel and Run All Cells。
翌日はステップ1のフォルダに移動し、ステップ9で起動します。環境は作り直しません。
終了時は保存してブラウザを閉じ、PowerShell で Ctrl+C を押して停止を確認します。

Select a cell and press Shift+Enter; Ctrl+S saves. Run top to bottom. Values persist in the
kernel. If confused, use Kernel → Restart Kernel and Run All Cells.
Next day return to the Step 1 folder and launch with Step 9; do not recreate environments.
To finish, save, close the browser, then stop Jupyter with Ctrl+C in PowerShell.

### 例外：第4日後の Anomalib 準備 / Alternative: Anomalib setup after Day 4

講師が明示的に許可した場合のみ、ステップ4と Anomalib の登録・重み取得・検査を第4日後に
延期できます。この場合、第1日の確認は基本環境のみで、**全日程の準備完了とは言いません**。
第5日前に残りを完了します。標準の両環境チェックリストとは別の例外です。

Only with explicit instructor approval may Step 4 and Anomalib registration/preload/verification
wait until after Day 4. Then Day 1 checks only the base environment; **full-course readiness is
not achieved**. Finish the remaining checks before Day 5. This is an exception, not the default.

### 困ったとき / Troubleshooting

| 症状 / Symptom | 対処 / Action |
|---|---|
| `python` / `py` が無い / missing | ステップ2。PATH・アプリ実行エイリアスを確認 / Step 2, check PATH and app aliases |
| パッケージ不足 / missing package | 正しい環境で requirements を入れる / install requirements in the correct environment |
| カーネルが違う / wrong kernel | `import sys; print(sys.executable)` を Python セルで確認 / check in a Python cell |
| 有効化が禁止 / activation blocked | ステップ3の直接実行を使う / use Step 3's direct executable |
| 重みが無い / missing weights | ステップ7を再実行し、失敗を記録 / rerun Step 7 and record the failure |

PowerShell の `python -m pip` と、ノートブック専用の Jupyter `%pip` は別物です。
授業中の自動インストールはしません。詳細は [installation.md](docs/troubleshooting/installation.md)。

PowerShell `python -m pip` and notebook-only Jupyter `%pip` are different.
Lessons do not install automatically. See [installation.md](docs/troubleshooting/installation.md).
