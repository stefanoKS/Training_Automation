"""नेपाली लाई रोमनमा लेख्ने / Write Nepali with Latin (Roman) letters.

The course ships three languages in this order: Japanese, English, Romanized Nepali
(BCP 47 ``ne-Latn``). Romanized Nepali is **Nepali words and grammar written in Latin
letters** — ``Yo notebook kasari prayog garne?`` — not an English translation and not a
character-by-character transliteration.

Two layers do the work:

* ``GLOSSARY`` — the reviewed spelling of the words this course uses most. The style guide in
  ``assets/i18n/ne/romanization_style_guide.md`` is the human-readable half of this table.
* ``romanize_word`` — a deterministic fallback for anything the glossary does not list, so an
  unmapped word never stops the build.

``romanize_text`` touches only Devanagari runs. Code spans, file names, URLs, numbers, table
pipes, HTML comments and existing Latin text pass through byte for byte, which is what keeps the
catalog anchors and the copied CMD lines intact.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

COURSE_ROOT = Path(__file__).resolve().parents[2]
CATALOG_ROOT = COURSE_ROOT / "assets" / "i18n" / "ne"

DEVANAGARI_RE = re.compile(r"[\u0900-\u097f]")
RUN_RE = re.compile(r"[\u0900-\u097f\u200c\u200d]+")
DIGITS = "०१२३४५६७८९"

INDEPENDENT_VOWELS = {
    "अ": "a", "आ": "a", "इ": "i", "ई": "i", "उ": "u", "ऊ": "u",
    "ऋ": "ri", "ॠ": "ri", "ऌ": "li", "ए": "e", "ऐ": "ai",
    "ओ": "o", "औ": "au", "अं": "an", "अः": "ah",
}

CONSONANTS = {
    "क": "k", "ख": "kh", "ग": "g", "घ": "gh", "ङ": "ng",
    "च": "ch", "छ": "chh", "ज": "j", "झ": "jh", "ञ": "n",
    "ट": "t", "ठ": "th", "ड": "d", "ढ": "dh", "ण": "n",
    "त": "t", "थ": "th", "द": "d", "ध": "dh", "न": "n",
    "प": "p", "फ": "ph", "ब": "b", "भ": "bh", "म": "m",
    "य": "y", "र": "r", "ल": "l", "व": "b", "श": "sh",
    "ष": "sh", "स": "s", "ह": "h", "ळ": "l", "ऱ": "r",
    "क़": "q", "ख़": "kh", "ग़": "g", "ज़": "j", "ड़": "r", "ढ़": "rh",
    "फ़": "f", "य़": "y", "ऩ": "n", "ऱ": "r",
}

CONJUNCTS = {
    "क्ष": "ksh", "त्र": "tr", "ज्ञ": "gy", "श्र": "shr", "द्य": "dy",
    "द्व": "dw", "द्ध": "ddh", "ट्ट": "tt", "त्त": "tt", "न्न": "nn",
    "म्म": "mm", "ल्ल": "ll", "च्च": "chch", "क्क": "kk", "ग्ग": "gg",
    "न्ध": "ndh", "म्ब": "mb", "न्द": "nd", "न्त": "nt", "म्प": "mp",
    "ङ्क": "nk", "ञ्च": "nch", "ञ्ज": "nj", "ष्ट": "sht", "स्ट": "st",
    "स्प": "sp", "स्त": "st", "स्क": "sk", "स्व": "sw", "स्र": "sr",
}

MATRAS = {
    "ा": "a", "ि": "i", "ी": "i", "ु": "u", "ू": "u", "ृ": "ri",
    "े": "e", "ै": "ai", "ो": "o", "ौ": "au", "ॢ": "li", "ॣ": "li",
}
SIGNS = {"ं": "n", "ँ": "n", "ः": "h", "ऽ": "'"}
VIRAMA = "\u094d"

# Postpositions and plural markers attach to the noun in Devanagari. Romanized Nepali writes the
# short ones apart ("data ma", "tasbir baat") and the genitive/ergative ones joined
# ("tasbirko", "notebookle"), which is what the course style guide shows.
SUFFIX_SPACED = {
    "मा": "ma", "बाट": "baat", "सँग": "sang", "लाई": "lai",
    "देखि": "dekhi", "सम्म": "samma", "जस्तै": "jastai", "अनुसार": "anusar",
}
SUFFIX_JOINED = {
    "को": "ko", "का": "ka", "की": "ki", "ले": "le", "हरू": "haru",
    "हरूको": "haruko", "हरूमा": "haruma", "हरूले": "harule",
}

# Reviewed spellings for the words this course uses most. Keep one spelling per idea; the style
# guide explains the choices. Anything not listed falls back to ``romanize_word``.
GLOSSARY = {
    "नेपाली": "Nepali", "जापानी": "Japani", "अङ्ग्रेजी": "Angreji",
    "दिन": "din", "नोटबुक": "notebook", "पाठ": "paath", "भाग": "bhaag",
    "उदाहरण": "udaharan", "प्रश्न": "prashna",
    "उत्तर": "uttar", "काम": "kaam", "समय": "samay", "मिनेट": "minet",
    "लक्ष्य": "lakshya", "पूर्वशर्त": "poorwashart",
    "तस्बिर": "tasbir", "चित्र": "chitra", "तालिम": "talim",
    "प्रशिक्षण": "prashikshan", "परीक्षण": "parikshan",
    "क्यालिब्रेसन": "calibration",
    "डेटा": "data", "डेटासेट": "dataset",
    "मोडेल": "model", "थ्रेसहोल्ड": "threshold",
    "सामान्य": "samanya", "असामान्य": "asamanya", "दोष": "dosh",
    "नतिजा": "natija", "सङ्ख्या": "sankhya", "मान": "maan", "स्तर": "star",
    "तस्बिर-स्तर": "tasbir-star", "वस्तु-स्तर": "wastu-star",
    "फाइल": "file", "फोल्डर": "folder", "बाटो": "bato", "नाम": "naam",
    "सेटिङ": "setting", "सेटिङमा": "setting ma", "सेल": "cell",
    "कर्नेल": "kernel", "मेमोरी": "memory", "ब्याङ्क": "bank",
    "स्कोर": "score", "स्कोरको": "scoreko", "म्याप": "map",
    "इनपुट": "input", "हिटम्याप": "heatmap", "हिटम्यापको": "heatmapko",
    "आउटपुट": "output", "नम्बर": "number", "वर्गीकरण": "bargikaran",
    "विवरण": "biwaran", "वाक्य": "baky", "वाक्यमा": "bakyama",
    "सुरक्षित": "surakshit", "जाँच": "jaanch", "जाँच्नुहोस्": "jaanchnuhos",
    "गर्नुहोस्": "garnuhos", "हेर्नुहोस्": "hernuhos",
    "चलाउनुहोस्": "chalaunuhos", "लेख्नुहोस्": "lekhnuhos",
    "पढ्नुहोस्": "padhnuhos", "भन्नुहोस्": "bhannuhos",
    "राख्नुहोस्": "rakhnuhos", "छान्नुहोस्": "chhannuhos",
    "बदल्नुहोस्": "badalnuhos", "मिलाउनुहोस्": "milaunuhos",
    "सम्झनुहोस्": "samjhanuhos", "नठान्नुहोस्": "nathaannuhos",
    "भन्ने": "bhanne", "गर्ने": "garne", "हुने": "hune", "दिने": "dine",
    "पर्ने": "parne", "सक्ने": "sakne", "रहने": "rahane", "लिने": "line",
    "छ": "chha", "छन्": "chhan", "छैन": "chhaina", "छैनन्": "chhainan",
    "हो": "ho", "हुन्": "hun", "हुन्छ": "hunchha", "हुन्छन्": "hunchhan",
    "गर्छ": "garchha", "गर्छन्": "garchhan", "पर्छ": "parchha",
    "सक्छ": "sakchha", "दिन्छ": "dinchha", "जान्छ": "janchha",
    "लाग्छ": "lagchha", "देखिन्छ": "dekhinchha", "बन्छ": "banchha",
    "आउँछ": "aaunchha", "रहन्छ": "rahanchha", "होइन": "hoina",
    "हुनुहुन्छ": "hunuhunchha", "गर्नुहुन्छ": "garnuhunchha",
    "थियो": "thiyo", "थिए": "thie", "हुन्थ्यो": "hunthyo",
    "गर्न": "garna", "हुन": "huna", "लिन": "lina",
    "पर्न": "parna", "सक्न": "sakna", "राख्न": "rakhna", "छान्न": "chhanna",
    "पढ्न": "padhna", "लेख्न": "lekhna", "हेर्न": "herna", "जाँच्न": "jaanchna",
    "बदल्न": "badalna", "मिलाउन": "milauna", "देखाउन": "dekhauna",
    "गरेर": "garera", "गरेपछि": "garepachhi", "हेरेपछि": "herepachhi",
    "पछि": "pachhi", "अघि": "aghi", "पहिले": "pahile", "अहिले": "ahile",
    "त्यसपछि": "tyaspachhi", "यसपछि": "yaspachhi", "सकेपछि": "sakepachhi",
    "बेला": "bela", "बेलामा": "belama", "समयमा": "samayma",
    "मा": "ma", "मा।": "ma.", "लाई": "lai", "ले": "le", "को": "ko",
    "का": "ka", "की": "ki", "बाट": "baat", "सँग": "sang", "सँगै": "sangai",
    "र": "ra", "वा": "wa", "तर": "tar", "पनि": "pani",
    "अनि": "ani", "किन": "kina", "कसरी": "kasari", "के": "ke",
    "कुन": "kun", "कति": "kati", "कहाँ": "kahan", "कहिले": "kahile",
    "यो": "yo", "त्यो": "tyo", "यी": "yi", "ती": "ti", "यस": "yas",
    "त्यस": "tyas", "यहाँ": "yahan", "त्यहाँ": "tyahan", "यसै": "yasai",
    "एउटा": "euta", "एक": "ek", "दुई": "dui", "तीन": "tin", "चार": "chaar",
    "पाँच": "paanch", "सबै": "sabai", "धेरै": "dherai",
    "थोरै": "thorai", "अलि": "ali", "अझै": "ajhai", "अब": "aba",
    "फेरि": "feri", "दोहोरो": "dohoro", "दोहोर्याउनुहोस्": "dohoryaunuhos",
    "अनुमान": "anuman", "अनुमान गर्नुहोस्": "anuman garnuhos",
    "सोच्नुहोस्": "sochnuhos", "ध्यान": "dhyan", "दिनुपर्ने": "dinuparne",
    "कुरा": "kura", "कुराहरू": "kuraharu", "कुरालाई": "kuralai",
    "किनभने": "kinabhane", "भने": "bhane", "भनेर": "bhanera",
    "भएको": "bhaeko", "भएका": "bhaeka", "भए": "bhae", "भयो": "bhayo",
    "हुनेछ": "hunechha", "हुनेछैन": "hunechhaina", "सकिँदैन": "sakindaina",
    "मिल्दैन": "mildaina", "हुँदैन": "hundaina", "गर्दैन": "gardaina",
    "पर्दैन": "pardaina",
    "ठुलो": "thulo", "सानो": "sano", "राम्रो": "ramro", "नराम्रो": "naramro",
    "उच्च": "uchcha", "न्यून": "nyoon", "बढी": "badhi", "कम": "kam",
    "अधिकतम": "adhikatam", "न्यूनतम": "nyoonatam", "औसत": "ausat",
    "अनुपात": "anupaat", "दर": "dar", "प्रतिशत": "pratishat",
    "सही": "sahi", "गलत": "galat", "झुटो": "jhuto", "अलार्म": "alarm",
    "छुट्ने": "chhutne", "छुट्नु": "chhutnu", "पहिचान": "pahichan",
    "क्याप्सन": "caption", "सन्दर्भ": "sandarbha",
    "वास्तविक": "bastabik",
    "गरिएको": "garieko", "गरिएका": "garieka", "बनाइएको": "banaiyeko",
    "देखाइएको": "dekhaieko", "नापिएको": "napieko", "लेखिएको": "lekhieko",
    "सकिएको": "sakieko", "भनिएको": "bhanieko", "राखिएको": "rakhieko",
    "प्रयोग": "prayog", "प्रयोग गर्नुहोस्": "prayog garnuhos",
    "आवश्यक": "aawashyak", "अनिवार्य": "aniwarya", "वैकल्पिक": "baikalpik",
    "जानकारी": "jankari", "अर्थ": "arth", "कारण": "karan", "उद्देश्य": "uddeshya",
    "नियम": "niyam", "निर्णय": "nirnaya", "विधि": "bidhi", "चरण": "charan",
    "क्रम": "kram", "दिशा": "disha", "सीमा": "sima", "स्तम्भ": "stambha",
    "लाइन": "line", "तालिका": "talika", "सूची": "soochi", "सङ्केत": "sanket",
    "वातावरण": "batabaran",
    "कम्प्युटर": "computer", "प्रणाली": "pranali", "समस्या": "samasya",    "समाधान": "samadhan", "त्रुटि": "truti", "सन्देश": "sandesh",
    "सुरु": "suru", "अन्त्य": "antya", "अन्तिम": "antim",
    "तयार": "tayar", "तयारी": "tayari", "खुला": "khula", "बन्द": "banda",
    "सक्रिय": "sakriya", "निष्क्रिय": "nishkriya",
    "बदलिन्छ": "badlinchha", "बदल्नुहोस्": "badalnuhos",
    "फरक": "farak", "फरक छ": "farak chha", "उही": "uhi", "समान": "saman",
    "समान छ": "saman chha", "बराबर": "barabar", "हुनसक्छ": "hunasakchha",
    "सकिन्छ": "sakinchha", "पाइन्छ": "painchha",
    # 綴りの統一 / one spelling per idea
    "मात्र": "matra", "लागि": "lagi", "अभ्यास": "abhyas", "लेबल": "label",
    "फिचर": "feature", "अपडेट": "update", "व्याख्या": "byakhya",
    "महत्त्वपूर्ण": "mahattwapurna", "जाँच्ने": "jaanchne",
    "समयतालिका": "samayatalika", "सामग्री": "samagri", "बनाउने": "banaune",
    "ठाउँ": "thaun", "नयाँ": "nayan", "प्रमाणीकरण": "pramanikaran",
    "अनुवाद": "anuwad", "मूल्याङ्कन": "mulyankan", "पूरा": "pura",
    "संश्लेषित": "sansleshit", "योजनाबद्ध": "yojanabaddha",
    "अनुवादमा": "anuwad ma", "नेपालीमा": "Nepali ma",
    "मापन": "maapan", "मापनको": "maapanko", "तुलना": "tulna",
    "सिकाइ": "sikai", "सिकाइको": "sikaiko", "गणना": "ganana",
    "गणना गर्नुहोस्": "ganana garnuhos", "तय": "tay", "तय गर्नुहोस्": "tay garnuhos",
    "स्थिर": "sthir", "स्थिर गर्नुहोस्": "sthir garnuhos",
    "राख्नुहोस्": "rakhnuhos", "हेर्नुहोस्": "hernuhos",
    "लेख्नुहोस्": "lekhnuhos", "जाँच्नुहोस्": "jaanchnuhos",
    "सोच्नुहोस्": "sochnuhos", "चलाउनुहोस्": "chalaunuhos",
    "छान्नुहोस्": "chhannuhos", "बदल्नुहोस्": "badalnuhos",
    "मिलाउनुहोस्": "milaunuhos", "प्रयोग गर्नुहोस्": "prayog garnuhos",
    # 見出しと図・演習で使う語 / heading and exercise vocabulary
    "लर्निङ": "larning", "बनावट": "banabat", "रचना": "rachana",
    "सामान्यीकृत": "samanyikrit", "निर्देशाङ्क": "nirdeshangk",
    "भूमिका": "bhoomika", "चुहावट": "chuhabat", "एउटै": "eutai",
    "मध्यम": "madhyam", "खाली": "khali", "गन्ने": "ganne",
    "सम्पन्नता": "sampannata", "जाँचसूची": "janchasuchi",
    "दोहोरिने": "dohorine", "शब्दहरू": "shabdaharu", "एकै": "ekai",
    "चलाउने": "chalaune", "स्विच": "sbich", "सफल": "saphal",
    "मिल्छ": "milchha", "आफ्नै": "aphnai", "आँखाले": "ankhale",
    "असफलताका": "asaphalataka", "प्रकार": "prakar",
    "ओभरफिटिङ": "obharaphiting", "नहुन": "nahun", "अवस्था": "abastha",
    "रोजभन्दा": "rojabhanda", "भेट्ने": "bhetne", "प्याच": "pyach",
    "टुक्रा": "tukra", "नजिकको": "najikako", "छिमेकीसँगको": "chhimekisangako",
    "दूरी": "duri", "अहिलेको": "ahileko", "स्थानानुसार": "sthanaanusar",
    "मिलाउने": "milaune", "पुष्टि": "pushti", "कमजोरी": "kamajori",
    "पक्ष": "paksh", "हिस्सा": "hissa", "थप": "thap", "अध्ययन": "adhyayan",
    "निकाल्ने": "nikalne", "आधारमा": "adharama", "वितरण": "bitaran",
    "निरीक्षण": "nirikshan", "निरीक्षणमा": "nirikshan ma",
    # `-एर` 動詞連用形 / `-एर` converbs: the rule engine stops at the final `र` and yields
    # `banaer`. Nepali says `banaera`, so every converb of the course is glossed by hand.
    "बनाएर": "banaera", "चलाएर": "chalaera", "भएर": "bhaera", "मिलाएर": "milaera",
    "छुट्याएर": "chhutyaera", "छोएर": "chhoera", "लगाएर": "lagaera",
    "घुमाएर": "ghumaera", "लिएर": "liera", "घटाएर": "ghataera",
    "मेटाएर": "metaera", "बदलिएर": "badaliera", "हटाएर": "hataera",
    "ल्याएर": "lyaera", "गएर": "gaera", "भेट्टाएर": "bhettaera",
    "उल्ट्याएर": "ultyaera", "थिचिएर": "thichiera", "छुट्टाएर": "chhuttaera",
    "फर्काएर": "pharkaera", "साटिएर": "satiera", "पछ्याएर": "pachhyaera",
    "जोडिएर": "jodiera", "रोकिएर": "rokiera",
    # `र`/`न`/`ल` で終わる語 / words ending in a consonant cluster: the dropped final vowel
    # would leave `bhitr`, `gann`, `kshetr`, which nobody can read aloud.
    "भित्र": "bhitra", "क्षेत्र": "kshetra", "केन्द्र": "kendra", "सूत्र": "sutra",
    "गन्न": "ganna", "भन्न": "bhanna", "नाप्न": "napna", "निकाल्न": "nikalna",
    "भेट्न": "bhetna", "देख्न": "dekhna", "बढ्न": "badhna", "उकास्न": "ukasna",
    "छुट्न": "chhutna", "जोड्न": "jodna", "कर्ण": "karna", "विभिन्न": "bibhinna",
    "खोल्न": "kholna", "सम्हाल्न": "samhalna", "सँभाल्न": "sanbhalna",
    "सर्न": "sarna", "पुग्न": "pugna", "चल्न": "chalna", "पार्न": "parna",
    "समात्न": "samatna", "घट्न": "ghatna", "बुझ्न": "bujhna", "चिन्न": "chinna",
    "नगन्न": "naganna", "नबिगार्न": "nabigarna",
    "सम्पूर्ण": "sampurna", "पूर्ण": "purna", "अर्थपूर्ण": "arthapurna",
    "पूर्णाङ्क": "purnank", "सूक्ष्म": "sukshma", "शून्य": "shunya",
    "समग्र": "samagra", "नत्र": "natra", "चक्र": "chakra", "यन्त्र": "yantra",
    "संयन्त्र": "sanyantra", "स्वतन्त्र": "sbatantra", "विज्ञ": "bigya",
    "प्रमाणपत्र": "pramanapatra", "दृश्यक्षेत्र": "drishyakshetra",
    "गुरुत्वकेन्द्र": "gurutbakendra",
    # 複合語「〜भित्र」/ compounds in `-भित्र` keep the same spelling as the simple word
    "मानकभित्र": "manakbhitra", "दायराभित्र": "dayarabhitra",
    "मापदण्डभित्र": "mapadandbhitra", "तस्बिरभित्र": "tasbirbhitra",
    "मिनेटभित्र": "minetbhitra", "फोल्डरभित्र": "foldarbhitra",
    "गुणभित्र": "gunbhitra", "पङ्क्तिभित्र": "pangktibhitra",
    "कम्प्युटरभित्र": "kampyuterbhitra", "सीमाभित्र": "simabhitra",
    "सह्यताभित्र": "sahyatabhitra", "लूपभित्र": "lupbhitra",
}


def _map_signs(text: str) -> str:
    out = []
    for char in text:
        if char in DIGITS:
            out.append(str(DIGITS.index(char)))
        elif char == "।":
            out.append(".")
        elif char == "॥":
            out.append(".")
        elif char in SIGNS:
            out.append(SIGNS[char])
        elif char in ("\u200c", "\u200d"):
            continue
        else:
            out.append(char)
    return "".join(out)


def _trailing_punctuation(word: str) -> str:
    return word[len(word.rstrip("।॥.,;:!?()[]\"'")):]


def _suffix_split(stem: str) -> tuple[str, str] | None:
    """既知の語幹＋接尾辞に分ける / split a known stem plus a postposition."""
    for suffix, roman in SUFFIX_SPACED.items():
        if stem.endswith(suffix) and len(stem) > len(suffix):
            head = stem[: -len(suffix)]
            if head in GLOSSARY:
                return GLOSSARY[head], " " + roman
    for suffix, roman in SUFFIX_JOINED.items():
        if stem.endswith(suffix) and len(stem) > len(suffix):
            head = stem[: -len(suffix)]
            if head in GLOSSARY:
                return GLOSSARY[head], roman
    return None


def romanize_word(word: str) -> str:
    """Devanagari 1 語をラテン文字にする / one Devanagari word to Latin letters."""
    if word in GLOSSARY:
        return GLOSSARY[word]
    stripped = word.rstrip("।॥.,;:!?()[]\"'")
    trailing = word[len(stripped):].replace("।", ".").replace("॥", ".")
    if stripped in GLOSSARY:
        return GLOSSARY[stripped] + trailing
    split = _suffix_split(stripped)
    if split is not None:
        return split[0] + split[1] + trailing
    return _rule_romanize(stripped) + trailing


def _rule_romanize(stripped: str) -> str:
    """用語集を通さない変換規則そのもの / the letter rules, with no glossary lookup."""
    out: list[str] = []
    inherent = False
    index = 0
    length = len(stripped)
    while index < length:
        pair = stripped[index:index + 2]
        char = stripped[index]
        if pair in CONJUNCTS:
            if inherent:
                out.append("a")
            out.append(CONJUNCTS[pair])
            inherent = True
            index += 2
            continue
        if pair in INDEPENDENT_VOWELS:
            if inherent:
                out.append("a")
            out.append(INDEPENDENT_VOWELS[pair])
            inherent = False
            index += 2
            continue
        if char in INDEPENDENT_VOWELS:
            if inherent:
                out.append("a")
            out.append(INDEPENDENT_VOWELS[char])
            inherent = False
            index += 1
            continue
        if char in CONSONANTS:
            if inherent:
                out.append("a")
            out.append(CONSONANTS[char])
            inherent = True
            index += 1
            continue
        if char == VIRAMA:
            inherent = False
            index += 1
            continue
        if char in MATRAS:
            inherent = False
            out.append(MATRAS[char])
            index += 1
            continue
        if char in SIGNS:
            if inherent:
                out.append("a")
            inherent = False
            out.append(SIGNS[char])
            index += 1
            continue
        if char in DIGITS:
            if inherent:
                out.append("a")
            inherent = False
            out.append(str(DIGITS.index(char)))
            index += 1
            continue
        if inherent:
            out.append("a")
            inherent = False
        out.append(char)
        index += 1
    # 語末の固有母音 a は落とす（काम → kaam）。1 文字の語と「-छ」は残す（र → ra、गर्छ → garchha）。
    if inherent and (len(stripped) == 1 or stripped.endswith("छ")):
        out.append("a")
    text = "".join(out)
    if text.endswith("aa"):
        text = text[:-1]
    return text


# 綴り直しの安全弁 / guards for the respelling pass. Short rule outputs collide with code
# identifiers and English words (`ab`, `bat`, `man`), and `path` is a file-path token in the
# YOLO lessons, so neither is ever rewritten.
_RESPELLING_MIN_LENGTH = 4
_RESPELLING_SKIP = frozenset({"path", "data", "model", "test", "train", "range", "byte"})


def glossary_respellings() -> dict[str, str]:
    """規則の出力 → 用語集の綴り / rule-engine spelling -> reviewed glossary spelling.

    Used to bring an already Romanized catalog back in line after the glossary is extended;
    ``convert_nepali_to_latin.py`` applies it to Latin catalogs, where no Devanagari is left to
    transliterate. Only *unambiguous* rules are kept: when two glossary words collapse onto the
    same rule output (``हुन`` and ``हुन्`` both give ``hun``) the pair is different words, so
    rewriting one into the other would be wrong.
    """
    produced: dict[str, list[str]] = {}
    for devanagari in GLOSSARY:
        produced.setdefault(_rule_romanize(devanagari), []).append(devanagari)
    mapping = {}
    for rule, sources in produced.items():
        if len(sources) != 1 or not rule.isalpha():
            continue
        if len(rule) < _RESPELLING_MIN_LENGTH or rule in _RESPELLING_SKIP:
            continue
        reviewed = GLOSSARY[sources[0]]
        if reviewed != rule and reviewed.isalpha() and rule not in ENGLISH_MARKERS:
            mapping[rule] = reviewed
    return mapping


def apply_glossary_spellings(text: str) -> str:
    """ラテン文字だけのカタログに用語集の綴りを当てる / re-apply the glossary to Latin text."""
    mapping = glossary_respellings()
    if not mapping:
        return text
    pattern = re.compile(r"(?<![\w-])(%s)(?![\w-])"
                         % "|".join(sorted(map(re.escape, mapping), key=len, reverse=True)))
    return pattern.sub(lambda match: mapping[match.group(0)], text)


def romanize_text(text: str) -> str:
    """Devanagari runs だけを置き換える / replace Devanagari runs, nothing else."""
    return RUN_RE.sub(lambda match: _romanize_run(match.group(0)), text)


def _romanize_run(run: str) -> str:
    pieces = re.split(r"([\u0900-\u097f\u200c\u200d]+)", run)
    return "".join(romanize_word(piece) if DEVANAGARI_RE.search(piece) else piece
                   for piece in pieces if piece)


def leftover_devanagari(text: str) -> bool:
    return bool(DEVANAGARI_RE.search(text))


# Romanized Nepali and English share the alphabet, so a Latin block cannot be identified by its
# glyphs. The markers are the glossed Nepali forms themselves (so the two tables cannot drift apart)
# plus the function words that carry most sentences.
_ENGLISH_LOOKALIKES = {
    "model", "data", "score", "file", "folder", "setting", "cell", "kernel", "memory",
    "bank", "map", "feature", "update", "label", "input", "output", "heatmap", "computer",
    "threshold", "calibration", "dataset", "notebook", "caption", "number", "line",
    "partition", "nepali", "bank",
}

_FUNCTION_WORDS = {
    "chha", "chhan", "chhaina", "ho", "hoina", "hun", "hunchha", "hunchhan",
    "ra", "pani", "ma", "ko", "ka", "ki", "le", "lai", "baat", "sang",
    "yo", "tyo", "yas", "tyas", "yahan", "tyahan", "kun", "kati", "kasari",
    "kina", "ke", "tara", "tar", "ani", "feri", "aba", "pahile", "pachhi",
    "garnuhos", "hernuhos", "lekhnuhos", "jaanchnuhos", "chalaunuhos",
    "sochnuhos", "bhannuhos", "rakhnuhos", "chhannuhos", "badalnuhos",
    "garne", "hune", "garna", "huna", "bhaeko", "bhaeka", "bhayo", "garchha",
    "sakchha", "parchha", "lagchha", "dekhinchha", "garinchha", "hudaina",
    "hundaina", "mildaina", "sakindaina", "tasbir", "natija", "talim",
    "prashikshan", "parikshan", "samanya", "asamanya", "dosh", "sankhya",
    "maan", "matra", "sabai", "dherai", "thorai", "sakne", "naam", "jaanch",
    "abhilekh", "surakshit", "mulyankan", "udaharan", "prashna", "uttar",
    "abhyas", "sikai", "lakshya", "din", "bhaag", "charan", "kram", "kura",
    "tayari", "tulna", "bishay", "biwaran", "tah", "padhne", "jaanchne",
    # 見出しだけの短いブロックは語数が少ないので、見出しによく出る語も数える。
    # Short `after-heading` blocks hold a handful of words, so the vocabulary that headings use
    # most is listed here as well.
    "pahilo", "paila", "rakhne", "tarika", "khojne", "herne", "heraun", "gardai",
    "bandne", "badalne", "badalinda", "sanbhalne", "dohoryaun", "lagaunu",
    "chitrako", "bhaagko", "bhaneko", "bastabama", "bastubat", "prakriya",
    "ujyalo", "utpadan", "ramra", "seto", "mathi", "bayan", "talatir",
    "akshar", "anusar", "sart", "apabad", "abashyakata", "mapadand", "ayat",
    "baks", "baunding", "kantur", "kinara", "lup", "naper", "napne", "sarer",
    "sanyog", "pratichchhed", "pichchhe", "pharkieko", "phankshan", "dip",
    "mesin", "mesinalai", "sbachalan", "nirdeshank", "mulabindu", "chitrabindu",
    "notabukabhitrabat", "talikako", "pikselalai", "milimitarama", "bikas",
    "aichchhik", "bishbas", "lekher", "samma", "chal", "sikai", "kram",
}

NEPALI_MARKERS = (
    {value.lower() for value in GLOSSARY.values()
     if re.fullmatch(r"[a-z]+", value.lower())} - _ENGLISH_LOOKALIKES
) | _FUNCTION_WORDS

ENGLISH_MARKERS = frozenset({
    "the", "is", "are", "and", "of", "to", "you", "your", "this", "that", "these",
    "those", "with", "for", "from", "on", "in", "into", "it", "its", "not", "by",
    "as", "be", "we", "can", "will", "when", "then", "than", "only", "same", "use",
    "used", "using", "which", "what", "how", "why", "where", "there", "here", "has",
    "have", "does", "do", "did", "should", "must", "may", "more", "less", "all",
    "any", "some", "each", "one", "two", "three", "first", "second", "next", "also",
    "but", "if", "so", "because", "before", "after", "about", "between", "under",
    "over", "no", "yes", "please", "check", "run", "read", "write", "show", "value",
    "values", "image", "images", "but", "same", "not",
})


def looks_like_nepali_latin(text: str, minimum: int = 2) -> bool:
    """ラテン文字のネパール語らしさを語彙で確かめる / positive check, never glyph guessing.

    A block qualifies when its words include Nepali markers and are not dominated by English
    function words. This lets ``din 4 notebook 01: dataset ra label`` and a paragraph that quotes
    many Latin technical tokens pass, while a copied English paragraph fails.
    """
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    words = re.findall(r"[A-Za-z]+", text.lower())
    if not words:
        return False
    nepali = {word for word in words if word in NEPALI_MARKERS}
    english = {word for word in words if word in ENGLISH_MARKERS}
    if not nepali:
        return False
    if len(english) >= 2 and len(english) >= len(nepali):
        return False
    return len(nepali) >= minimum or len(nepali) / len(words) >= 0.2


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Romanize Nepali text.")
    parser.add_argument("text", nargs="*", help="text to romanize (default: read stdin)")
    args = parser.parse_args(argv)
    if args.text:
        print(romanize_text(" ".join(args.text)))
        return 0
    print(romanize_text(sys.stdin.read()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
