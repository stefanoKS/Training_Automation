# 第2日 講師ガイド / Day 2 Instructor Guide

**Python プログラミングと OpenCV / Python programming and OpenCV**

---

## 午前（08:00–09:00）／ Morning session

### 学習目標 / Learning goals

1. `print()` と変数で値扱いができる
2. `=` と `==` の違いを言える
3. `if` / `elif` / `else` を書ける
4. 関数の引数と戻り値を説明できる
5. OpenCV で画像を読み、グレー・2値化できる
6. ピクセルを mm に変換し、**その限界** を説明できる

### 説明する概念 / Key concepts

| 概念 / Concept | 説明の要点 / Key message |
|---|---|
| 変数 | 名前の付いた箱。`=` は「入れる」、`==` は「等しいか」 |
| 型 | `int`（整数）/ `float`（小数）/ `str`（文字列）/ `bool`（真偽） |
| 小数の誤差 | `0.1 + 0.2 != 0.3`。**比較は不等号か `round`** |
| 条件分岐 | `:` とインデントが必須。**最初に当てはまった枝だけ** 実行 |
| 関数 | 引数 → 処理 → 戻り値。**1 か所直せば全部直る** |
| 例外 | `try` / `except`。**エラーを隠さず記録する** |
| 2値化 | しきい値は **人間が決める**。上げると誤報、下げると見逃し |
| 校正 | px/mm は **撮影条件で決まる**。動かしたら校正し直す |

### 実演 / Demonstration（10 分程度）

**日本語：** **必ず「エラーを見せる」実演を入れてください。**

1. `print(sheet_width)` を未定義で実行 → `NameError` を見せる
2. `"abc" + 100` → `TypeError` を見せる
3. `if` の `:` を消す → `SyntaxError` を見せる
4. そのあと正しく直して動かす

**English:** Always demonstrate errors: an undefined name, adding text to a number, a missing colon —
then fix each one. Learners need to see that errors are information, not failure.

### よくある誤解 / Common beginner misunderstandings

| 誤解 / Misunderstanding | 実際 / Reality |
|---|---|
| `=` は「等しい」 | 代入。比較は `==` |
| インデントは見た目だけ | **文法**。ずれるとエラー |
| `0.3` は正確に表せる | 2 進数では表せない。誤差が出る |
| `except: pass` で安全 | **危険**。エラーが消えて原因不明になる |
| `cv2.imread` は失敗すると例外 | `None` を返す。**必ず確認** |
| OpenCV と Matplotlib の色順は同じ | OpenCV は **BGR**、Matplotlib は RGB |

### 受講者に投げかける質問 / Questions to ask

1. 「`=` と `==`、どう違いますか？」
2. 「`input()` を使わないのはなぜだと思いますか？」（→ 自動実行できない、記録が残らない）
3. 「しきい値を 150 から 200 に上げると、現場では何が起きますか？」

### 午前の課題説明 / Explaining the morning assignment

**日本語：** ノートブック 01 の全 Part と、02 の Part 1〜Part 3 まで。

**English:** All of Notebook 01 and Parts 1-3 of Notebook 02.

---

## 午後（12:50–13:50）／ Afternoon session

### 午前の振り返り / What to review

1. `=` と `==`（言わせる）
2. 小数の誤差（**なぜ** 起きるか）
3. `if` の 2 つの必須事項（`:` とインデント）

**日本語：** エラー記録を見せ合う時間を 5 分取ってください。「同じエラーを 3 人が出した」
という発見が、受講者の不安を大きく下げます。

**English:** Spend five minutes comparing error logs. Discovering that three people hit the same
error greatly reduces anxiety.

### 期待される結果 / Expected results

| ノートブック / Notebook | 午後終了時の到達 / By end of day |
|---|---|
| 01 Python Basics | 全 Part、演習 1〜3 |
| 02 Conditions/Loops/Functions | Part 1〜Part 5、`analyse_measurements` が動く |
| 03 OpenCV | 輪郭検出、px→mm 換算、面積の mm² 換算 |

### よくあるエラー / Common errors

| 症状 / Symptom | 原因 / Cause | 説明の仕方 / How to explain |
|---|---|---|
| `IndentationError` | `if` の次の行のインデント | 「中身は 4 文字下げる」と口頭で統一 |
| `NameError: judge_width` | 関数定義のセルを実行していない | 「上から順に実行」を再確認 |
| `cv2.findContours` が 3 つ返る | OpenCV 3 系の記事 | 4 系は 2 つ。教材のコードを使う |
| 色が反転 | BGR/RGB の変換忘れ | `COLOR_BGR2RGB` を見せる |
| 面積の換算が合わない | 長さは 1 乗、面積は 2 乗 | `px_per_mm ** 2` を強調 |

### 次に導入する概念 / Next concepts to introduce

**日本語：** 第 3 日は「**自分では書けないルールを、学習済みモデルに任せる**」話に入ります。
第 2 日で「しきい値は人間が決める」と学んだことが、第 3 日では
「confidence のしきい値」として再登場します。

**English:** Day 3 delegates the rules you cannot write to a pretrained model. The human-chosen
threshold from Day 2 returns as the confidence threshold.

### 午後の課題説明 / Afternoon assignment briefing

1. ノートブック 02 の Part 6（判定プログラムの完成）と演習
2. ノートブック 03 の全 Part と演習
3. 提出物：OK/NG 判定プログラム（5 つ以上の測定値）、OpenCV の処理結果、
   px→mm の換算結果と誤差の考察

---

## 評価ルーブリック / Assessment rubric

| 観点 / Criterion | Level 0 | Level 1 | Level 2 | Level 3 |
|---|---|---|---|---|
| Python の基本 | 未着手 | 写経のみ | 自分で書ける | エラーを自分で直せる |
| 条件分岐・ループ | 未着手 | 動かすだけ | 変更できる | 新規に書ける |
| 関数 | 未着手 | 呼べるだけ | 引数・戻り値を説明 | 自分で設計できる |
| 例外処理 | 未着手 | 用語のみ | `try/except` が書ける | 記録の設計まで考えられる |
| OpenCV の基本処理 | 未着手 | 実行のみ | 意味を説明 | しきい値を根拠をもって選べる |
| 校正と測定 | 未着手 | 数値の写しのみ | 換算できる | 誤差の原因を説明できる |

---

## 理解度チェックの解答例 / Model answers

**（受講者には渡さないでください / do not hand these to learners）**

### ノートブック 01

1. `=` は **代入**（箱に入れる）、`==` は **比較**（等しいかの判定）。
2. コンピュータは小数を **2 進数** で表すため、0.3 は正確に表せない。
3. `print(a, b)` は **スペース区切りで並べて表示**。`print(a + b)` は **足し算** をしようとして
   `TypeError`（文字列と数値は足せない）。
4. **変数名の綴り** と、**その変数を定義したセルを実行したか**。
5. 読みやすく、単位（`_mm`）まで分かる。後で自分や他人が読んでも意味が分かる。

### ノートブック 02

1. `:` が無いと `SyntaxError`。
2. **最初に当てはまった枝だけ** 実行され、残りは飛ばされる。
3. ① 同じコードを繰り返さない ② 名前で意味が分かる ③ 修正が 1 か所で済む。
4. `continue` は **その回の残りを飛ばして次の要素へ** 進む。
5. エラーが **見えなくなる**。データが壊れていても気づかず、原因の特定が不可能になる。

### ノートブック 03

1. OpenCV は **BGR**、Matplotlib は **RGB**。変換しないと赤と青が入れ替わる。
2. **エラーにならない。`None` を返す。** 必ず `None` チェックをする。
3. `BINARY_INV` は **白黒を反転**。欠陥を白にしたいのでこちらを使う（輪郭検出が素直になる）。
4. **誤検出（偽陽性）が増える。** 明るさのムラまで欠陥と判定してしまう。
5. 1 ピクセルが何 mm かは **カメラと物体の距離** で変わる。校正していない画像の px は、
   mm に換算する根拠が無い。