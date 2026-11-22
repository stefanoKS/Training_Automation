# 記入例：機械構成図 / Worked example: Machine Component Map

**架空の記入例です。数値・型番は含みません。 / A fictional worked example with no specifications.**

| 部品 / component | 役割 / purpose | 位置 / location | 信号・エネルギー / signal or energy | 故障の例 / failure example | 安全メモ / safety note |
|---|---|---|---|---|---|
| 供給ロール / supply roll | 材料を供給 / feeds material | 上流 / upstream | 機械 / mechanical | 材料切れ / material run-out | 回転部に注意 / rotating part |
| ガイドローラ / guide rollers | 方向と張力 / direction and tension | 上流〜検査前 / upstream | 機械 / mechanical | 偏り・摩耗 / misalignment, wear | 巻き込み / nip point |
| 検査カメラ / inspection camera | 画像取得 / image capture | 検査点 / inspection point | 画像データ / image data | ピントずれ / focus loss | ブラケット固定 / secure mount |
| 照明 / illumination | 見え方の安定 / stable appearance | カメラ付近 / near camera | 電力 / power | 汚れ・劣化 / contamination, aging | 高輝度光に注意 / bright light |
| エンコーダ / encoder | 移動量 / travel | 搬送軸 / transport shaft | パルス / pulses | 断線 / open circuit | 取付と配線 / mounting and wiring |
| PLC | 制御 / control | 制御盤 / cabinet | 信号 / signals | 出力停止 / output failure | 安全系とは別 / separate from safety |

**因果の記入例 / causal chain example:** ベアリング摩耗 → ローラ振れ → 画像ぼけ → 小さな欠陥の見落とし。
Bearing wear → roller run-out → blurred image → missed fine defects.
