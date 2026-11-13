# はじめかた / START HERE

このファイルは、**パソコンの電源を入れるところから**始める方向けの手順書です。
むずかしい言葉はできるだけ避けて書いています。上から順番に進めてください。

This is the **from-switching-the-PC-on** guide. It avoids jargon wherever possible.
Work through it from top to bottom.

---

## ステップ 0　この手順書のゴール / Goal of this guide

ゴールは 1 つだけです。

> `notebooks/00_Setup/00_Environment_Setup.ipynb` を開いて、最後までエラーなく実行できること。

There is exactly one goal: open
`notebooks/00_Setup/00_Environment_Setup.ipynb` and run it to the end without errors.

---

## ステップ 1　フォルダを確認する / Check the folder

`AI_Vision_Training` フォルダを、次の場所に置いてください。

```text
C:\Users\<あなたの名前>\Documents\AI_Vision_Training
```

デスクトップやダウンロードのままでも動きますが、**Documents** を推奨します。
あとで探しやすく、パスも短くなるからです。

Put the `AI_Vision_Training` folder under
`C:\Users\<your-name>\Documents\`. It also works from the Desktop or Downloads, but Documents is
recommended: it is easier to find and keeps the path short.

---

## ステップ 2　PowerShell を開く / Open PowerShell

画面下の検索欄に `PowerShell` と入力し、出てきた **Windows PowerShell** をクリックします。

黒い（または青い）窓が開きます。これが **ターミナル** です。

Type `PowerShell` in the Windows search box and click **Windows PowerShell**.
A dark (or blue) window opens. That is the **terminal**.

> マウスでクリックする代わりに、**文字で** コンピュータに命令する窓です。
> It is the window where you type instructions instead of clicking.

---

## ステップ 3　フォルダに移動する / Move into the folder

次の 1 行をコピーして、PowerShell に貼り付け、`Enter` を押します。

Copy the following single line, paste it into PowerShell and press `Enter`.

```powershell
cd "$HOME\Documents\AI_Vision_Training"
```

うまくいかない場合は、自分のユーザー名を直接書きます。

If that does not work, type your user name explicitly:

```powershell
cd "C:\Users\あなたの名前\Documents\AI_Vision_Training"
```

正しく移動できたか確認します。

Check that you are in the right place:

```powershell
pwd
Get-ChildItem
```

`README.md` と `notebooks` が見えれば成功です。
If you can see `README.md` and `notebooks`, you are in the right folder.

---

## ステップ 4　Python があるか確認する / Check Python

```powershell
python --version
```

`Python 3.11.x` または `Python 3.12.x` と表示されれば OK です。

| 表示 / What you see | 意味 / Meaning | 対処 / What to do |
|---|---|---|
| `Python 3.11.9` | 正常 / fine | 次へ / continue |
| `Python was not found` | 入っていない / not installed | 下の「Python の入れ方」 / see below |
| Microsoft Store が開く / the Store opens | Windows の機能 / Windows alias | 設定 →「アプリ実行エイリアス」→ `python.exe` をオフ / Settings -> App execution aliases -> turn `python.exe` off |

### Python の入れ方（必要な場合のみ）/ Installing Python (only if needed)

[python.org](https://www.python.org/downloads/) を開き、**Python 3.11** を選びます。

**必ず** インストーラの最初の画面で

- ☑ **Add python.exe to PATH**

にチェックを入れ、「Install Now」を押します。**このチェックを忘れると動きません。**

Open [python.org](https://www.python.org/downloads/) and choose **Python 3.11**.
On the first installer screen you **must** tick "**Add python.exe to PATH**", then click "Install Now".
Forgetting that tick is the most common cause of failure.

入れ終わったら PowerShell を **閉じて、もう一度開き**、`python --version` を確認してください。
Afterwards **close and reopen** PowerShell and check `python --version` again.

---

## ステップ 5　仮想環境を作る / Create the virtual environment

**仮想環境** は「この研修専用の道具箱」です。作っておくと、
他の仕事の Python を壊しません。

A **virtual environment** is a private toolbox for this course. It keeps you from
breaking the Python used by other work.

```powershell
python -m venv .venv
```

何も表示されなければ成功です（1〜2 分かかります）。

Success is silent; it takes a minute or two.

次に、この道具箱を **使う状態** にします。

Now switch the toolbox on:

```powershell
.\.venv\Scripts\Activate.ps1
```

プロンプトの先頭に `(.venv)` が付きます。

```text
(.venv) PS C:\Users\あなたの名前\Documents\AI_Vision_Training>
```

The prompt now starts with `(.venv)`.

**エラーが出た場合 / If it fails**

```text
Activate.ps1 cannot be loaded because running scripts is disabled
```

次の 1 行を実行し、`Y` を押してから、もう一度 `Activate.ps1` を実行します。
Run the line below, answer `Y`, then activate again.

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

## ステップ 6　必要なものを入れる / Install the packages

`(.venv)` が付いた状態で、上から順に実行します。**数分かかります。**

With `(.venv)` visible, run these in order. It takes several minutes.

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements\base.txt
python -m pip install -r requirements\yolo.txt
python -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
```

最後の `ipykernel install` は「この道具箱を、Jupyter から選べるように登録する」作業です。
**これを忘れると、Jupyter から研修用の環境が見えません。**

The last line registers this environment so Jupyter can offer it as a kernel.
**Skip it and Jupyter will not see the course environment.**

エラーで止まったら、**同じコマンドをもう一度実行** してください。
ネットワークの一時的な失敗がほとんどです。何度も失敗する場合は講師に連絡してください。

If a command fails, **run the same command again**; transient network errors are common.
Contact the instructor if it keeps failing.

---

## ステップ 7　第1日の準備確認 / Day 1 readiness check

ここまで終わったら、第1日の朝 09:00–09:10 の 10 分で次の 4 つを確認します。
**全部そろってから第1日を始めます。** 準備を授業時間に持ち込むと、その日の必須学習が入りません。

At 09:00-09:10 on Day 1 you check these four items. **Day 1 starts when they all pass.**
Carrying setup into lesson time means the required work no longer fits.

| チェック / Check | 合格の条件 / Passes when |
|---|---|
| カーネル / kernels | 「Python 3 (AI Vision)」と「Python 3 (AI Vision Anomalib)」の両方が一覧に出る |
| ライブラリ / libraries | `python assets\scripts\verify_environment.py --profile all` が 0 で終わる |
| 画像 / images | `Day01_02` の Part 1 が画像を 1 枚表示できる |
| フォント / font | 図のタイトルに `□` が出ない |

**準備が終わらなかった場合 / If it is not finished:**

`COURSE_SYLLABUS.md` の「準備が終わらなかった場合」に、3 つの現実的な選択肢を書いてあります。
ごまかさず、そのどれかを選んでください。

Three realistic recovery options are listed in `COURSE_SYLLABUS.md` under "if preflight is not
finished". Do not pretend; choose one of them.

---

## ステップ 7　（第5日の前に）2つ目の環境を作る / Create the second environment (before Day 5)

**第 5 日だけ** 別の道具箱を使います。第 4 日が終わってからで構いません。

**Day 5 only** uses a second toolbox. You can do this after Day 4.

```powershell
python -m venv .venv-anomalib
.\.venv-anomalib\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements\anomalib.txt
python -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

なぜ分けるのかは [`README.md`](README.md) の 3 節に書いています。
Section 3 of `README.md` explains why they are separate.

---

## ステップ 8　素材を作る / Generate the assets

画像・図・データセットを生成します（`(.venv)` の状態で）。

Generate the images, diagrams and datasets (with `(.venv)` active).

```powershell
python assets\scripts\generate_training_assets.py
python assets\scripts\prepare_datasets.py
```

`Done.` と表示されれば成功です。
You should see `Done.`

---

## ステップ 9　JupyterLab を起動する / Start JupyterLab

```powershell
jupyter lab
```

ブラウザが自動で開きます。開かない場合は、PowerShell に表示された
`http://localhost:8888/...` の URL をブラウザに貼り付けてください。

Your browser opens automatically. If not, copy the `http://localhost:8888/...` URL from
PowerShell into the browser.

画面の左にファイル一覧が出ます。`notebooks` → `00_Setup` →
`00_Environment_Setup.ipynb` の順にクリックして開いてください。

A file list appears on the left. Click `notebooks` -> `00_Setup` ->
`00_Environment_Setup.ipynb`.

---

## ステップ 10　ノートブックの操作 / Working with a notebook

| 操作 / Action | やり方 / How |
|---|---|
| セルを実行 / run a cell | セルを選び、`Shift` + `Enter` |
| セルを追加 / add a cell | 上の `+` ボタン / the `+` button |
| カーネルを選ぶ / choose the kernel | 右上のカーネル名 → `Python 3 (AI Vision)` |
| カーネルを再起動 / restart | 上部メニュー `Kernel` → `Restart Kernel and Run All Cells` |
| 保存 / save | `Ctrl` + `S` |

**セルは上から順番に実行してください。** 途中を飛ばすとエラーになります。

**Run the cells from top to bottom.** Skipping cells causes errors.

---

## ステップ 11　最初の壁 / The first wall

うまくいかないときの **9 割は、次の 3 つ** です。

| 症状 / Symptom | 原因 / Cause | 対処 / Fix |
|---|---|---|
| `No module named 'numpy'` | カーネルが違う / wrong kernel | 右上で `Python 3 (AI Vision)` を選ぶ / choose it top-right |
| `python が見つからない` | PATH 未設定 / PATH not set | Python を入れ直す（PATH にチェック）/ reinstall with the PATH tick |
| `Activate.ps1 cannot be loaded` | 実行ポリシー / execution policy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |

それでも分からないときは、**次の 3 つをメモして** 講師に伝えてください。

1. どのノートブックの、どのセルか
2. エラーメッセージ（最後の 2 行）
3. すでに試したこと

If you are still stuck, note three things for the instructor: which notebook and cell,
the last two lines of the error message, and what you already tried.

---

## ステップ 12　終わるとき / When you finish for the day

1. `Ctrl` + `S` でノートブックを保存
2. ブラウザのタブを閉じる
3. PowerShell に戻り、`Ctrl` + `C` を **2 回** 押して JupyterLab を止める
4. PowerShell の窓を閉じる

Save with `Ctrl` + `S`, close the browser tab, press `Ctrl` + `C` twice in PowerShell to
stop JupyterLab, then close the PowerShell window.

PowerShell を閉じると、`(.venv)` も解除されます。翌日はステップ 3 からやり直してください。

Closing PowerShell also deactivates `(.venv)`. Next day, start again from Step 3.
