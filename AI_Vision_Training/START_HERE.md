# はじめかた / START HERE

これは Windows 11 / コマンド プロンプト（cmd.exe）の**正式な準備手順**です。第1日より前に、授業時間外で
上から順に進めます。インストールが終わってから準備ノートブックを開きます。

This is the **authoritative Windows 11 / Command Prompt (cmd.exe) preflight sequence**. Complete it before
Day 1, outside lesson hours. Open the preparatory notebook after installation.

## ステップ 1　取得してフォルダを開く / Download and open the folder

Windows の検索で「コマンド プロンプト」または `cmd` を開きます。
エクスプローラーで目的のフォルダを開き、アドレス欄に `cmd` と入力して Enter でも開けます。
以下はこの窓に1行ずつ貼り付けます。管理者として開く必要はありません。

Open **Command Prompt** by searching Windows for `cmd`, or type `cmd` in File Explorer's
address bar and press Enter. Paste the following commands one line at a time into that window.
Administrator privileges are not required.

GitHub の Code → Download ZIP を展開するか、Git がある場合は次を実行します。
Use Code → Download ZIP on GitHub and extract it, or use Git:

```cmd
cd /d "%USERPROFILE%\Documents"
git clone https://github.com/stefanoKS/Training_Automation.git
cd /d "%USERPROFILE%\Documents\Training_Automation\AI_Vision_Training"
dir
```

ZIP の場合は展開先の `AI_Vision_Training` に移動します。以後のコマンドはすべて
`README.md` と `requirements` があるこのフォルダで実行します。

For a ZIP, move into the extracted `AI_Vision_Training` folder. Run all following commands
there, where `README.md` and `requirements` are visible.

Documents が OneDrive などへ移動されている場合は、実際の展開先を使ってください。
`cd /d "<actual extracted AI_Vision_Training path>"` の山括弧内は説明用の仮の文字列です。
そのまま実行せず、実際のパスに置き換えます。例：

If Documents is redirected (for example to OneDrive), use your actual extracted folder.
In `cd /d "<actual extracted AI_Vision_Training path>"`, the angle-bracketed text is a
placeholder, not a valid path to paste unchanged. Replace it with the real path, for example:

```cmd
cd /d "D:\Training Materials\Training_Automation\AI_Vision_Training"
dir
cd
```

`dir` は中身、引数なしの `cd` は現在地を表示します。空白を含むパスも必ず引用符で囲みます。
`dir` lists files; `cd` without arguments prints your location. Keep paths quoted, including spaces.

<!-- ne:begin doc:67168a6814 -->
### Nepali ma

yo Windows 11 / Command Prompt (cmd.exe) ko **adhikarik tayari prakriya** ho. din 1 bhanda aghi, paath
samayabahir mathibat kramaisang pura garnuhos. installation sakiepachhi tayari notebook kholnuhos.

Windows ko khojama "Command Prompt" wa `cmd` kholer suru garnuhos. File Explorer ma folder kholer
thegana barama `cmd` lekher Enter thichda pani khulchha. prashasak (Administrator) bannu aawashyak chhaina.

GitHub ko Code → Download ZIP nikalnuhos, wa Git chha bhane talako adesh chalaunuhos.

```cmd
cd /d "%USERPROFILE%\Documents"
git clone https://github.com/stefanoKS/Training_Automation.git
cd /d "%USERPROFILE%\Documents\Training_Automation\AI_Vision_Training"
dir
```

ZIP bhae nikaleko `AI_Vision_Training` folder ma januhos. abaka sabai adesh `README.md` ra `requirements`
bhaeko yahi folder ma chalaunuhos.

Documents OneDrive jasto any thaun ma sarieko chha bhane bastabik nikaleko thaun prayog garnuhos.
`cd /d "<actual extracted AI_Vision_Training path>"` ma <> bhitrako bhaag udaharan matra ho; jastako
tastai nachalai bastabik path le badalnuhos. udaharan:

```cmd
cd /d "D:\Training Materials\Training_Automation\AI_Vision_Training"
dir
cd
```

`dir` le bhitri samagri dekhaunchha, argument nabhaeko `cd` le ahileko thaun dekhaunchha. khali thaun bhaeko path pani
quote bhitr rakhnuhos.
<!-- ne:end -->

## ステップ 2　Python 3.11 を確認する / Check Python 3.11

```cmd
py -3.11 --version
```

検証済みの系列は **Python 3.11** です。3.12 など他の系列は未検証です。
詳細は [tested_versions.md](requirements/tested_versions.md) を参照してください。
`py` が無ければ python.org の Python 3.11 を入れ、Add python.exe to PATH を選び、
コマンド プロンプトを開き直します。`python --version` が 3.11 なら以後の `py -3.11` を
`python` に置き換えられます。

**Python 3.11** is the tested series; 3.12 and other series are unverified.
See [tested_versions.md](requirements/tested_versions.md). If `py` is missing, install
Python 3.11 from python.org, select Add python.exe to PATH, and reopen Command Prompt.
If `python --version` reports 3.11, substitute `python` for `py -3.11` below.

<!-- ne:begin doc:ba5e215a2b -->
### Nepali ma

```cmd
py -3.11 --version
```

janchieko series **Python 3.11** ho. 3.12 jasta any series janchieka chhainan.
bistrit kura [tested_versions.md](requirements/tested_versions.md) ma chha.
`py` chhaina bhane python.org baat Python 3.11 rakher Add python.exe to PATH chhannuhos ra Command Prompt feri
kholnuhos. `python --version` le 3.11 dekhayo bhane abaka `py -3.11` lai `python` le badalna sakinchha.
<!-- ne:end -->

## ステップ 3　基本環境を作る / Create the base environment

仮想環境は研修用の道具箱です。他の仕事の Python と分けます。
A virtual environment is a course toolbox, separate from Python used for other work.

```cmd
py -3.11 -m venv .venv
.\.venv\Scripts\activate.bat
where python
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
python -m pip install -r requirements\base.txt
python -m pip install -r requirements\yolo.txt
```

表示された Python の先頭がこのフォルダの `.venv\Scripts\python.exe` であることを確認します。
有効化できない場合は `python` の代わりに `".\.venv\Scripts\python.exe"` を使います。
例：`".\.venv\Scripts\python.exe" -m pip install -r requirements\base.txt`。
CMD の有効化に実行ポリシーの変更は不要です。組織の制限がある場合は講師・IT に相談します。

Check that the first Python listed belongs to this folder's `.venv\Scripts\python.exe`.
If activation is unavailable, replace `python` with `".\.venv\Scripts\python.exe"`.
For example: `".\.venv\Scripts\python.exe" -m pip install -r requirements\base.txt`.
CMD activation needs no execution-policy changes. Ask the instructor/IT about organisational restrictions.

<!-- ne:begin doc:830d6a3c17 -->
### Nepali ma

virtual environment bhaneko talimka lagi chhuttyaieko aujar-bakas ho. arko kaamko Python sang misindain.

```cmd
py -3.11 -m venv .venv
.\.venv\Scripts\activate.bat
where python
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
python -m pip install -r requirements\base.txt
python -m pip install -r requirements\yolo.txt
```

dekhieko Python ko pahilo thegana yahi folderko `.venv\Scripts\python.exe` ho ki jaanchnuhos.
sakriya (activate) garna nasakie `python` ko satta `".\.venv\Scripts\python.exe"` prayog garnuhos.
udaharan: `".\.venv\Scripts\python.exe" -m pip install -r requirements\base.txt`.
CMD sakriya garna execution policy paribartan aawashyak chhaina. sansthako bandej chha bhane prashikshak/IT sang sodhnuhos.
<!-- ne:end -->

## ステップ 4　Anomalib 環境を作る / Create the Anomalib environment

第5日は別の道具箱を使います。**標準手順では第1日前に両方を準備**します。
Day 5 uses another toolbox. **The default is to prepare both before Day 1.**

```cmd
deactivate
py -3.11 -m venv .venv-anomalib
.\.venv-anomalib\Scripts\activate.bat
where python
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
python -m pip install -r requirements\anomalib.txt
deactivate
```

有効化せず直接 Python を使っている場合は `deactivate` は不要です。
If you use Python executables directly, omit `deactivate`. For Day 5 use
`".\.venv-anomalib\Scripts\python.exe"` instead of `python`.

<!-- ne:begin doc:1f3f0467c0 -->
### Nepali ma

din 5 ma arko aujar-bakas prayog garinchha. **manak prakriyama din 1 bhanda aghi dubai tayar garinchha.**

```cmd
deactivate
py -3.11 -m venv .venv-anomalib
.\.venv-anomalib\Scripts\activate.bat
where python
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
python -m pip install -r requirements\anomalib.txt
deactivate
```

sakriya nagari sidhai Python prayog gariraheko chha bhane `deactivate` aawashyak chhaina. din 5 ka lagi `python` ko satta
`".\.venv-anomalib\Scripts\python.exe"` prayog garnuhos.
<!-- ne:end -->

## ステップ 5　両方のカーネルを登録する / Register both kernels

カーネルはノートブックのコードを実行する Python です。
A kernel is the Python process that executes notebook code.

```cmd
".\.venv\Scripts\python.exe" -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
".\.venv-anomalib\Scripts\python.exe" -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

<!-- ne:begin doc:250dba12d0 -->
### Nepali ma

kernel bhaneko notebookko kod chalaune Python ho.

```cmd
".\.venv\Scripts\python.exe" -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
".\.venv-anomalib\Scripts\python.exe" -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```
<!-- ne:end -->

## ステップ 6　教材とデータを作る / Generate teaching assets and datasets

ここからは有効化せず、**基本環境 `.venv` の Python を直接指定**します。`--force` や `--clean` は不要です。
既存の提出物や保存済みモデル出力を再生成しません。

From here, call **the base `.venv` Python directly**, without activation. Do not use `--force` or `--clean`. Do not regenerate
student submissions or saved model outputs.

```cmd
".\.venv\Scripts\python.exe" assets\scripts\generate_training_assets.py
".\.venv\Scripts\python.exe" assets\scripts\prepare_datasets.py
".\.venv\Scripts\python.exe" assets\scripts\generate_teaching_diagrams.py
".\.venv\Scripts\python.exe" assets\scripts\generate_svg_figures.py
```

<!-- ne:begin doc:72b74d0a89 -->
### Nepali ma

yahan baat sakriya nagari **adharabhut batabaran `.venv` ko Python sidhai** dinuhos. `--force` wa `--clean`
aawashyak chhaina. bujhaisakeka kaam wa surakshit model natija feri banaindain.

```cmd
".\.venv\Scripts\python.exe" assets\scripts\generate_training_assets.py
".\.venv\Scripts\python.exe" assets\scripts\prepare_datasets.py
".\.venv\Scripts\python.exe" assets\scripts\generate_teaching_diagrams.py
".\.venv\Scripts\python.exe" assets\scripts\generate_svg_figures.py
```
<!-- ne:end -->

## ステップ 7　オフライン授業の素材を先に取得する / Preload offline lesson inputs

参考写真はライセンス付きの原本です。合成画像や工場の実測結果ではありません。
重みも授業前に取得します。初回はネットワークが必要です。

Reference photographs are licensed originals, not synthetic images or factory measurements.
Download weights before lessons too. The initial download needs network access.

```cmd
".\.venv\Scripts\python.exe" assets\scripts\download_reference_images.py --course-root .
".\.venv\Scripts\python.exe" assets\scripts\preload_models.py --profile yolo
".\.venv-anomalib\Scripts\python.exe" assets\scripts\preload_models.py --profile anomalib
".\.venv\Scripts\python.exe" assets\scripts\download_reference_images.py --course-root . --offline
".\.venv\Scripts\python.exe" assets\scripts\preload_models.py --profile yolo --offline
".\.venv-anomalib\Scripts\python.exe" assets\scripts\preload_models.py --profile anomalib --offline
```

重みの配布・使用条件は提供元（Ultralytics / timm / torchvision）を確認してください。
取得に失敗したら授業前に講師へ連絡します。参考結果は
`assets/reference_outputs/`、受講者が実行して保存する結果は `submissions/` です。

Check the providers' licence terms (Ultralytics / timm / torchvision) before redistribution/use.
Report download failures before class. Supplied references live in `assets/reference_outputs/`;
students' live outputs go into `submissions/`.

<!-- ne:begin doc:9fbc66bc33 -->
### Nepali ma

sandarbha photo laisens bhaeka mul file hun. kritrim chitra wa karakhanako maapan natija hoinan.
model ko weight pani paath aghi lyainchha. pahilo patak network chahinchha.

```cmd
".\.venv\Scripts\python.exe" assets\scripts\download_reference_images.py --course-root .
".\.venv\Scripts\python.exe" assets\scripts\preload_models.py --profile yolo
".\.venv-anomalib\Scripts\python.exe" assets\scripts\preload_models.py --profile anomalib
".\.venv\Scripts\python.exe" assets\scripts\download_reference_images.py --course-root . --offline
".\.venv\Scripts\python.exe" assets\scripts\preload_models.py --profile yolo --offline
".\.venv-anomalib\Scripts\python.exe" assets\scripts\preload_models.py --profile anomalib --offline
```

weight ko bitaran ra prayogka sart dine nikay (Ultralytics / timm / torchvision) baat jaanchnuhos.
lina asaphal bhae paath aghi prashikshakalai khabar garnuhos. diieka sandarbha natija `assets/reference_outputs/`
ma chhan; prashiksharthile chalaer surakshit garne natija `submissions/` ma janchha.
<!-- ne:end -->

## ステップ 8　環境と教材を確認する / Verify environments and assets

`--profile all` は**実行した環境だけ**を検査します。両方で実行してください。
`--profile all` checks **only the current environment**. Run it in both.

```cmd
".\.venv\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv-anomalib\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv\Scripts\python.exe" assets\scripts\validate_notebooks.py
".\.venv\Scripts\python.exe" -m jupyter kernelspec list
```

終了コード 0 に加え、表示された素材の不足がないことも確認します。
Check exit code 0 **and** that the printed asset list contains no missing items.

<!-- ne:begin doc:520ff2c5c4 -->
### Nepali ma

`--profile all` le **chalaieko batabaran matra** janchchha. dubaima chalaunuhos.

```cmd
".\.venv\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv-anomalib\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv\Scripts\python.exe" assets\scripts\validate_notebooks.py
".\.venv\Scripts\python.exe" -m jupyter kernelspec list
```

exit code 0 sangai dekhaieko samagriko soochi ma kunai napug bhaag nabhaeko pani jaanchnuhos.
<!-- ne:end -->

## ステップ 9　JupyterLab を起動する / Launch JupyterLab

基本環境を有効化してから起動します。別の Python の `jupyter-lab` が選ばれるのを防ぎます。
この CMD ウィンドウだけの変更です。

Activate the base environment before launch so Jupyter cannot select another Python's
`jupyter-lab` executable. This affects only this CMD window.

```cmd
.\.venv\Scripts\activate.bat
".\.venv\Scripts\python.exe" -m jupyter lab
```

日々の起動は、このフォルダの `start_training.cmd` をダブルクリックしても同じです。
この起動用ファイルは準備済みの環境を使うだけで、インストール・素材取得・学習はしません。

For daily use, double-click `start_training.cmd` in this folder instead. It uses the prepared
environment only; it does not install, download assets or train models.

ブラウザが開かなければ表示された localhost の URL を開きます。
`notebooks` → `00_Setup` → `00_Environment_Setup.ipynb` を開き、
`Python 3 (AI Vision)` を選びます。第5日だけ `Python 3 (AI Vision Anomalib)` を選びます。

If no browser opens, open the printed localhost URL. Open
`notebooks` → `00_Setup` → `00_Environment_Setup.ipynb`, select `Python 3 (AI Vision)`.
Only Day 5 uses `Python 3 (AI Vision Anomalib)`.

<!-- ne:begin doc:790f812b79 -->
### Nepali ma

adharabhut batabaran sakriya garepachhi matra suru garnuhos. arko Python ko `jupyter-lab` chhaninabat jogaunchha.
paribartan yo CMD jhyalama matra lagu hunchha.

```cmd
.\.venv\Scripts\activate.bat
".\.venv\Scripts\python.exe" -m jupyter lab
```

dainik suru garna yahi folderko `start_training.cmd` dabal-klik gare pani uhi hunchha.
yo suru garne filele tayar bhaisakeko batabaran prayog garchha matra; install, samagri line wa train garne kaam
gardaina.

braujar nakhule dekhaieko localhost URL kholnuhos. `notebooks` → `00_Setup` →
`00_Environment_Setup.ipynb` kholer `Python 3 (AI Vision)` chhannuhos. din 5 ma matra
`Python 3 (AI Vision Anomalib)` chhaninchha.
<!-- ne:end -->

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

<!-- ne:begin doc:334c6e4167 -->
### Nepali ma

din 1 bhanda aghi tayari notebook mathibat kramaisang chalaunuhos. janajan rakhieko trutiko abhyas byakhya anusar
sudharnuhos. din 1 ko 09:00–09:10 tayar bhaisakeko abastha punah jaanchne samay ho, installation ko samay hoina.

- [ ] dubai kernel chhanna sakinchha
- [ ] dubai batabaranko jaanch saphal bhayo, samagri ma kunai napug chhaina
- [ ] aphalain photo ra weight ko jaanch saphal bhayo
- [ ] Day01_02 Part 1 ma chitra dekhinchha
- [ ] chitrako Japani akshar bargama parinat bhaeko chhaina
- [ ] `submissions/day00/` ma tayari riport surakshit gariyo

samayamai nabhyae [COURSE_SYLLABUS.md](COURSE_SYLLABUS.md) ko punahsthapan prakriya prayog garnuhos.
<!-- ne:end -->

## ステップ 11　授業を始める / Start lessons

セルを選んで Shift+Enter、保存は Ctrl+S。セルは上から順番に実行します。
値はカーネルに残ります。順序を見失ったら Kernel → Restart Kernel and Run All Cells。
翌日はステップ1のフォルダに移動し、ステップ9で起動します。環境は作り直しません。
終了時は保存してブラウザを閉じ、コマンド プロンプトで Ctrl+C を押して停止を確認します。

Select a cell and press Shift+Enter; Ctrl+S saves. Run top to bottom. Values persist in the
kernel. If confused, use Kernel → Restart Kernel and Run All Cells.
Next day return to the Step 1 folder and launch with Step 9; do not recreate environments.
To finish, save, close the browser, then stop Jupyter with Ctrl+C in Command Prompt.

<!-- ne:begin doc:e09ed05ae5 -->
### Nepali ma

cell chhaner Shift+Enter, surakshit garna Ctrl+S. cell mathibat kramaisang chalaunuhos.
maan kernel ma rahanchha. kram birsiyo bhane Kernel → Restart Kernel and Run All Cells prayog garnuhos.
bholiko din step 1 ko folder ma gaer step 9 baat suru garnuhos. batabaran feri banaindain.
sakda surakshit garera braujar banda garnuhos, ra Command Prompt ma Ctrl+C thicher rokieko pushti garnuhos.
<!-- ne:end -->

### 例外：第4日後の Anomalib 準備 / Alternative: Anomalib setup after Day 4

講師が明示的に許可した場合のみ、ステップ4と Anomalib の登録・重み取得・検査を第4日後に
延期できます。この場合、第1日の確認は基本環境のみで、**全日程の準備完了とは言いません**。
第5日前に残りを完了します。標準の両環境チェックリストとは別の例外です。

Only with explicit instructor approval may Step 4 and Anomalib registration/preload/verification
wait until after Day 4. Then Day 1 checks only the base environment; **full-course readiness is
not achieved**. Finish the remaining checks before Day 5. This is an exception, not the default.

<!-- ne:begin doc:d0fff85723 -->
### Nepali ma

prashikshakale spasht anumati dieko abastha ma matra step 4 ra Anomalib ko darta, weight line ra jaanch din 4
pachhi sarn sakinchha. tyas abastha ma din 1 ko jaanch adharabhut batabaran ma matra hunchha ra **purai talim tayar chha**
bhann mildaina. din 5 aghi banki kaam pura garnuhos. yo manak dubai-batabaran janchasuchibhanda chhuttai apabad ho.
<!-- ne:end -->

### 困ったとき / Troubleshooting

| 症状 / Symptom | 対処 / Action |
|---|---|
| `python` / `py` が無い / missing | ステップ2。PATH・アプリ実行エイリアスを確認 / Step 2, check PATH and app aliases |
| パッケージ不足 / missing package | 正しい環境で requirements を入れる / install requirements in the correct environment |
| カーネルが違う / wrong kernel | `import sys; print(sys.executable)` を Python セルで確認 / check in a Python cell |
| 有効化が禁止 / activation blocked | ステップ3の直接実行を使う / use Step 3's direct executable |
| 重みが無い / missing weights | ステップ7を再実行し、失敗を記録 / rerun Step 7 and record the failure |

コマンド プロンプトの `python -m pip` と、ノートブック専用の Jupyter `%pip` は別物です。
授業中の自動インストールはしません。詳細は [installation.md](docs/troubleshooting/installation.md)。

Command Prompt `python -m pip` and notebook-only Jupyter `%pip` are different.
Lessons do not install automatically. See [installation.md](docs/troubleshooting/installation.md).

<!-- ne:begin doc:3a2254859c -->
### Nepali ma

| lakshan | ke garne |
|---|---|
| `python` / `py` chhaina | step 2. PATH ra app execution aliases jaanchnuhos |
| package napug | sahi batabaran ma requirements rakhnuhos |
| kernel farak chha | Python cell ma `import sys; print(sys.executable)` jaanchnuhos |
| sakriya garna manahi chha | step 3 ko sidhai chalaune tarika prayog garnuhos |
| weight chhaina | step 7 feri chalaer asaphalata abhilekh garnuhos |

Command Prompt ko `python -m pip` ra notebookka lagi matrako Jupyter `%pip` farak kura hun.
paath chalirahanda sbatah install garindain. bistrit kura
[installation.md](docs/troubleshooting/installation.md) ma chha.
<!-- ne:end -->
