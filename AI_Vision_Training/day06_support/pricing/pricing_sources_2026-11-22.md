# 第6日 API価格の出典 / Day 6 official API price sources

**確認日 / Verified: 2026-11-22.** 単位：米ドル/100万トークン。利用する前に必ず公式サイトで再確認してください。 / USD per million tokens; check official pricing again before spending.

Representative hosted API standard-rate examples; not a quote or universal comparison

| 提供元・正確なID / Provider and model ID | 入力 / Input | 出力 / Output | キャッシュ読込 / Cached input | 適用条件 / Condition |
|---|---:|---:|---:|---|
| OpenAI `gpt-6-luna` | $0.1 | $0.5 | $0.01 | Standard; short context |
| OpenAI `gpt-6.2-astra` | $8 | $40 | $0.4 | Standard; short context |
| Google Gemini `gemini-4-hydrogen` | $1.5 | $7.5 | $0.075 | Gemini Developer API paid standard tier |
| Google Gemini `gemini-4-carbon` | $2 | $10 | $0.1 | Paid standard tier through 2026-11-30 |
| Anthropic `claude-haiku-5-5` | $0.1 | $0.5 | $0.01 | Prompt up to 100,000 tokens |
| Anthropic `claude-fable-5-2` | $8 | $40 | $0.2 | Standard Claude API |
| DeepSeek `deepseek-flash` | $0.15 | $0.6 | $0.003 | Off-peak; input cache miss |
| DeepSeek `deepseek-v4-pro` | $0.66 | $1.98 | $0.022 | Off-peak; input cache miss |
| Mistral AI `ministral-3-3b-25-12` | $0.1 | $0.1 | Not verified | Official model page rate |
| Mistral AI `mistral-large-4-0` | $0.7 | $2.1 | $0.07 | Official model page rate |
| xAI `grok-build-0.1` | $1 | $2 | $0.2 | Prompt below 200,000 tokens |
| xAI `grok-4.7` | $2 | $6 | $0.5 | Prompt below 200,000 tokens |
| Alibaba Cloud Qwen `qwen3.8-flash` | $0.15 | $0.47 | Not verified | Model Studio International; 0 < input tokens <= 1M |
| Alibaba Cloud Qwen `qwen3.8-max` | $2 | $6 | Not verified | Model Studio International; 0 < input tokens <= 1M |
| Meta `muse-ember-1.0` | $0.1 | $0.5 | $0.004 | Meta Model API Standard; up to 200K input tokens |
| Meta `muse-wonder-1.0` | $4 | $20 | $0.2 | Meta Model API Standard |

## 条件と出典 / Conditions and official sources

### OpenAI — `gpt-6-luna` (lower-cost)

- 適用条件 / Condition: Standard; short context.
- 注意 / Caveat: Long-context, cache-write and Batch/Flex rates differ.
- 公式資料 / Official source: https://developers.openai.com/api/docs/pricing.md
- 確認日 / Verified: 2026-11-22.

### OpenAI — `gpt-6.2-astra` (higher-capability)

- 適用条件 / Condition: Standard; short context.
- 注意 / Caveat: Long-context input $16 and output $60 per 1M; cache writes separately priced.
- 公式資料 / Official source: https://developers.openai.com/api/docs/pricing.md
- 確認日 / Verified: 2026-11-22.

### Google Gemini — `gemini-4-hydrogen` (lower-cost example)

- 適用条件 / Condition: Gemini Developer API paid standard tier.
- 注意 / Caveat: Thinking tokens are included in output billing; free-tier availability and data terms differ.
- 公式資料 / Official source: https://aistudio.google.com/docs/pricing
- 確認日 / Verified: 2026-11-22.

### Google Gemini — `gemini-4-carbon` (higher-capability)

- 適用条件 / Condition: Paid standard tier through 2026-11-30.
- 注意 / Caveat: From 2026-12-01: input $4, output $20, cached $0.20 per 1M; grounding may cost extra.
- 公式資料 / Official source: https://aistudio.google.com/docs/pricing
- 確認日 / Verified: 2026-11-22.

### Anthropic — `claude-haiku-5-5` (lower-cost)

- 適用条件 / Condition: Prompt up to 100,000 tokens.
- 注意 / Caveat: Above 100K: input $0.50, output $2.50, cache read $0.05; cache writes cost extra.
- 公式資料 / Official source: https://platform.claude.com/docs/en/about-claude/pricing
- 確認日 / Verified: 2026-11-22.

- IDの出典 / Model ID source: https://platform.claude.com/docs/en/models/overview

### Anthropic — `claude-fable-5-2` (higher-capability)

- 適用条件 / Condition: Standard Claude API.
- 注意 / Caveat: Five-minute cache writes $10 and one-hour writes $16 per 1M; partner cloud pricing may differ.
- 公式資料 / Official source: https://platform.claude.com/docs/en/about-claude/pricing
- 確認日 / Verified: 2026-11-22.

- IDの出典 / Model ID source: https://platform.claude.com/docs/en/models/overview

### DeepSeek — `deepseek-flash` (lower-cost)

- 適用条件 / Condition: Off-peak; input cache miss.
- 注意 / Caveat: Peak: input $0.30, output $1.20, cached $0.006 per 1M; time windows are published in UTC.
- 公式資料 / Official source: https://api-docs.deepseek.com/quick_start/pricing
- 確認日 / Verified: 2026-11-22.

### DeepSeek — `deepseek-v4-pro` (higher-capability)

- 適用条件 / Condition: Off-peak; input cache miss.
- 注意 / Caveat: Peak: input $1.32, output $3.96, cached $0.044 per 1M; vision not supported.
- 公式資料 / Official source: https://api-docs.deepseek.com/quick_start/pricing
- 確認日 / Verified: 2026-11-22.

### Mistral AI — `ministral-3-3b-25-12` (lower-cost)

- 適用条件 / Condition: Official model page rate.
- 注意 / Caveat: Cached input price not verified on this model page; model ID uses official page identifier.
- 公式資料 / Official source: https://docs.mistral.ai/models/ministral-3-3b-25-12
- 確認日 / Verified: 2026-11-22.

### Mistral AI — `mistral-large-4-0` (higher-capability)

- 適用条件 / Condition: Official model page rate.
- 注意 / Caveat: Open-weight model; local deployment costs are not API charges; model ID uses official page identifier.
- 公式資料 / Official source: https://docs.mistral.ai/models/mistral-large-4-0
- 確認日 / Verified: 2026-11-22.

### xAI — `grok-build-0.1` (coding-focused)

- 適用条件 / Condition: Prompt below 200,000 tokens.
- 注意 / Caveat: At or above 200K prompt tokens, all tokens in a request use input $2/output $4/cached $0.40 rates.
- 公式資料 / Official source: https://docs.x.ai/developers/models
- 確認日 / Verified: 2026-11-22.

### xAI — `grok-4.7` (higher-capability)

- 適用条件 / Condition: Prompt below 200,000 tokens.
- 注意 / Caveat: At or above 200K prompt tokens, all tokens use input $4/output $12/cached $1 rates.
- 公式資料 / Official source: https://docs.x.ai/developers/models
- 確認日 / Verified: 2026-11-22.

### Alibaba Cloud Qwen — `qwen3.8-flash` (lower-cost)

- 適用条件 / Condition: Model Studio International; 0 < input tokens <= 1M.
- 注意 / Caveat: Regional prices differ; discounted cache rate mentioned but numeric cache-hit price not verified.
- 公式資料 / Official source: https://www.alibabacloud.com/help/en/model-studio/model-pricing
- 確認日 / Verified: 2026-11-22.

### Alibaba Cloud Qwen — `qwen3.8-max` (higher-capability)

- 適用条件 / Condition: Model Studio International; 0 < input tokens <= 1M.
- 注意 / Caveat: Regional prices differ; discounted cache rate mentioned but numeric cache-hit price not verified.
- 公式資料 / Official source: https://www.alibabacloud.com/help/en/model-studio/model-pricing
- 確認日 / Verified: 2026-11-22.

### Meta — `muse-ember-1.0` (lower-cost)

- 適用条件 / Condition: Meta Model API Standard; up to 200K input tokens.
- 注意 / Caveat: Above 200K the whole request uses input $0.30/output $1.50/cached $0.012; Contributor mode changes data terms.
- 公式資料 / Official source: https://dev.meta.ai/docs/pricing-rate-limits.md
- 確認日 / Verified: 2026-11-22.

### Meta — `muse-wonder-1.0` (higher-capability)

- 適用条件 / Condition: Meta Model API Standard.
- 注意 / Caveat: Hosted Muse pricing, not a price for open-weight Llama; other tool services may charge separately.
- 公式資料 / Official source: https://dev.meta.ai/docs/pricing-rate-limits.md
- 確認日 / Verified: 2026-11-22.

## 表の読み方 / How to read the table

価格は支払い総額ではありません。トークン数、キャッシュ条件、地域、長い文脈、時間帯、外部ツール、税金、為替、契約条件で変わります。 キャッシュ値が `Not verified` の行は0円という意味ではありません。

These are not total bills. Token counts, cache eligibility, region, long context, time of day, external tools, taxes, currency and contracts can change costs. `Not verified` is not a zero price.

MetaのMuse APIは旧来のLlamaモデルの価格ではありません。オープンウェイト配布とホスト型APIは別で、モデルの利用条件も別に確認します。 / Meta Muse hosted API prices do not price Llama or open-weight deployment.
