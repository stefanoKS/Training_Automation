# 第5日 学習レポート / Day 05 Learning Report
**氏名 / Name:** ____________________
**日付 / Date:** 2026 年 ____ 月 ____ 日

---

## 記入のルール / How to fill this in

空欄はすべて埋めてください。「なし」も立派な記録です。**他人の答えを写さないでください。**

Fill in every field. "None" is a perfectly good record. Do not copy anyone else's answers.

---

<!-- ne:begin doc:2786d02dea -->
### नेपालीमा

सबै खाली ठाउँ भर्नुहोस्। "छैन" पनि राम्रो अभिलेख हो।
**अरूको जवाफ नक्कल नगर्नुहोस्।** आफ्नै शब्दमा लेख्नु नै यो तालिमको उद्देश्य हो।
<!-- ne:end -->

## 1. 本日の学習内容 / Today's learning

異常検知が「正常だけ」で学ぶ仕組みと、YOLO との違いをまとめてください。

Summarise how anomaly detection learns from normal data only, and how it differs from YOLO.

```text
（ここに記入 / write here）



```

---

<!-- ne:begin doc:f232ffa42e -->
### नेपालीमा

आज सिकेको कुरा ३–५ पङ्क्तिमा जम्मा गर्नुहोस्।
<!-- ne:end -->

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

<!-- ne:begin doc:4713166a3d -->
### नेपालीमा

चलाएको नोटबुक र सकिएको Part मा चिन्ह लगाउनुहोस्। नोटबुकको नाम जस्ताको तस्तै राख्नुहोस्।

| नोटबुक | चलाएँ | सकिएको Part / सिकाइ सकियो | लागेको समय |
|---|---|---|---|
|  | [ ] | | ____ मिनेट |
|  | [ ] | | ____ मिनेट |
|  | [ ] | | ____ मिनेट |

गरेका अभ्यासमा चिन्ह लगाउनुहोस्।

- [ ] अभ्यास 1 (आधारभूत)
- [ ] अभ्यास 2 (मध्यम)
- [ ] अभ्यास 3 (विकास)
- [ ] निर्देशित प्रयोग
- [ ] बुझाइ जाँचका ५ प्रश्न
<!-- ne:end -->

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

<!-- ne:begin doc:34dc34065f -->
### नेपालीमा

सङ्ख्या र नतिजा **जस्ताको तस्तै** लेख्नुहोस्। मापन (metric) का नाम जस्ताको तस्तै राख्नुहोस्।
क्यालिब्रेसन र परीक्षण अलग-अलग लेख्नुहोस्; परीक्षण डेटामा threshold मिलाउनु हुँदैन।

| विषय | मान |
|---|---|
| backbone | |
| coreset_sampling_ratio | |
| num_neighbors | |
| सिकाइ समय | ____ सेकेन्ड |

| मापन | मान |
|---|---|
| image_AUROC | |
| image_F1Score | |
<!-- ne:end -->

## 4. YOLO と PatchCore の比較 / YOLO versus PatchCore

同じ画像で比べた結果を書いてください。

Record the comparison on the same images.

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

<!-- ne:begin doc:51b09c1d8d -->
### नेपालीमा

दुई तरिकाको नतिजा **एउटै परीक्षण सेटमा** राखेर तुलना गर्नुहोस्। क्यालिब्रेसनमा छानिएको
threshold र परीक्षणको नतिजा अलग-अलग लेख्नुहोस्। परीक्षणमा हेरेर threshold मिलाउनु हुँदैन।

| विषय | YOLO | PatchCore |
|---|---|---|
| देखाउने कुरा | | |
| यो सेटमा नतिजा | | |
| फाइदा | | |
| कमी | | |

score लाई probability नसम्झनुहोस्; image score र heatmap को अधिकतम मान फरक कुरा हुन्।
<!-- ne:end -->

## 5. 塩ビ検査への推奨 / Recommendation for PVC inspection

根拠となる数字を必ず引用してください。

Cite concrete numbers as evidence.

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

<!-- ne:begin doc:9aaf9441ee -->
### नेपालीमा

आफ्नो प्रक्रियाका लागि कुन तरिका सिफारिस गर्नुहुन्छ र किन, लेख्नुहोस्। उत्पादनमा प्राप्त हुने
शुद्धताको दाबी नगर्नुहोस्; यो तालिमको नतिजा नै त्यसको आधार होइन।

| विषय | विवरण |
|---|---|
| सिफारिस गर्ने तरिका | |
| कारण | |
| चाहिने डेटा | |
| जोखिम | |
<!-- ne:end -->

## 4. 発生した問題 / Problems encountered

どのノートブックの、どのセルで、どんなメッセージが出たかを書いてください。

Record which notebook, which cell, and the exact message.

| # | ノートブック / Notebook | セル / Cell | エラーメッセージ / Error message |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

**問題が無かった場合は「なし」/ write "none" if there were no problems**

---

<!-- ne:begin doc:19764a627e -->
### नेपालीमा

त्रुटि आए **कुन नोटबुकको, कुन सेलमा, के सन्देश आयो** लेख्नुहोस्। screenshot भए पनि हुन्छ।

| # | नोटबुक | सेल | त्रुटि सन्देश |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

समस्या नभए "छैन" लेख्नुहोस्।
<!-- ne:end -->

## 5. 試した解決方法 / Troubleshooting attempts

| # | 試したこと / What I tried | 結果 / Result |
|---|---|---|
| 1 | | |
| 2 | | |

---

<!-- ne:begin doc:17cb1658b6 -->
### नेपालीमा

माथिका समस्याका लागि **के प्रयास गरें र के भयो** लेख्नुहोस्। नमिलेका प्रयास पनि लेख्नुहोस्।

| # | प्रयास | नतिजा |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
<!-- ne:end -->

## 6. 理解できなかった内容 / Questions remaining

質問の形で書いてください。

Write them as questions.

1. 
2. 
3. 

---

<!-- ne:begin doc:1775cfdc3c -->
### नेपालीमा

नबुझेको कुरा **प्रश्नको रूपमा** लेख्नुहोस्।
"केही बुझिएन" भन्दा "〇〇 र 〇〇 को फरक बुझिएन" भन्दा राम्रो जवाफ पाइन्छ।

1.
2.
3.
<!-- ne:end -->

## 7. 化成品工程への応用 / Application to Kaseihin

今日学んだことが、あなたの工程のどこに使えそうか。うまくいかないと思う点も書いてください。

Where could today's topic be applied in your process? Include what you think would not work.

```text
（ここに記入 / write here）



```

---

<!-- ne:begin doc:23769afbb0 -->
### नेपालीमा

आज सिकेको कुरा **तपाईंको प्रक्रियाको कुन ठाउँमा प्रयोग गर्न सकिन्छ** लेख्नुहोस्।
राम्रो नहुने लागेको बुँदा पनि लेख्नुहोस्।
<!-- ne:end -->

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

<!-- ne:begin doc:963898c2dd -->
### नेपालीमा

तलको ४ तहले आफैं मूल्याङ्कन गर्नुहोस्। **लक्ष्य तह 2 वा माथि** हो।

| तह | अवस्था | चिन्ह |
|---|---|---|
| 0 | नसकिएको | [ ] |
| 1 | ठुलो सहयोगमा सकिएको | [ ] |
| 2 | अलिकति सहयोगमा सकिएको | [ ] |
| 3 | एक्लै सकेर नतिजा बुझाउन सक्ने | [ ] |

तह 3 को सर्त "**नतिजा अरूलाई बुझाउन सक्ने**" हो। "चल्यो" मात्र भए 3 होइन।

**यो तह छान्नुको कारण:**
<!-- ne:end -->

## 提出物チェック / Submission checklist

- [ ] 実行済みのノートブック（保存済み / saved）
- [ ] このレポート（記入済み / filled in）
- [ ] 保存した画像・CSV・JSON
- [ ] エラーの記録（無い場合は「なし」/ "none" if none）

<!-- ne:begin doc:3a26b58eff -->
### नेपालीमा

- [ ] चलाइएको नोटबुक (सुरक्षित)
- [ ] यो रिपोर्ट (भरिएको)
- [ ] सुरक्षित गरिएका चित्र, CSV, JSON (`submissions/day05/` भित्र)
- [ ] त्रुटिको अभिलेख (नभए "छैन" भनेर स्पष्ट लेखिएको)

**बुझाउने ठाउँ:** प्रशिक्षक (`submissions/day05/` फोल्डर सहित)
<!-- ne:end -->
