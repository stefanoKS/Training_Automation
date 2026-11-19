# Tamang (taj) localization — provenance and review state

このフォルダは **タマン語** の翻訳カタログです。ネパール語（`ne`）の置き換えであり、名前の
付け替えではありません。/ This folder holds the **Tamang** catalogs. It replaces the Nepali
(`ne`) third language; it is not a label rename.

## What is decided, and what is not

| Item | Value | State |
|---|---|---|
| Language | Tamang (Sino-Tibetan / Tibeto-Burman, Nepal) | decided |
| Provisional variety | Eastern Tamang | **UNCONFIRMED** — confirm with the trainees |
| Provisional script | Devanagari | **UNCONFIRMED** — Tamyig is also in use |
| BCP 47 tag used by the PDF exporter | `taj-Deva` | provisional |
| Separate language, never mixed in | Western Tamang (`tdg`) | decided |
| Superseded third language | Nepali in Latin letters (`ne-Latn`) | legacy / rollback only |

Tamang is **not** Nepali. Nepali is Indo-Aryan and is written in the same Devanagari script, so
*script alone proves nothing*: a Devanagari block can be perfectly Nepali and completely wrong as
Tamang. That is why this repository never treats a script test, and never treats machine output, as
evidence of a correct Tamang translation.

## Translation status

**No learner-facing Tamang text has been produced yet.** Every required block is recorded in the
catalogs as `pending` with the reason, instead of being filled with a machine guess or with copied
Nepali:

```
<!-- taj-pending: 1c4cd018 | no dependable reference translation ... -->
```

The production gate reflects that honestly:

```
python assets\scripts\check_localization_coverage.py --locale taj --strict   # exit 1 = BLOCKED
```

## How a block becomes learner-facing

1. A translator (native or advanced Tamang speaker) replaces a `taj-pending` line with a real block:

   ```
   <!-- taj-cell: <cell id> -->
   …Tamang text…
   ```

   For documents, copy the exact key from the pending line (`<!-- taj-section: ## 4. … -->`).
   Repeated headings are qualified with their parent headings, separated by ` > `. Code
   fences and headings inside legacy translations do not define sections.
2. A reviewer reads the block against the Japanese and English source and records the decision:

   ```
   <!-- taj-status: <cell id> approved -->
   <!-- taj-status: ## 4. … | approved -->
   ```

   Machine output stays `draft`; only a reviewer may write `approved`. Set the catalog
   header's `review: approved` and record the actual reviewer (`reviewer:`), traceable
   translation/review record (`provenance:`), and ISO review date (`reviewed-on: YYYY-MM-DD`).
   Keep the locale, BCP 47 tag, script, and variety aligned with the confirmed locale. The
   header is not a substitute for approving every cell or section. A source-only
   `<!-- localization-exempt -->` section body denotes intentionally untranslated scaffolding.
3. `apply_translations.py --locale taj --write` inserts or rewrites the region;
   `apply_docs.py --locale taj --write` does the same for the twelve documents.
4. `check_localization_coverage.py --locale taj --strict` must pass before a booklet is produced.

The Tamang PDF takes its third-language text only from those reviewed blocks. Built-in cover
and navigation labels remain Japanese/English; there is no fallback to Nepali. For a paired
heading, use `after-heading` with `<!-- taj-pair: Exact English heading -->` and a translated
Markdown heading. For a translated figure caption, start the first paragraph of an
`after-image:` block with `<!-- taj-caption -->`, then put the caption on the next line.

## Files

| Path | Purpose |
|---|---|
| `notebooks/<stem>.taj.md` | one catalog per notebook (16) |
| `docs/<name>.taj.md` | one catalog per learner document (12) |
| `terminology.md` | term list with review state — **no invented equivalents** |
| `coverage_inventory.json` | machine-readable inventory produced by the coverage tool |

## Resources that would be needed

* A native or advanced Tamang speaker (Eastern Tamang) willing to review, and the trainees' answer
  on variety and script.
* Reference material in a legally usable form: a Tamang–Nepali/English dictionary or word list, and
  official curriculum text where available. Kathmandu University's ILPRL/TMT material was **not**
  reachable from this environment; no text from it was copied or paraphrased.

Without those, the pending blocks stay pending. **Do not** fill them from Nepali, Hindi, or
machine-translated English.
