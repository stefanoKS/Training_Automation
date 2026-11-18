# Romanized Nepali style guide / रोमन नेपाली लेख्ने नियम

The third language of this course is **Nepali written with Latin letters** (BCP 47 `ne-Latn`).
It is not English, not Hindi, and not a new language. Files that are migrated carry `ne-Latn`
everywhere and never a mixture:

```
JA  このノートブックの使い方
EN  How to use this notebook
NE  Yo notebook kasari prayog garne
```

The canonical text lives in the sidecar catalogs (`assets/i18n/ne/notebooks/*.ne.md`,
`assets/i18n/ne/docs/*.ne.md`). `assets/scripts/romanize_nepali.py` holds the machine-readable half
of this guide (`GLOSSARY`) and the acceptance test (`looks_like_nepali_latin`), so an automated
check can tell Romanized Nepali from copied English.

## How the migration works

* `assets/scripts/convert_nepali_to_latin.py --scope docs --write` rewrites a catalog in place.
  `--review` lists every word that falls back to the rule engine, which is the queue for the human
  reviewer.
* A word listed in `GLOSSARY` uses that spelling exactly. Everything else is transliterated with
  the published rules below, so the result is never random.
* Applying a catalog twice is a no-op; the appliers and the coverage checker refuse a block that is
  neither Devanagari Nepali nor Romanized Nepali.

## Spelling rules

1. **ASCII only.** No Devanagari, no academic diacritics (`ā`, `ī`, `ṇ`). `aa` is written only
   where the word would otherwise be misread (`kaam`, `jaanch`, `naam`, `baat`).
2. **Short vowels.** `ि`/`ी` both become `i`, `ु`/`ू` both become `u`, and a word-final long `ा`
   becomes `a` (`डेटा` → `data`, `तालिका` → `talika`).
3. **`व` is written `b`** (`वास्तविक` → `bastabik`, `विधि` → `bidhi`). The conjunction `वा`
   ("or") stays `wa`, and `ओ`/`औ` stay `o`/`au`.
4. **Word-final inherent vowel is dropped** (`काम` → `kaam`, `तस्बिर` → `tasbir`, `दोष` → `dosh`).
   Single-letter words and words ending in `-छ` keep it (`र` → `ra`, `हुन्छ` → `hunchha`).
5. **Postpositions.** `मा`, `बाट`, `सँग`, `लाई`, `देखि`, `सम्म` are written apart
   (`data ma`, `tasbir baat`); `को`, `का`, `की`, `ले`, `हरू` stay attached (`tasbirko`,
   `notebookle`, `tasbirharu`).
6. **Technical tokens stay exactly as in the code**: `YOLO`, `PatchCore`, `Anomalib`, `train`,
   `val`, `test`, `calibration`, `image_AUROC`, `F1Score`, `precision`, `recall`, `TP/FP/FN/TN`,
   `.venv`, `python`, `cmd`, paths, file names, URLs, numbers, units and operators.
7. **Punctuation.** A Devanagari danda `।` becomes `.`. Colons inside Nepali lines are ASCII `:`.
8. **One idea, one spelling.** Do not alternate `thresold`/`threshold`/`threshhold`; use the
   glossary form.
9. **`-एर` converbs keep the final `a`** (`बनाएर` → `banaera`, `चलाएर` → `chalaera`,
   ` पढेर` → `padhera`). The letter rules alone stop at `र` and produce `banaer`, which cannot be
   read aloud, so every converb the course uses is listed in `GLOSSARY`.
10. **A final `र`/`न`/`ल` after another consonant takes an `a`** (`भित्र` → `bhitra`,
    `क्षेत्र` → `kshetra`, `गन्न` → `ganna`, `निकाल्न` → `nikalna`). Rule 4 still drops the
    ordinary word-final vowel (`काम` → `kaam`); this rule only rescues the clusters that would
    otherwise end a word in three consonants.

## Layout review rules

* The empty `before`/`after` margins of `<!-- ne:begin … -->` regions are not content: only the
  text between the markers is translated.
* When the glossary grows, `convert_nepali_to_latin.py` re-applies the reviewed spellings to
  catalogs that are already Latin. Only unambiguous rules are rewritten: when two Devanagari words
  collapse onto the same Latin form (`हुन` and `हुन्` both give `hun`) they are different words, so
  both are left alone, and short forms such as `ab`, `bat`, `man` or the file token `path` are
  never touched.

## Approved glossary (operator training)

| 日本語 | English | Romanized Nepali (`ne-Latn`) |
| --- | --- | --- |
| 画像 | image | `tasbir` |
| 画素 / ピクセル | pixel | `pixel` |
| データ | data | `data` |
| モデル | model | `model` |
| 学習 / 訓練 | training | `prashikshan` (`talim` for the course itself) |
| 較正 | calibration | `calibration` |
| 試験 | test | `parikshan` (`test` for the data partition) |
| 評価 | evaluation | `mulyankan` |
| しきい値 | threshold | `threshold` |
| 正常 | normal | `samanya` |
| 異常 | abnormal | `asamanya` |
| 欠陥 / 不良 | defect | `dosh` |
| 誤報 | false alarm | `jhuto alarm` |
| 見逃し | miss / false negative | `chhutne dosh` |
| スコア | score | `score` |
| 記憶 / メモリバンク | memory bank | `memory bank` |
| 最近傍 | nearest neighbour | `najikako chhimeki` |
| バウンディングボックス | bounding box | `bounding box` (`ayat`) |
| 正規化座標 | normalised coordinate | `samanyikrit nirdeshangk` |
| データ漏れ | data leakage | `data chuhabat` |
| 固定 | freeze | `sthir garnu` |
| 分割 | partition / split | `bhaag` / `bibhajan` |
| 保存 | save | `surakshit garnu` |
| 確認する | check | `jaanch garnu` |
| 実行する | run | `chalaunu` |
| 記録 | record | `abhilekh` |
| 再現性 | reproducibility | `punarutpadanshilata` |
| 過学習 | overfitting | `obharaphiting` |
| 精度 | precision | `precision` |
| 再現率 | recall | `recall` |
| 結果 | result | `natija` |
| 図 / 画像の説明 | figure / caption | `chitra` / `caption` |
| 質問 / 答え | question / answer | `prashna` / `uttar` |
| 演習 | exercise | `abhyas` |
| 注意 | caution | `dhyan dinuparne kura` |
| 任意 | optional | `baikalpik` |
| 必須 | required | `aniwarya` |
| 意味 | meaning | `arth` |
| 理由 | reason | `karan` |
| 値 | value | `maan` |
| …の中 / 内側 | inside | `bhitra` |
| …して（連用） | by doing | `-era` (`banaera`, `chalaera`) |
| 斜辺 | hypotenuse | `karna` |

## Review checklist (required before sign-off)

- [ ] Every heading, warning, exercise instruction and table header reads as Nepali grammar, not as
      English word order.
- [ ] Operators that matter are unchanged: `>=`, `<`, `%`, class IDs, partition names, `0–1`
      scores, `nan`.
- [ ] "only on calibration" and "after freeze" keep their force; an optional exercise still says it
      is optional (`baikalpik`, `aniwarya hoina`).
- [ ] Command lines, file names and numbers are byte-identical to the Japanese/English source.
- [ ] No Devanagari remains inside a migrated block, and no block is English copied as "Nepali".
- [ ] The `--review` word list has been read, and every surprising spelling was either glossed or
      accepted deliberately. The reviewed spellings of the `-एर` converbs and of the words that
      end in a consonant cluster live in `GLOSSARY`; the remaining rule-engine forms
      (`utpadanako`, `tinabata`, `pikselama`) are accepted as they are.

Automated tests can prove structure, coverage and script. They **cannot** certify conversational
fluency: a native or advanced Nepali reviewer must sign off the wording before the course is taught.
