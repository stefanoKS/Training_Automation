# 第9日 公式・確認カード / Day 9 formula and check card

**すべて仮定の例です。/ All examples are hypothetical.**

## 1. 画素スケール / Pixel scale

**mm/px = FOV ÷ horizontal pixels**

| FOV | pixels | mm/px |
|---:|---:|---:|
| 600 mm | 4,096 | ≈ 0.146484 |
| 400 mm | 2,048 | ≈ 0.195313 |
| 300 mm | 2,448 | ≈ 0.122549 |

**1画素未満の欠陥が必ず検出できる意味ではありません。 / Not a guarantee that sub-pixel defects are detectable.**

## 2. ライン周波数 / Line rate

**mm/s = m/min × 1,000 ÷ 60**
**lines/s = mm/s ÷ (mm/line)**

| speed | mm/s | mm/line | lines/s |
|---:|---:|---:|---:|
| 30 m/min | 500 | 0.2 | 2,500 |
| 60 m/min | 1,000 | 0.1 | 10,000 |
| 15 m/min | 250 | 0.25 | 1,000 |

## 3. 露光中の移動 / Travel during exposure

**travel = velocity × exposure time**

| speed | exposure | travel |
|---:|---:|---:|
| 0.5 m/s | 1.0 ms | 0.5 mm |
| 1.0 m/s | 0.2 ms | 0.2 mm |
| 0.5 m/s | 0.1 ms | 0.05 mm |

## 4. 画像データ量 / Image data volume

**bytes/s = pixels/line × lines/s × bytes/pixel**

4,096 × 2,500 × 1 = **10,240,000 B/s ≈ 10.24 MB/s**（10進 / decimal）。
**10.24 MB/s ≈ 81.92 Mb/s**（1 byte = 8 bits）。**MB/s と Mb/s を混同しない / never confuse them.**

## 5. 遅延と移動 / Latency and travel

**travel = velocity × latency**

| speed | latency | travel |
|---:|---:|---:|
| 0.5 m/s | 0.12 s | 60 mm |
| 0.4 m/s | 0.15 s | 60 mm |
| 1.0 m/s | 0.05 s | 50 mm |

移動量は**位置ずれ誤差と同じではない**。位置追跡・処理遅延・判断可能時刻・動作時刻を分ける。
Travel is **not the same as positioning error**; separate tracking, processing delay, decision time and action time.

## 6. 判定の6状態 / Six decision states

| 状態 / state | 自動OK / auto OK |
|---|---|
| 有効OK / valid OK | 可（方針による） / yes, per policy |
| 有効NG / valid NG | 不可 / no |
| 無効 / invalid | 不可 / no |
| タイムアウト / timeout | 不可 / no |
| 画像なし / no image | 不可 / no |
| 通信失敗 / comms failure | 不可 / no |

## 7. 受入確認 / Acceptance check

- ☐ 既知の良品・不良品で正しく判定 / known good and bad samples judged correctly
- ☐ 無効・タイムアウトがOKにならない / invalid and timeout never become OK
- ☐ 古いID・重複IDを拒否する / stale and duplicate IDs rejected
- ☐ 再起動後に古い結果を使わない / no stale result after restart
- ☐ 故障注入で検出できる / fault injection detected
- ☐ 平均値ではなく最大値とジッタを測る / measure worst case and jitter, not averages
- ☐ 安全系がAIと独立 / safety independent of AI

## 8. よくある誤解 / Common misunderstandings

1. 画素数を増やせば必ず良くなる → 光学・照明・コントラスト次第 / more pixels always better → depends on optics, lighting, contrast.
2. ラインスキャンは万能 → 同期と照明が難しい / line scan is always better → harder sync and lighting.
3. 推論時間＝応答時間 → 取得・転送・待ち・通信が加わる / inference time equals response → add acquisition, transfer, queue, comms.
4. 通信成功＝結果が正しい → 別の情報 / communication success equals correctness → different facts.
5. AIのスコア＝校正済み確率 → そうではない / AI score equals calibrated probability → it does not.
