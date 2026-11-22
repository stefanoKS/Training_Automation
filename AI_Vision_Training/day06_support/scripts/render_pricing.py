"""Render Day 6 lesson and source tables from one dated official-pricing snapshot."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

SUPPORT = Path(__file__).resolve().parents[1]
SNAPSHOT = SUPPORT / "pricing" / "pricing_snapshot_2026-11-22.json"
SOURCES = SUPPORT / "pricing" / "pricing_sources_2026-11-22.md"


def load_snapshot() -> dict:
    data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    if data["unit"] != "per 1 million tokens" or data["currency"] != "USD":
        raise ValueError("Unexpected price unit or currency")
    for row in data["entries"]:
        if not row.get("model_id") or not row.get("source") or not row.get("condition"):
            raise ValueError(f"Incomplete pricing source: {row}")
        if not row["source"].startswith("https://"):
            raise ValueError(f"Non-HTTPS official source: {row['source']}")
        if any(row[key] < 0 for key in ("input", "output")):
            raise ValueError(f"Negative price for {row['model_id']}")
    return data


def money(number: float | None) -> str:
    return "Not verified" if number is None else f"${number:g}"


def render_lesson_table(data: dict) -> str:
    rows = [
        "| 提供元・正確なID / Provider and model ID | 入力 / Input | 出力 / Output | キャッシュ読込 / Cached input | 適用条件 / Condition |",
        "|---|---:|---:|---:|---|",
    ]
    for row in data["entries"]:
        rows.append(
            f"| {row['provider']} `{row['model_id']}` | {money(row['input'])} | "
            f"{money(row['output'])} | {money(row['cached_input'])} | {row['condition']} |"
        )
    return "\n".join(rows)


def render_source_document(data: dict) -> str:
    lines = [
        "# 第6日 API価格の出典 / Day 6 official API price sources",
        "",
        f"**確認日 / Verified: {data['verified_on']}.** 単位：米ドル/100万トークン。"
        "利用する前に必ず公式サイトで再確認してください。"
        " / USD per million tokens; check official pricing again before spending.",
        "",
        data["scope"],
        "",
        render_lesson_table(data),
        "",
        "## 条件と出典 / Conditions and official sources",
        "",
    ]
    for row in data["entries"]:
        lines += [
            f"### {row['provider']} — `{row['model_id']}` ({row['tier']})",
            "",
            f"- 適用条件 / Condition: {row['condition']}.",
            f"- 注意 / Caveat: {row['caveat']}",
            f"- 公式資料 / Official source: {row['source']}",
            f"- 確認日 / Verified: {data['verified_on']}.",
            "",
        ]
        if row.get("model_id_source"):
            lines += [f"- IDの出典 / Model ID source: {row['model_id_source']}", ""]
    lines += [
        "## 表の読み方 / How to read the table",
        "",
        "価格は支払い総額ではありません。トークン数、キャッシュ条件、地域、長い文脈、"
        "時間帯、外部ツール、税金、為替、契約条件で変わります。"
        " キャッシュ値が `Not verified` の行は0円という意味ではありません。",
        "",
        "These are not total bills. Token counts, cache eligibility, region, long context,"
        " time of day, external tools, taxes, currency and contracts can change costs."
        " `Not verified` is not a zero price.",
        "",
        "MetaのMuse APIは旧来のLlamaモデルの価格ではありません。オープンウェイト配布と"
        "ホスト型APIは別で、モデルの利用条件も別に確認します。"
        " / Meta Muse hosted API prices do not price Llama or open-weight deployment.",
        "",
    ]
    return "\n".join(lines)


def token_cost(input_tokens: int, output_tokens: int, input_rate: str, output_rate: str) -> Decimal:
    if min(input_tokens, output_tokens) < 0:
        raise ValueError("Token counts must be nonnegative")
    return (
        Decimal(input_tokens) * Decimal(input_rate)
        + Decimal(output_tokens) * Decimal(output_rate)
    ) / Decimal(1_000_000)


if __name__ == "__main__":
    SOURCES.write_text(render_source_document(load_snapshot()), encoding="utf-8")
    print(f"Rendered {SOURCES}")
