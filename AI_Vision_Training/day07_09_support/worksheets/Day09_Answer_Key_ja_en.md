# 第9日 解答例 / Day 9 Answer Key

> T1の選択項目は、条件によって複数の妥当な答えがあります。数値は独立に再計算しています。
> The selection items in T1 have several valid answers depending on conditions. The numbers were re-computed independently.

## T1 計算 / calculations

| # | 式 / Formula | 計算 / Working | 答え / Answer |
|---|---|---|---|
| 1 | 視野 ÷ 画素数 / FOV ÷ pixels | 240 ÷ 1920 | **0.125 mm/px** |
| 2 | 欠陥 ÷ 1px実寸 / defect ÷ sampling | 0.5 ÷ 0.125 | **4 px** |
| 3 | 速度 × 露光、÷ 1px実寸 | 1,000 × 0.001 = 1 mm；1 ÷ 0.125 | **1 mm、8 px** |

**採点上の注意 / marking note:** 4 px は検出保証ではない。照明・ピント・コントラスト・ぶれ・前処理・検証データで決まる。 / Four pixels is not a guarantee; lighting, focus, contrast, blur, preprocessing and validation data decide.

**別解の例 / alternative valid answer:** 露光0.125 ms を選べば 1 px。ただし光量が1/8になるため、照明の強化が必要。 / An exposure of 0.125 ms gives one pixel of blur but only one eighth of the light, so lighting must be re-checked.

## T1 選定チェックリストの例 / example selection answers

- 候補カメラ：2,000 px 級のエリアセンサ（速度要件が厳しければラインセンサ）。 / candidate camera: an area-scan camera around 2000 px, or line-scan if speed demands it.
- 候補レンズ：視野240 mm、作動距離300 mm 級。センササイズ対応とマウントを確認。 / candidate lens: 240 mm FOV at about 300 mm working distance, with sensor-size compatibility and mount checked.
- 候補照明：内部異物ならバックライト、表面傷なら低角度＋拡散。 / backlight for internal contamination; low-angle plus diffuse for surface scratches.
- 結果の伝達：PC → PLC（通信）、PLCが機械を制御。AIが電磁弁を直接動かさない。 / PC to PLC, and the PLC controls the machine; AI does not drive valves directly.

## T2 症状の原因候補 / possible causes

| 症状 / Symptom | 原因候補 / possible causes | 確認方法 / how to check |
|---|---|---|
| 午後に誤検出が増える / false detections later in the day | 太陽光・環境光の変化、温度上昇による特性変化、レンズ・保護窓の汚れ / changing daylight, thermal drift, contamination | 同じサンプルを時間帯別に撮影し、明るさとコントラストを比較 / capture the same sample at different times and compare brightness and contrast |
| 一部の欠陥だけ見えない / some defects never detected | 照明方向が合っていない、コントラスト不足、解像度不足、ピント / lighting direction, low contrast, insufficient sampling, focus | 照明方向を変えた比較、実対象での撮像試験 / change the light direction and test on real samples |
| ときどき暗くなる / sometimes dark | 露光・ゲイン設定のばらつき、照明の劣化、電源・ケーブルの接触 / exposure or gain drift, lighting ageing, connector problems | 撮像条件の記録と、照明の出力・配線の点検 / compare the recorded conditions and check lighting output and wiring |
| 位置がずれて写る / position shifts | 振動、取付の緩み、材料の張力・高さ変動、トリガのずれ / vibration, loose mounts, tension or height change, trigger drift | 固定具の点検、材料の支持、トリガ記録の確認 / inspect mounts, support the material, check trigger records |

## 数値の再現方法 / how to reproduce

```text
sampling = 240/1920          = 0.125 mm/px
pixels   = 0.5/0.125         = 4 px
blur_mm  = 1000*0.001        = 1 mm
blur_px  = 1/0.125           = 8 px
```
