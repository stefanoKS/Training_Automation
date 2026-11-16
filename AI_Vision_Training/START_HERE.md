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
### नेपालीमा

यो Windows 11 / Command Prompt (cmd.exe) को **आधिकारिक तयारी प्रक्रिया** हो। दिन १ भन्दा अघि, पाठ
समयबाहिर माथिबाट क्रमैसँग पूरा गर्नुहोस्। installation सकिएपछि तयारी नोटबुक खोल्नुहोस्।

Windows को खोजमा "Command Prompt" वा `cmd` खोलेर सुरु गर्नुहोस्। File Explorer मा फोल्डर खोलेर
ठेगाना बारमा `cmd` लेखेर Enter थिच्दा पनि खुल्छ। प्रशासक (Administrator) बन्नु आवश्यक छैन।

GitHub को Code → Download ZIP निकाल्नुहोस्, वा Git छ भने तलको आदेश चलाउनुहोस्।

```cmd
cd /d "%USERPROFILE%\Documents"
git clone https://github.com/stefanoKS/Training_Automation.git
cd /d "%USERPROFILE%\Documents\Training_Automation\AI_Vision_Training"
dir
```

ZIP भए निकालेको `AI_Vision_Training` फोल्डरमा जानुहोस्। अबका सबै आदेश `README.md` र `requirements`
भएको यही फोल्डरमा चलाउनुहोस्।

Documents OneDrive जस्तो अन्य ठाउँमा सारिएको छ भने वास्तविक निकालेको ठाउँ प्रयोग गर्नुहोस्।
`cd /d "<actual extracted AI_Vision_Training path>"` मा <> भित्रको भाग उदाहरण मात्र हो; जस्ताको
तस्तै नचलाई वास्तविक path ले बदल्नुहोस्। उदाहरण:

```cmd
cd /d "D:\Training Materials\Training_Automation\AI_Vision_Training"
dir
cd
```

`dir` ले भित्री सामग्री देखाउँछ, argument नभएको `cd` ले अहिलेको ठाउँ देखाउँछ। खाली ठाउँ भएको path पनि
quote भित्र राख्नुहोस्।
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
### नेपालीमा

```cmd
py -3.11 --version
```

जाँचिएको series **Python 3.11** हो। 3.12 जस्ता अन्य series जाँचिएका छैनन्।
विस्तृत कुरा [tested_versions.md](requirements/tested_versions.md) मा छ।
`py` छैन भने python.org बाट Python 3.11 राखेर Add python.exe to PATH छान्नुहोस् र Command Prompt फेरि
खोल्नुहोस्। `python --version` ले 3.11 देखायो भने अबका `py -3.11` लाई `python` ले बदल्न सकिन्छ।
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
### नेपालीमा

virtual environment भनेको तालिमका लागि छुट्ट्याइएको औजार-बाकस हो। अर्को कामको Python सँग मिसिँदैन।

```cmd
py -3.11 -m venv .venv
.\.venv\Scripts\activate.bat
where python
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
python -m pip install -r requirements\base.txt
python -m pip install -r requirements\yolo.txt
```

देखिएको Python को पहिलो ठेगाना यही फोल्डरको `.venv\Scripts\python.exe` हो कि जाँच्नुहोस्।
सक्रिय (activate) गर्न नसकिए `python` को सट्टा `".\.venv\Scripts\python.exe"` प्रयोग गर्नुहोस्।
उदाहरण: `".\.venv\Scripts\python.exe" -m pip install -r requirements\base.txt`।
CMD सक्रिय गर्न execution policy परिवर्तन आवश्यक छैन। संस्थाको बन्देज छ भने प्रशिक्षक/IT सँग सोध्नुहोस्।
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
### नेपालीमा

दिन ५ मा अर्को औजार-बाकस प्रयोग गरिन्छ। **मानक प्रक्रियामा दिन १ भन्दा अघि दुवै तयार गरिन्छ।**

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

सक्रिय नगरी सिधै Python प्रयोग गरिरहेको छ भने `deactivate` आवश्यक छैन। दिन ५ का लागि `python` को सट्टा
`".\.venv-anomalib\Scripts\python.exe"` प्रयोग गर्नुहोस्।
<!-- ne:end -->

## ステップ 5　両方のカーネルを登録する / Register both kernels

カーネルはノートブックのコードを実行する Python です。
A kernel is the Python process that executes notebook code.

```cmd
".\.venv\Scripts\python.exe" -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
".\.venv-anomalib\Scripts\python.exe" -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

<!-- ne:begin doc:250dba12d0 -->
### नेपालीमा

kernel भनेको नोटबुकको कोड चलाउने Python हो।

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
### नेपालीमा

यहाँबाट सक्रिय नगरी **आधारभूत वातावरण `.venv` को Python सिधै** दिनुहोस्। `--force` वा `--clean`
आवश्यक छैन। बुझाइसकेका काम वा सुरक्षित model नतिजा फेरि बनाइँदैन।

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
### नेपालीमा

सन्दर्भ फोटो लाइसेन्स भएका मूल फाइल हुन्। कृत्रिम चित्र वा कारखानाको मापन नतिजा होइनन्।
model को weight पनि पाठ अघि ल्याइन्छ। पहिलो पटक network चाहिन्छ।

```cmd
".\.venv\Scripts\python.exe" assets\scripts\download_reference_images.py --course-root .
".\.venv\Scripts\python.exe" assets\scripts\preload_models.py --profile yolo
".\.venv-anomalib\Scripts\python.exe" assets\scripts\preload_models.py --profile anomalib
".\.venv\Scripts\python.exe" assets\scripts\download_reference_images.py --course-root . --offline
".\.venv\Scripts\python.exe" assets\scripts\preload_models.py --profile yolo --offline
".\.venv-anomalib\Scripts\python.exe" assets\scripts\preload_models.py --profile anomalib --offline
```

weight को वितरण र प्रयोगका सर्त दिने निकाय (Ultralytics / timm / torchvision) बाट जाँच्नुहोस्।
लिन असफल भए पाठ अघि प्रशिक्षकलाई खबर गर्नुहोस्। दिइएका सन्दर्भ नतिजा `assets/reference_outputs/`
मा छन्; प्रशिक्षार्थीले चलाएर सुरक्षित गर्ने नतिजा `submissions/` मा जान्छ।
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
### नेपालीमा

`--profile all` ले **चलाइएको वातावरण मात्र** जाँच्छ। दुवैमा चलाउनुहोस्।

```cmd
".\.venv\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv-anomalib\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv\Scripts\python.exe" assets\scripts\validate_notebooks.py
".\.venv\Scripts\python.exe" -m jupyter kernelspec list
```

exit code 0 सँगै देखाइएको सामग्रीको सूचीमा कुनै नपुग भाग नभएको पनि जाँच्नुहोस्।
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
### नेपालीमा

आधारभूत वातावरण सक्रिय गरेपछि मात्र सुरु गर्नुहोस्। अर्को Python को `jupyter-lab` छानिनबाट जोगाउँछ।
परिवर्तन यो CMD झ्यालमा मात्र लागू हुन्छ।

```cmd
.\.venv\Scripts\activate.bat
".\.venv\Scripts\python.exe" -m jupyter lab
```

दैनिक सुरु गर्न यही फोल्डरको `start_training.cmd` डबल-क्लिक गरे पनि उही हुन्छ।
यो सुरु गर्ने फाइलले तयार भइसकेको वातावरण प्रयोग गर्छ मात्र; install, सामग्री लिने वा train गर्ने काम
गर्दैन।

ब्राउजर नखुले देखाइएको localhost URL खोल्नुहोस्। `notebooks` → `00_Setup` →
`00_Environment_Setup.ipynb` खोलेर `Python 3 (AI Vision)` छान्नुहोस्। दिन ५ मा मात्र
`Python 3 (AI Vision Anomalib)` छानिन्छ।
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
### नेपालीमा

दिन १ भन्दा अघि तयारी नोटबुक माथिबाट क्रमैसँग चलाउनुहोस्। जानाजान राखिएको त्रुटिको अभ्यास व्याख्याअनुसार
सुधार्नुहोस्। दिन १ को 09:00–09:10 तयार भइसकेको अवस्था पुनः जाँच्ने समय हो, installation को समय होइन।

- [ ] दुवै kernel छान्न सकिन्छ
- [ ] दुवै वातावरणको जाँच सफल भयो, सामग्रीमा कुनै नपुग छैन
- [ ] अफलाइन फोटो र weight को जाँच सफल भयो
- [ ] Day01_02 Part 1 मा चित्र देखिन्छ
- [ ] चित्रको जापानी अक्षर वर्गमा परिणत भएको छैन
- [ ] `submissions/day00/` मा तयारी रिपोर्ट सुरक्षित गरियो

समयमै नभ्याए [COURSE_SYLLABUS.md](COURSE_SYLLABUS.md) को पुनःस्थापन प्रक्रिया प्रयोग गर्नुहोस्।
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
### नेपालीमा

सेल छानेर Shift+Enter, सुरक्षित गर्न Ctrl+S। सेल माथिबाट क्रमैसँग चलाउनुहोस्।
मान kernel मा रहन्छ। क्रम बिर्सियो भने Kernel → Restart Kernel and Run All Cells प्रयोग गर्नुहोस्।
भोलिको दिन स्टेप 1 को फोल्डरमा गएर स्टेप 9 बाट सुरु गर्नुहोस्। वातावरण फेरि बनाइँदैन।
सक्दा सुरक्षित गरेर ब्राउजर बन्द गर्नुहोस्, र Command Prompt मा Ctrl+C थिचेर रोकिएको पुष्टि गर्नुहोस्।
<!-- ne:end -->

### 例外：第4日後の Anomalib 準備 / Alternative: Anomalib setup after Day 4

講師が明示的に許可した場合のみ、ステップ4と Anomalib の登録・重み取得・検査を第4日後に
延期できます。この場合、第1日の確認は基本環境のみで、**全日程の準備完了とは言いません**。
第5日前に残りを完了します。標準の両環境チェックリストとは別の例外です。

Only with explicit instructor approval may Step 4 and Anomalib registration/preload/verification
wait until after Day 4. Then Day 1 checks only the base environment; **full-course readiness is
not achieved**. Finish the remaining checks before Day 5. This is an exception, not the default.

<!-- ne:begin doc:d0fff85723 -->
### नेपालीमा

प्रशिक्षकले स्पष्ट अनुमति दिएको अवस्थामा मात्र स्टेप 4 र Anomalib को दर्ता, weight लिने र जाँच दिन ४
पछि सार्न सकिन्छ। त्यस अवस्थामा दिन १ को जाँच आधारभूत वातावरणमा मात्र हुन्छ र **पूरै तालिम तयार छ**
भन्न मिल्दैन। दिन ५ अघि बाँकी काम पूरा गर्नुहोस्। यो मानक दुवै-वातावरण जाँचसूचीभन्दा छुट्टै अपवाद हो।
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
### नेपालीमा

| लक्षण | के गर्ने |
|---|---|
| `python` / `py` छैन | स्टेप 2। PATH र app execution aliases जाँच्नुहोस् |
| package नपुग | सही वातावरणमा requirements राख्नुहोस् |
| kernel फरक छ | Python सेलमा `import sys; print(sys.executable)` जाँच्नुहोस् |
| सक्रिय गर्न मनाही छ | स्टेप 3 को सिधै चलाउने तरिका प्रयोग गर्नुहोस् |
| weight छैन | स्टेप 7 फेरि चलाएर असफलता अभिलेख गर्नुहोस् |

Command Prompt को `python -m pip` र नोटबुकका लागि मात्रको Jupyter `%pip` फरक कुरा हुन्।
पाठ चलिरहँदा स्वतः install गरिँदैन। विस्तृत कुरा
[installation.md](docs/troubleshooting/installation.md) मा छ।
<!-- ne:end -->
