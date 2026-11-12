# 第5日 学習レポート / Day 05 Learning Report
**氏名 / Name:** ____________________
**日付 / Date:** 2026 年 ____ 月 ____ 日

---

## 記入のルール / How to fill this in

**日本語：** 空欄はすべて埋めてください。「なし」も立派な記録です。**他人の答えを写さないでください。**

**English:** Fill in every field. "None" is a perfectly good record. Do not copy anyone else's answers.

---
## 1. 本日の学習内容 / Today's learning

**日本語：** 異常検知が「正常だけ」で学ぶ仕組みと、YOLO との違いをまとめてください。

**English:** Summarise how anomaly detection learns from normal data only, and how it differs from YOLO.

```text
（ここに記入 / write here）



```

---

## 2. 実施した作業 / Completed activities

| ノートブック / Notebook | 実行した / Ran | 完了した Part / Parts done |
|---|---|---|
| Day05_01_Anomaly_Detection_Concepts | [ ] | |
| Day05_02_PatchCore_Training | [ ] | |
| Day05_03_YOLO_vs_PatchCore | [ ] | |

- [ ] 演習 1（基本）/ basic
- [ ] 演習 2（中級）/ intermediate
- [ ] 演習 3（発展）/ challenge
- [ ] しきい値を変えた実験 / threshold experiment
- [ ] 理解度チェック 5 問 / five questions

---

## 3. 実行結果 / Results

**PatchCore の設定 / PatchCore configuration**

| 項目 / Item | 値 / Value |
|---|---|
| backbone | |
| coreset_sampling_ratio | |
| num_neighbors | |
| 学習時間 / fit time | ____ 秒 |

**指標 / metrics**

| 指標 / Metric | 値 / Value |
|---|---|
| image_AUROC | |
| image_F1Score | |
| pixel_AUROC | |
| pixel_F1Score | |

**スコアの分離 / score separation**

| 項目 / Item | 値 / Value |
|---|---|
| 正常品スコアの最大 / max normal score | |
| 異常品スコアの最小 / min abnormal score | |
| 設定したしきい値 / threshold used | |

**ヒートマップ / heatmaps**

| ファイル / File | 異常か / abnormal | 気づいたこと / observation |
|---|---|---|
| | | |
| | | |

---

## 4. YOLO と PatchCore の比較 / YOLO versus PatchCore

**日本語：** 同じ画像で比べた結果を書いてください。

**English:** Record the comparison on the same images.

| 項目 / Item | YOLO | PatchCore |
|---|---|---|
| 学習に必要な画像 / training images | | |
| 学習に必要なラベル / labels | | |
| 出力 / output | | |
| 欠陥の種類が分かるか / defect type | | |
| 位置が分かるか / location | | |
| 見逃し（FN）の数 / misses | | |
| 誤報（FP）の数 / false alarms | | |
| precision | | |
| recall | | |
| 処理速度の印象 / speed impression | | |

**この比較の限界（自分で気づいた点）/ limits of this comparison**

1. 
2. 

---

## 5. PVC 検査への推奨 / Recommendation for PVC inspection

**日本語：** 根拠となる数字を必ず引用してください。

**English:** Cite concrete numbers as evidence.

| 項目 / Item | あなたの推奨 / Your recommendation |
|---|---|
| 第 1 段階で使う手法 / stage 1 method | |
| その理由（数字を引用）/ reason with numbers | |
| 第 2 段階で追加する手法 / stage 2 method | |
| 見逃しを減らすためにすること / reduce misses | |
| 誤報を減らすためにすること / reduce false alarms | |
| 第 2 週で確認すべきこと / check in Week 2 | |
| この研修の数字を製品精度として使えるか / usable as product accuracy? | はい / いいえ（理由: ） |
---

## 4. 発生した問題 / Problems encountered

**日本語：** どのノートブックの、どのセルで、どんなメッセージが出たかを書いてください。

**English:** Record which notebook, which cell, and the exact message.

| # | ノートブック / Notebook | セル / Cell | エラーメッセージ / Error message |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

**問題が無かった場合は「なし」/ write "none" if there were no problems**

---

## 5. 試した解決方法 / Troubleshooting attempts

| # | 試したこと / What I tried | 結果 / Result |
|---|---|---|
| 1 | | |
| 2 | | |

---

## 6. 理解できなかった内容 / Questions remaining

**日本語：** 質問の形で書いてください。

**English:** Write them as questions.

1. 
2. 
3. 

---

## 7. 化成品工程への応用 / Application to Kaseihin

**日本語：** 今日学んだことが、あなたの工程のどこに使えそうか。うまくいかないと思う点も書いてください。

**English:** Where could today's topic be applied in your process? Include what you think would not work.

```text
（ここに記入 / write here）



```

---

## 8. 自己評価 / Self-assessment

**目標はレベル 2 以上 / target is level 2 or above**

| レベル / Level | 状態 / State | チェック / Tick |
|---|---|---|
| 0 | 未完了 / not completed | [ ] |
| 1 | 大きな助けがあって完了 / significant assistance | [ ] |
| 2 | 少しの助けで完了 / minor assistance | [ ] |
| 3 | 一人で完了し、結果を説明できる / independently and can explain | [ ] |

**レベル 3 の条件は「結果を人に説明できる」ことです / level 3 means "can explain the result"**

**自分の評価の理由 / Why I chose this level:**

```text
（ここに記入 / write here）

```

---

## 提出物チェック / Submission checklist

- [ ] 実行済みのノートブック（保存済み / saved）
- [ ] このレポート（記入済み / filled in）
- [ ] 保存した画像・CSV・JSON
- [ ] エラーの記録（無い場合は「なし」/ "none" if none）