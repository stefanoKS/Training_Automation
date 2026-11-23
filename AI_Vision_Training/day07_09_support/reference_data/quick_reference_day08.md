# 第8日 公式・確認カード / Day 8 formula and check card

> このカードは学習用です。実機の配線・通電・安全設計を承認するものではありません。
> This card is for learning. It does not approve real wiring, energisation or safety design.

## 1. 電気の基本 / electrical basics

```text
V = I × R
P = V × I = I²R = V²/R
```

**例 / example**: DC24V・6Wランプ → I = 6/24 = **0.25 A**、R ≈ **96 Ω**（動作点）。
**Example**: 6 W lamp at 24 V → I = **0.25 A**, R ≈ **96 Ω** at the operating point.

**負荷合計 / load total**: 3 W×2 + 0.06 A×3 + 0.15 A×2 → 0.25 + 0.18 + 0.30 = **0.73 A**（定常）。
**Load total**: two 3 W lamps + three 0.06 A sensors + two 0.15 A valves → 0.25 + 0.18 + 0.30 = **0.73 A** steady state.

> 0.73 A は電源選定の承認ではありません。突入電流・定格低下・電線・端子・保護を別に確認します。
> 0.73 A is not approval of a supply selection. Check inrush, derating, wiring, terminals and protection separately.

## 2. 統一I/O表 / canonical I/O

| アドレス / Address | 機器 / Device | 正常時 / Normal |
|---|---|---|
| X0 | START pushbutton | OFF; ON while pressed |
| X1 | STOP_OK (physical NC) | ON while healthy |
| X2 | retracted confirmation | ON at retracted end |
| X3 | extended confirmation | ON at extended end |
| M0 | RUN state | OFF at power-up |
| Y0 | RUN lamp | OFF when stopped |
| Y1 | delayed lamp (T0 done) | OFF before 3 s |
| Y2 | extend solenoid command | OFF = spring return (training valve) |
| T0 | 3 s on-delay timer | 0 when RUN off |

> Y1は遅延ランプ専用。電磁弁はY2。アドレスは物理端子番号ではない。
> Y1 is only the delayed lamp. The solenoid is Y2. Addresses are not physical terminals.

## 3. 自己保持 / self-holding

```text
(X0 AND X2) OR M0   → 直列 X1 → コイル M0
```

- M0の保持枝はX2を通らない / the M0 seal-in branch does not pass through X2.
- STARTを離してもRUNが続く / RUN survives START release.
- X1（停止許可）がOFFでRUNが落ち、T0がリセット / X1 OFF drops RUN and resets T0.
- 復電時は新しいSTARTが必要 / a fresh START is required after power restoration.

## 4. シーケンス状態 / sequence states

IDLE → READY → EXTEND → WAIT_EXTENDED → RETRACT → WAIT_RETRACTED → COMPLETE → FAULT

| 故障 / Fault | 検出 / Detection | 応答 / Response |
|---|---|---|
| F001 | 前進端が時間内に来ない / no X3 before timeout | Y2 OFF, RUN OFF, FAULT |
| F002 | X2とX3が同時ON / both end sensors ON | 全出力OFF / all outputs OFF |
| F003 | 後退端が時間内に来ない / no X2 before timeout | Y2 OFF, RUN OFF, FAULT |

## 5. 提出前チェック / pre-submission checks

- [ ] 物理NO/NCと論理接点を区別した / separated physical and logical contacts
- [ ] NPN/PNPを入力共通端子まで説明した / explained NPN/PNP through the input common
- [ ] 出力定格とサージ対策を確認した / checked output ratings and surge suppression
- [ ] 自己保持の保持接点を書いた / included the seal-in contact
- [ ] 位置確認とタイムアウトを状態に含めた / included position confirmation and timeouts
- [ ] リセットが動作開始でないことを確認した / verified reset is not a start
- [ ] 復電時の自動再起動を防いだ / prevented automatic restart on power restoration
- [ ] 通常制御と安全機能を区別した / separated ordinary control from safety functions
