# 第9日 公式・確認カード / Day 9 formula and check card

> このカードは学習用です。実ネットワークの変更や投資判断を承認するものではありません。
> This card is for learning. It does not approve a real network change or an investment decision.

## 1. IPv4とサブネット / IPv4 and subnets

| 項目 / Item | /24 例 / example | /25 例 / example |
|---|---|---|
| IP | 192.168.10.10 | 192.168.10.130 |
| マスク / mask | 255.255.255.0 | 255.255.255.128 |
| ネットワーク / network | 192.168.10.0 | 192.168.10.128 |
| ブロードキャスト / broadcast | 192.168.10.255 | 192.168.10.255 |
| 割当可能 / assignable | .1–.254 (254) | .129–.254 (126) |

- 同一サブネットは、同じマスクで計算したネットワークアドレスが一致するかで判定 / same subnet = equal network addresses under the same mask.
- /31はRFC 3021のポイントツーポイント、/32は単一ホスト / /31 is RFC 3021 point-to-point; /32 is a single host.
- 同じ第3オクテットでも、/25では別サブネットになり得る / the same third octet can be a different /25 subnet.

## 2. 通信の層 / communication layers

| 層 / Layer | 決めること / Decides |
|---|---|
| IP | どの機器へ / which device |
| ポート / port | どのサービスへ / which service |
| TCP / UDP | どう運ぶか / how data is carried |
| アプリ / application | データの意味 / meaning of the data |

- リンクOK ≠ IP OK ≠ アプリOK / link OK does not imply IP or application success.
- ping成功はModbus成功を保証しない / ping success does not guarantee Modbus success.
- 通信喪失時の機械動作を設計する / design machine behaviour on communication loss.

## 3. 段階ゲート / staged gates

G0 文書 → G1 機械 → G2 電気（隔離）→ G3 オフライン → G4 監督下準備 → G5 通電（任意）→ G6 受入

- G5は課程の必須ではない / G5 is not required for this course.
- 未実施はBLOCKEDまたはNOT TESTED / unperformed tests are BLOCKED or NOT TESTED.
- BLOCKEDをPASSにしない / never turn BLOCKED into PASS.
- リセットは動作開始ではない / reset is not a start.

## 4. 試験記録 / test record fields

試験ID、要求ID、前提、手順、期待、実測、合否、証跡、実施者、日付、是正処置
Test ID, requirement ID, preconditions, procedure, expected, actual, status, evidence, operator, date, corrective action.

## 5. 費用対効果 / cost and benefit

```text
年間効果 = 削減時間/日 × 稼働日 × 時間単価
回収期間 = 投資 ÷ (年間効果 − 年間運用費)
```

**例 / example**: 12 s × 180回/日 = 36 min/日 → 0.6 h/日 × 220日 × 2,400円 = **316,800円/年**。
設備450,000円 → **約1.42年**（単純回収、運用費0の仮定）。
**Example**: 12 s × 180/day = 36 min/day → **316,800 JPY/year**; 450,000 JPY → **about 1.42 years** (simple payback, zero operating cost assumption).

> 316,800円は労務時間の仮換算であり、実現する利益とは限りません。運用費・停止損失・品質・教育・税金・減価償却は別に評価します。
> 316,800 JPY is a hypothetical labour-time conversion, not guaranteed profit. Evaluate operating cost, downtime, quality, training, tax and depreciation separately.

## 6. 提出前チェック / pre-submission checks

- [ ] IP割当表と構成図を作った / built the IP allocation table and network diagram
- [ ] 同一/別サブネットを判定した / judged same/different subnet
- [ ] 通信喪失時の動作を書いた / wrote behaviour on communication loss
- [ ] ゲートと試験記録を作った / built gates and test records
- [ ] BLOCKEDをPASSにしなかった / did not record BLOCKED as PASS
- [ ] 投資・運用費・効果・回収を分けた / separated investment, operating cost, benefit and payback
- [ ] 危険源と専門レビュー項目を書いた / wrote hazards and expert-review items
- [ ] 次のステップに責任者と期限を書いた / wrote next steps with owners and dates
