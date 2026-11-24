# 第9日 公式・確認カード / Day 9 formula and check card

> このカードは学習用です。実機の撮像系・照明・ネットワークの設計を承認するものではありません。
> This card is for learning. It does not approve a real imaging, lighting or network design.

## 1. 解像度と視野 / resolution and field of view

```text
1ピクセルの実寸[mm/px] = 視野の幅[mm] ÷ 画像の横画素数[px]
欠陥のピクセル数 = 欠陥寸法[mm] ÷ 1ピクセルの実寸[mm/px]
```

例 / example: 240 mm ÷ 1,920 px = **0.125 mm/px**。0.5 mm の欠陥 → **約4 px**。

- 4 px でも検出保証ではない。 / Four pixels is not a guarantee.
- 光学・ピント・コントラスト・照明・ぶれ・前処理・検証データで決まる。

## 2. 動体ぶれ / motion blur

```text
露光中の移動量[mm] = 材料速度[mm/s] × 露光時間[s]
ぶれ[px] = 移動量[mm] ÷ 1ピクセルの実寸[mm/px]
目標ぶれに必要な露光時間[s] = 目標ぶれ[px] × 1ピクセルの実寸 ÷ 材料速度
```

例 / example: 1,000 mm/s × 0.001 s = **1 mm** → **8 px**。1 px 目標なら **0.125 ms**。

- 短くすると光が減る。 / A shorter exposure collects less light.
- 例示的な目標であり保証ではない。 / An illustrative target, not a guarantee.

## 3. ラインセンサ / line scan

```text
必要なライン速度[line/s] = 材料速度[mm/s] ÷ 移動方向のサンプリング[mm/line]
```

例 / example: 1,000 ÷ 0.125 = **8,000 ライン/秒**。実際の能力は検証が必要。

## 4. フレーム間の移動 / movement between frames

```text
移動量[mm] = 材料速度[mm/s] ÷ フレームレート[FPS]
```

例 / example: 1,000 ÷ 30 ≈ **33.33 mm**。

- カメラFPS ≠ 検査FPS。転送・推論・判定・応答を含める。
- 移動方向の視野と幅方向の視野を混同しない。

## 5. シャッター / shutter

| 方式 / Type | 露光 / Exposure | 動く対象 / Moving object |
|---|---|---|
| グローバル / global | 全画素が同時 / all pixels together | 行ごとの時間ずれによるゆがみなし / no row-timing skew |
| ローリング / rolling | 行ごとに時間をずらす / rows in sequence | 斜めにゆがむことがある / can skew |

- グローバルでもぶれは残る。ぶれは露光時間で決まる。 / Blur remains; it depends on exposure.

## 6. 照明の使い分け / lighting choice

| 照明 / Lighting | 向く例 / Suitable examples |
|---|---|
| バックライト / backlight | シルエット、輪郭、穴、透過欠陥 / silhouette, edges, holes, transmission |
| リング / ring | 一般的な表面、近距離 / general surfaces at short range |
| バー / bar | 広い範囲、方向を決めた照射 / wide areas, directional |
| 拡散 / diffuse | 光沢、曲面、むら / gloss, curved surfaces, unevenness |
| 同軸 / coaxial | 平らな反射面の傷・印字 / flat reflective surfaces |
| 低角度・暗視野 / low angle | 傷、異物、微細な凹凸 / scratches, particles, relief |

- 効果は材質と欠陥形状に依存する。1種類で全欠陥は見えない。
- 透明・半透明・光沢・つや消しで返り方が変わる。

## 7. 撮像条件の記録 / record the imaging conditions

カメラ機種、レンズ、作動距離、視野、カメラ角度、照明の種類と位置、露光時間、ゲイン、フレームレート／ライン速度、材料速度、画像解像度、代表的な欠陥サンプル、環境条件。

Camera model, lens, working distance, field of view, camera angle, light type and position, exposure, gain, frame or line rate, material speed, image resolution, representative defect samples, environmental conditions.

## 8. 検査判定 / inspection decision

| 状態 / State | 扱い / Handling |
|---|---|
| OK | 良品 / good |
| NG | 不良 / reject |
| INVALID | 画像なし・推論失敗・通信失敗。**OKにしない** / no image, inference failure, link failure: **never OK** |

## 9. 構成の要点 / architecture points

- 画像データ・制御信号・電力・機械動作・フィードバックを区別する。
- AIは結果を制御装置へ渡す。危険な動作は機械側の制御と安全で扱う。
- AIソフトが電磁弁を直接動かす構成にしない。
- 記録・画像保存は任意。
