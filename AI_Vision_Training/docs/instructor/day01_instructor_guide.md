# 第1日 講師ガイド / Day 1 Instructor Guide

**AI の基礎と画像認識 / AI fundamentals and image recognition**

---

## 午前（08:00–09:00）／ Morning session

### 学習目標 / Learning goals

受講者が今日 1 日で到達する状態を示します。
State where learners should be by the end of the day.

1. AI・機械学習・深層学習が **入れ子** であることを言える
2. 「学習」と「推論」の違いを、時間とデータの量で説明できる
3. 画像が **数値の表** であることを言える
4. 分類・検出・セグメンテーション・異常検知の **出力の違い** を言える
5. PVC 検査に、どの手法が向いていそうかを **自分の言葉で** 提案できる

### 説明する概念 / Key concepts

| 概念 / Concept | 説明の要点 / Key message |
|---|---|
| プログラム | 人間が書いた手順書。速い・疲れない・正確。**ルールが書ける仕事** に強い |
| 自動化 | 決まった手順の繰り返し。判断のルールは人間が決める |
| 機械学習 | データから規則性を **コンピュータ自身に** 見つけさせる |
| 深層学習 | 多層ニューラルネットワークを使う機械学習。ML の中の一部 |
| 学習 / 推論 | 学習は遅くデータが必要、推論は速く 1 枚で足りる。**ラインで動くのは推論** |

### 実演 / Demonstration（10 分程度）

ノートブック 01 の Part 1〜Part 4 を、プロジェクタで実演してください。

1. `judge_width()` に 100.3 / 100.6 を入れて OK / NG を出す
2. 1000 個を一括判定し、NG 率を出す（**自動化の速さ** を見せる）
3. 正常品 200 枚から正常範囲を学習する（**学習の最小形** を見せる）
4. 暗い日のデータで学習すると、正常品が NG になる（**データの偏り** を見せる）

Run Parts 1-4 of Notebook 01 on the projector: a hand-written rule, a batch run to show
speed, learning a normal range from 200 good products, then the same model trained on a dark day
mislabelling a good product.

### よくある誤解 / Common beginner misunderstandings

| 誤解 / Misunderstanding | 実際 / Reality |
|---|---|
| 「AI は何でも判断できる」 | 学習したことしかできない。**学習していない欠陥は見逃す** |
| 「AI は人間より正確」 | データが偏れば人間より悪い。しかも自信満々に間違える |
| 「AI と機械学習は別物」 | 深層学習 ⊂ 機械学習 ⊂ AI の入れ子 |
| 「学習＝AI が賢くなる」 | 数値（パラメータ）が決まるだけ。**賢さはデータで決まる** |
| 「画像は特別なもの」 | ただの数値の表。第1日 02 で実際に書き換える |

### 受講者に投げかける質問 / Questions to ask

1. 「あなたの工程で、**ルールで書ける検査** と、**書けない検査** は何ですか？」
2. 「見逃し（偽陰性）と誤報（偽陽性）、どちらが困りますか？ なぜですか？」
3. 「もし AI が 95 % の精度だったら、このラインに入れますか？」

### 午前の課題説明 / Explaining the morning assignment

ノートブック 01 の **演習 1〜2（必須）** を午前中に終えるよう伝えてください。
**演習 3（発展）は任意** です。完了チェックリストには入っていません。

Aim to finish **Exercises 1-2 (required)** of Notebook 01 before lunch.
**Exercise 3 (challenge) is optional** and is not part of the completion checklist.

> **変更点 / Change:** 以前の演習 1 は「判定関数を自分で書く」でしたが、
> **関数は第 2 日に教える** ため、第2日ノートブック02 の演習 1 に移しました。
> 第 1 日の演習 1 は、**用意された関数を実行して結果を予想する** 課題になっています。
> 第 1 日で関数の文法を説明する必要はありません。
>
> The old Exercise 1 asked learners to write a judgement function, but **functions are taught on
> Day 2**, so it moved to Exercise 1 of Day 2 Notebook 02. Day 1 Exercise 1 now asks learners to
> **run a supplied function and predict its result**. You do not need to explain function syntax on
> Day 1.

今日の核心は **演習 3（発展）** の「ルールで書ける部分と AI が必要な部分の切り分け」ですが、
時間が無ければ講師のまとめで扱ってください。
The heart of the day is Exercise 3's split between rule-writable and AI tasks; if time is short,
cover it in the instructor wrap-up instead.

---

## 午後（12:50–13:50）／ Afternoon session

### 午前の振り返り / What to review

次の 3 点だけ、受講者に **言わせて** 確認してください（講師が説明しない）。

1. AI・機械学習・深層学習の関係
2. 学習と推論の違い
3. 偽陽性と偽陰性の違い

Have learners **say** these three things rather than hearing them again.

### 期待される結果 / Expected results

| ノートブック / Notebook | 午前終了時の到達 / By lunchtime |
|---|---|
| 01 Introduction to AI | Part 1〜Part 5 完了、演習 1・2 完了 |
| 02 Pixels and Images | Part 1〜Part 4 完了（画素・解像度・RGB・座標） |
| 03 Computer Vision Tasks | Part 1〜Part 4 完了（4 つのタスクの違い） |

遅れている受講者には、**02 と 03 の順序を入れ替えてもよい** と伝えてください。
02 の方が具体的で取り組みやすいためです。

For anyone falling behind, allow swapping the order of 02 and 03; 02 is more concrete.

### よくあるエラー / Common errors

| 症状 / Symptom | 原因 / Cause | 説明の仕方 / How to explain |
|---|---|---|
| `FileNotFoundError`（画像） | 素材未生成 | `generate_training_assets.py` を 1 回実行 |
| 図のタイトルが `□□□` | フォント未設定 | ノートブックのフォント設定セルを先に実行 |
| `IndexError` | 座標が画像外 | `shape` は `(高さ, 幅)` の順だと説明 |
| 「予想と違う」 | **正常** | 予想が外れたことを歓迎する。なぜ外れたかを書かせる |

### 次に導入する概念 / Next concepts to introduce

第 2 日の冒頭で「**今日から自分でプログラムを書きます**」と伝えてください。
第 1 日で見た「数字の表を書き換える」が、第 2 日では「条件で判定する」に進みます。

Announce that Day 2 starts writing programs. Modifying a table of numbers becomes
judging with conditions.

### 午後の課題説明 / Afternoon assignment briefing

1. ノートブック 02 の Part 5〜Part 7（画像の作成・書き換え・予想演習）
2. ノートブック 03 の全 Part
3. 各ノートブックの演習 3 つと理解度チェック 5 問
4. 提出物：実行済みノートブック、`Day01_Report_Template.md`、保存した画像

---

## 評価ルーブリック / Assessment rubric

| 観点 / Criterion | Level 0 | Level 1 | Level 2 | Level 3 |
|---|---|---|---|---|
| AI・ML・DL の説明 | 未着手 | 用語だけ並べる | 入れ子関係を説明できる | 製造の例で説明できる |
| 学習と推論 | 未着手 | 片方だけ説明 | 両方説明できる | 時間・データ量の観点で説明できる |
| 画素と解像度 | 未着手 | 画素の説明のみ | 解像度との関係を説明 | 欠陥サイズとの関係まで説明 |
| 画像の加工 | 未完了 | 助けを借りて完了 | 一人で完了 | 結果の意味を説明できる |
| 4 タスクの違い | 未着手 | 名前だけ | 出力の違いを説明 | 用途に応じて選べる |
| PVC への提案 | なし | 手法名のみ | 理由付きで提案 | データ計画と限界まで言及 |

---

## 理解度チェックの解答例 / Model answers

**（受講者には渡さないでください / do not hand these to learners）**

### ノートブック 01

1. **プログラムは人間がルールを書き、AI はデータからルールを見つける。**
   例：幅の判定はルールで書ける（100±0.5）。黒点の検出は「黒い」を数値で書ききれず、AI が必要。
2. **機械学習のほうが広い。** 深層学習は多層ニューラルネットワークを使う機械学習の一種。
3. **学習**：時間がかかり、大量のデータが必要。**推論**：速く、画像 1 枚で足りる。
4. 例：① 暗い日だけの写真で学習した（偏り）② 正常品 5 枚しか無い（不足）
   ③ ラベルの間違い ④ 本番と照明・距離が違う。
5. **偽陰性（見逃し）のほうが深刻。** 不良品を出荷してしまうため。
   ただし偽陽性が多すぎるとラインが止まり、現場が検査を信用しなくなる。

### ノートブック 02

1. 640 × 480 × 3 = **921,600 個**。
2. **左上**。数学のグラフは左下が原点で上向きが正だが、画像は左上が原点で **下向きが正**。
3. RGB がすべて同じ値なので **灰色**（120 は中間の灰色）。
4. **小さな欠陥は平均化されて消える**。縮小すると隣接画素がまとめられるため。
5. 画素の書き換えは、**画像の改変・欠陥のシミュレーション・マスク作成** に相当する。

### ノートブック 03

1. 分類は **画像 1 枚に 1 ラベル**、検出は **複数の四角＋種類＋confidence**。
2. セマンティックは欠陥全体を 1 つのマスクに。インスタンスは **欠陥ごとに別のマスク**。
3. 正常品の見え方だけを学ぶため。その代わり **何の欠陥かは分からない**。
4. **セグメンテーション**（画素単位で面積が分かる）。物体検出では四角の面積しか分からない。
5. **セグメンテーション** が最も大変。画素単位で塗る作業が必要で、時間もかかり、判断もぶれる。