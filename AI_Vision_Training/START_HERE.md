# はじめかた / START HERE

**日本語：** このファイルは、**パソコンの電源を入れるところから**始める方向けの手順書です。
むずかしい言葉はできるだけ避けて書いています。上から順番に進めてください。

**English:** This is the **from-switching-the-PC-on** guide. It avoids jargon wherever possible.
Work through it from top to bottom.

---

## ステップ 0　この手順書のゴール / Goal of this guide

**日本語：** ゴールは 1 つだけです。

> `notebooks/00_Setup/00_Environment_Setup.ipynb` を開いて、最後までエラーなく実行できること。

**English:** There is exactly one goal: open
`notebooks/00_Setup/00_Environment_Setup.ipynb` and run it to the end without errors.

---

## ステップ 1　フォルダを確認する / Check the folder

**日本語：** `AI_Vision_Training` フォルダを、次の場所に置いてください。

```text
C:\Users\<あなたの名前>\Documents\AI_Vision_Training
```

**日本語：** デスクトップやダウンロードのままでも動きますが、**Documents** を推奨します。
あとで探しやすく、パスも短くなるからです。

**English:** Put the `AI_Vision_Training` folder under
`C:\Users\<your-name>\Documents\`. It also works from the Desktop or Downloads, but Documents is
recommended: it is easier to find and keeps the path short.

---

## ステップ 2　PowerShell を開く / Open PowerShell

**日本語：** 画面下の検索欄に `PowerShell` と入力し、出てきた **Windows PowerShell** をクリックします。

黒い（または青い）窓が開きます。これが **ターミナル** です。

**English:** Type `PowerShell` in the Windows search box and click **Windows PowerShell**.
A dark (or blue) window opens. That is the **terminal**.

> **日本語：** マウスでクリックする代わりに、**文字で** コンピュータに命令する窓です。
> **English:** It is the window where you type instructions instead of clicking.

---

## ステップ 3　フォルダに移動する / Move into the folder

**日本語：** 次の 1 行をコピーして、PowerShell に貼り付け、`Enter` を押します。

**English:** Copy the following single line, paste it into PowerShell and press `Enter`.

```powershell
cd "$HOME\Documents\AI_Vision_Training"
```

**日本語：** うまくいかない場合は、自分のユーザー名を直接書きます。

**English:** If that does not work, type your user name explicitly:

```powershell
cd "C:\Users\あなたの名前\Documents\AI_Vision_Training"
```

**日本語：** 正しく移動できたか確認します。

**English:** Check that you are in the right place:

```powershell
pwd
Get-ChildItem
```

**日本語：** `README.md` と `notebooks` が見えれば成功です。
**English:** If you can see `README.md` and `notebooks`, you are in the right folder.

---

## ステップ 4　Python があるか確認する / Check Python

```powershell
python --version
```

**日本語：** `Python 3.11.x` または `Python 3.12.x` と表示されれば OK です。

| 表示 / What you see | 意味 / Meaning | 対処 / What to do |
|---|---|---|
| `Python 3.11.9` | 正常 / fine | 次へ / continue |
| `Python was not found` | 入っていない / not installed | 下の「Python の入れ方」 / see below |
| Microsoft Store が開く / the Store opens | Windows の機能 / Windows alias | 設定 →「アプリ実行エイリアス」→ `python.exe` をオフ / Settings -> App execution aliases -> turn `python.exe` off |

### Python の入れ方（必要な場合のみ）/ Installing Python (only if needed)

**日本語：** [python.org](https://www.python.org/downloads/) を開き、**Python 3.11** を選びます。

**必ず** インストーラの最初の画面で

- ☑ **Add python.exe to PATH**

にチェックを入れ、「Install Now」を押します。**このチェックを忘れると動きません。**

**English:** Open [python.org](https://www.python.org/downloads/) and choose **Python 3.11**.
On the first installer screen you **must** tick "**Add python.exe to PATH**", then click "Install Now".
Forgetting that tick is the most common cause of failure.

**日本語：** 入れ終わったら PowerShell を **閉じて、もう一度開き**、`python --version` を確認してください。
**English:** Afterwards **close and reopen** PowerShell and check `python --version` again.

---

## ステップ 5　仮想環境を作る / Create the virtual environment

**日本語：** **仮想環境** は「この研修専用の道具箱」です。作っておくと、
他の仕事の Python を壊しません。

**English:** A **virtual environment** is a private toolbox for this course. It keeps you from
breaking the Python used by other work.

```powershell
python -m venv .venv
```

**日本語：** 何も表示されなければ成功です（1〜2 分かかります）。

**English:** Success is silent; it takes a minute or two.

**日本語：** 次に、この道具箱を **使う状態** にします。

**English:** Now switch the toolbox on:

```powershell
.\.venv\Scripts\Activate.ps1
```

**日本語：** プロンプトの先頭に `(.venv)` が付きます。

```text
(.venv) PS C:\Users\あなたの名前\Documents\AI_Vision_Training>
```

**English:** The prompt now starts with `(.venv)`.

**エラーが出た場合 / If it fails**

```text
Activate.ps1 cannot be loaded because running scripts is disabled
```

**日本語：** 次の 1 行を実行し、`Y` を押してから、もう一度 `Activate.ps1` を実行します。
**English:** Run the line below, answer `Y`, then activate again.

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

## ステップ 6　必要なものを入れる / Install the packages

**日本語：** `(.venv)` が付いた状態で、上から順に実行します。**数分かかります。**

**English:** With `(.venv)` visible, run these in order. It takes several minutes.

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements\base.txt
python -m pip install -r requirements\yolo.txt
python -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
```

**日本語：** 最後の `ipykernel install` は「この道具箱を、Jupyter から選べるように登録する」作業です。
**これを忘れると、Jupyter から研修用の環境が見えません。**

**English:** The last line registers this environment so Jupyter can offer it as a kernel.
**Skip it and Jupyter will not see the course environment.**

**日本語：** エラーで止まったら、**同じコマンドをもう一度実行** してください。
ネットワークの一時的な失敗がほとんどです。何度も失敗する場合は講師に連絡してください。

**English:** If a command fails, **run the same command again**; transient network errors are common.
Contact the instructor if it keeps failing.

---

## ステップ 7　（第5日の前に）2つ目の環境を作る / Create the second environment (before Day 5)

**日本語：** **第 5 日だけ** 別の道具箱を使います。第 4 日が終わってからで構いません。

**English:** **Day 5 only** uses a second toolbox. You can do this after Day 4.

```powershell
python -m venv .venv-anomalib
.\.venv-anomalib\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements\anomalib.txt
python -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

**日本語：** なぜ分けるのかは [`README.md`](README.md) の 3 節に書いています。
**English:** Section 3 of `README.md` explains why they are separate.

---

## ステップ 8　素材を作る / Generate the assets

**日本語：** 画像・図・データセットを生成します（`(.venv)` の状態で）。

**English:** Generate the images, diagrams and datasets (with `(.venv)` active).

```powershell
python assets\scripts\generate_training_assets.py
python assets\scripts\prepare_datasets.py
```

**日本語：** `Done.` と表示されれば成功です。
**English:** You should see `Done.`

---

## ステップ 9　JupyterLab を起動する / Start JupyterLab

```powershell
jupyter lab
```

**日本語：** ブラウザが自動で開きます。開かない場合は、PowerShell に表示された
`http://localhost:8888/...` の URL をブラウザに貼り付けてください。

**English:** Your browser opens automatically. If not, copy the `http://localhost:8888/...` URL from
PowerShell into the browser.

**日本語：** 画面の左にファイル一覧が出ます。`notebooks` → `00_Setup` →
`00_Environment_Setup.ipynb` の順にクリックして開いてください。

**English:** A file list appears on the left. Click `notebooks` -> `00_Setup` ->
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

**日本語：** **セルは上から順番に実行してください。** 途中を飛ばすとエラーになります。

**English:** **Run the cells from top to bottom.** Skipping cells causes errors.

---

## ステップ 11　最初の壁 / The first wall

**日本語：** うまくいかないときの **9 割は、次の 3 つ** です。

| 症状 / Symptom | 原因 / Cause | 対処 / Fix |
|---|---|---|
| `No module named 'numpy'` | カーネルが違う / wrong kernel | 右上で `Python 3 (AI Vision)` を選ぶ / choose it top-right |
| `python が見つからない` | PATH 未設定 / PATH not set | Python を入れ直す（PATH にチェック）/ reinstall with the PATH tick |
| `Activate.ps1 cannot be loaded` | 実行ポリシー / execution policy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |

**日本語：** それでも分からないときは、**次の 3 つをメモして** 講師に伝えてください。

1. どのノートブックの、どのセルか
2. エラーメッセージ（最後の 2 行）
3. すでに試したこと

**English:** If you are still stuck, note three things for the instructor: which notebook and cell,
the last two lines of the error message, and what you already tried.

---

## ステップ 12　終わるとき / When you finish for the day

**日本語：**

1. `Ctrl` + `S` でノートブックを保存
2. ブラウザのタブを閉じる
3. PowerShell に戻り、`Ctrl` + `C` を **2 回** 押して JupyterLab を止める
4. PowerShell の窓を閉じる

**English:** Save with `Ctrl` + `S`, close the browser tab, press `Ctrl` + `C` twice in PowerShell to
stop JupyterLab, then close the PowerShell window.

**日本語：** PowerShell を閉じると、`(.venv)` も解除されます。翌日はステップ 3 からやり直してください。

**English:** Closing PowerShell also deactivates `(.venv)`. Next day, start again from Step 3.
