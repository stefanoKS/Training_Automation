<!--
नेपाली अनुवाद / Nepali translation source for
docs/pdf/README.md
-->
# docs/pdf/README — नेपाली अनुवाद

<!-- ne-doc: docs/pdf/README.md -->

<!-- ne-section: Explanation companions -->
### नेपालीमा

यो फोल्डरका PDF **नोटबुककै Markdown बाट स्वतः बनाइएका** पुस्तिका हुन्।
छुट्टै लेखिएको पाण्डुलिपि होइन, त्यसैले नोटबुक सुधारेर तलको आदेश फेरि चलाउँदा दुवै मिल्छ।

दुई किसिमका पुस्तिका छन्।

| किसिम | भाषा | बनाउने स्क्रिप्ट |
|---|---|---|
| `*_ja_en.pdf` | जापानी → अङ्ग्रेजी | `assets\scripts\export_explanations_pdf.py` |
| `*_ja_en_ne.pdf` | जापानी → अङ्ग्रेजी → नेपाली | `assets\scripts\export_trilingual_pdf.py` |

अघिल्ला `*_ja_en.pdf` फाइल **जस्ताको तस्तै** राखिएका छन्; नयाँ त्रिभाषी संस्करणले तिनलाई
प्रतिस्थापन गर्दैन।

<!-- ne-section: ## ファイル / Files -->
### नेपालीमा

| फाइल | सामग्री |
|---|---|
| `Day01_explanation_ja_en_ne.pdf` … `Day05_explanation_ja_en_ne.pdf` | प्रत्येक दिनका ३ नोटबुक (दिन ५ मा ३) |
| `Week1_explanation_ja_en_ne.pdf` | ५ दिनकै सामग्री एउटै पुस्तिकामा |
| `Setup_ja_en_ne.pdf` | तयारी नोटबुक `00_Environment_Setup.ipynb` |
| `Installation_Guide_ja_en_ne.pdf` | `START_HERE.md` र `docs/troubleshooting/installation.md` |
| `Repository_Guide_ja_en_ne.pdf` | `README.md` र `requirements/tested_versions.md` |
| `Course_Syllabus_ja_en_ne.pdf` | `COURSE_SYLLABUS.md` |

पाना सङ्ख्या हरेक पटक बनाउँदा स्क्रिप्टले आफैं देखाउँछ।

<!-- ne-section: ## 作り直す方法 / Regenerating -->
### नेपालीमा

installation (सिकाइको वातावरणभन्दा छुट्टै):

```cmd
python -m pip install -r requirements\pdf.txt
python -m playwright install chromium
```

`playwright install chromium` ले PDF छाप्ने Chromium खोज्छ। यो **PDF बनाउने र जाँच्ने मानिसका लागि
मात्र** हो; प्रशिक्षार्थीले यो चाहिँदैन।

जापानी–अङ्ग्रेजी पुस्तिका:

```cmd
python assets\scripts\export_explanations_pdf.py
```

त्रिभाषी पुस्तिका (**यो एक आदेशले सबै**) :

```cmd
python assets\scripts\export_trilingual_pdf.py
```

एउटा मात्र बनाउन:

```cmd
python assets\scripts\export_trilingual_pdf.py --only Day03
```

जाँच (हरेक पाना चित्र बनाएर, नेपाली खोजिने अवस्थामा छ कि छैन पनि जाँच्दै):

```cmd
python assets\scripts\inspect_pdf_pages.py --languages ja,ne
```

* model download, सिकाइ र नोटबुक **चलाइँदैन**। exporter ले Markdown, चित्र र छोटा कोड सेल मात्र
  पढ्छ।
* जापानी फन्ट OS को (Windows मा Noto Sans JP / Yu Gothic / Meiryo), नेपाली फन्ट Nirmala UI
  PDF मा embed हुन्छ।
* चित्रको स्रोत प्रत्येक PDF को अन्तिम पाना "स्रोत र सन्दर्भ" मा छ।

<!-- ne-section: ## 何が入り、何が入らないか / What is in, and what is out -->
### नेपालीमा

पर्छ:

* सिकाइ लक्ष्य, पूर्वशर्त र व्याख्या (जापानी → अङ्ग्रेजी → नेपाली)
* चलाउनुअघि नै देखिने स्थिर चित्र, captions, "ध्यान दिनुपर्ने कुरा", प्रश्नहरू
* प्रशिक्षार्थीले बदल्ने छोटा कोड उदाहरण (20 लाइनसम्म)
* अभ्यास, सङ्केत, बुझाइ जाँच
* सन्दर्भ नतिजा (यो तालिममा सुरक्षित भएका नतिजाबाट बनेका चित्र)। योजनाबद्ध र कृत्रिम डेटाको फरक
  चित्रभित्रै लेखिएको छ।

पर्दैन:

* सेलको output, stack trace, लामो तयारी कोड, काँचो JSON
* प्रशिक्षकका जवाफ (`docs/instructor/` मा छुट्टै)
* slider आफैं; त्यसको सट्टा स्थिर चित्र र "नोटबुकमा चलाउनुहोस्" भन्ने टिप्पणी
* नचलाइएको सिकाइ वा जाँचको नतिजा

<!-- ne-section: ## 既知の限界 / Known limitations -->
### नेपालीमा

* फराकिलो चित्र पढ्न सजिलो होस् भनेर **A4 तेर्सो पाना** मा राखिएको छ; अघिल्लो-पछिल्लो पानामा खाली
  ठाउँ देखिन्छ।
* PDF भित्रका लिङ्क plain text हुन् (क्लिक गर्दा खुल्दैन)।
* चित्रभित्रको अक्षर चित्रकै भाग हो, त्यसैले खोज्न वा छान्न मिल्दैन।
* नेपाली अक्षर खोज्न मिल्नका लागि नेपाली मज्जन 1.5 pt को गुणनमा राखिएको छ (9, 10.5, 12, 13.5 pt)।
  Chromium ले अन्य आकारमा शब्दको बीचमा खाली ठाउँ हालेर लेख्छ, जसले खोज बिगार्छ।
