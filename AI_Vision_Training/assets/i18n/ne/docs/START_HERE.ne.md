<!--
Nepali anuwad / Nepali translation source for
START_HERE.md

Each block is keyed on the exact heading line it belongs to; the Nepali text is appended at the end
of that section. Commands, paths and file names stay byte-identical.
-->
# START_HERE — Nepali anuwad

<!-- ne-doc: START_HERE.md -->

<!-- ne-section: ## ステップ 1　取得してフォルダを開く / Download and open the folder -->
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

<!-- ne-section: ## ステップ 2　Python 3.11 を確認する / Check Python 3.11 -->
### Nepali ma

```cmd
py -3.11 --version
```

janchieko series **Python 3.11** ho. 3.12 jasta any series janchieka chhainan.
bistrit kura [tested_versions.md](requirements/tested_versions.md) ma chha.
`py` chhaina bhane python.org baat Python 3.11 rakher Add python.exe to PATH chhannuhos ra Command Prompt feri
kholnuhos. `python --version` le 3.11 dekhayo bhane abaka `py -3.11` lai `python` le badalna sakinchha.

<!-- ne-section: ## ステップ 3　基本環境を作る / Create the base environment -->
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

<!-- ne-section: ## ステップ 4　Anomalib 環境を作る / Create the Anomalib environment -->
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

<!-- ne-section: ## ステップ 5　両方のカーネルを登録する / Register both kernels -->
### Nepali ma

kernel bhaneko notebookko kod chalaune Python ho.

```cmd
".\.venv\Scripts\python.exe" -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
".\.venv-anomalib\Scripts\python.exe" -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

<!-- ne-section: ## ステップ 6　教材とデータを作る / Generate teaching assets and datasets -->
### Nepali ma

yahan baat sakriya nagari **adharabhut batabaran `.venv` ko Python sidhai** dinuhos. `--force` wa `--clean`
aawashyak chhaina. bujhaisakeka kaam wa surakshit model natija feri banaindain.

```cmd
".\.venv\Scripts\python.exe" assets\scripts\generate_training_assets.py
".\.venv\Scripts\python.exe" assets\scripts\prepare_datasets.py
".\.venv\Scripts\python.exe" assets\scripts\generate_teaching_diagrams.py
".\.venv\Scripts\python.exe" assets\scripts\generate_svg_figures.py
```

<!-- ne-section: ## ステップ 7　オフライン授業の素材を先に取得する / Preload offline lesson inputs -->
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

<!-- ne-section: ## ステップ 8　環境と教材を確認する / Verify environments and assets -->
### Nepali ma

`--profile all` le **chalaieko batabaran matra** janchchha. dubaima chalaunuhos.

```cmd
".\.venv\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv-anomalib\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv\Scripts\python.exe" assets\scripts\validate_notebooks.py
".\.venv\Scripts\python.exe" -m jupyter kernelspec list
```

exit code 0 sangai dekhaieko samagriko soochi ma kunai napug bhaag nabhaeko pani jaanchnuhos.

<!-- ne-section: ## ステップ 9　JupyterLab を起動する / Launch JupyterLab -->
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

<!-- ne-section: ## ステップ 10　準備完了を確認する / Complete preflight -->
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

<!-- ne-section: ## ステップ 11　授業を始める / Start lessons -->
### Nepali ma

cell chhaner Shift+Enter, surakshit garna Ctrl+S. cell mathibat kramaisang chalaunuhos.
maan kernel ma rahanchha. kram birsiyo bhane Kernel → Restart Kernel and Run All Cells prayog garnuhos.
bholiko din step 1 ko folder ma gaer step 9 baat suru garnuhos. batabaran feri banaindain.
sakda surakshit garera braujar banda garnuhos, ra Command Prompt ma Ctrl+C thicher rokieko pushti garnuhos.

<!-- ne-section: ### 例外：第4日後の Anomalib 準備 / Alternative: Anomalib setup after Day 4 -->
### Nepali ma

prashikshakale spasht anumati dieko abastha ma matra step 4 ra Anomalib ko darta, weight line ra jaanch din 4
pachhi sarn sakinchha. tyas abastha ma din 1 ko jaanch adharabhut batabaran ma matra hunchha ra **purai talim tayar chha**
bhann mildaina. din 5 aghi banki kaam pura garnuhos. yo manak dubai-batabaran janchasuchibhanda chhuttai apabad ho.

<!-- ne-section: ### 困ったとき / Troubleshooting -->
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
