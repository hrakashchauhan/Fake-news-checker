# Fake News Checker

> An LLM-powered fake news detector that performs cognitive forensic analysis on news articles using Google Gemini.

Instead of a traditional supervised classifier, this project uses a carefully engineered "Cognitive Forensic Analyst" prompt to make a large language model (Google Gemini) reason about whether a piece of text is **Real** or **Fake**. The model examines psychological tone, logical structure, evidence quality, and source provenance, then returns a structured JSON verdict with a confidence score and a breakdown of its reasoning.

The repository also includes the tooling used to build a balanced evaluation set from public datasets (Kaggle Fake/Real News and the LIAR benchmark) and to measure the detector's accuracy against that set.

## How it works

The detector prompts the LLM to run a four-step forensic analysis as an internal chain of thought before producing its verdict:

1. **Psychological tone & intent** — detects emotionally charged, loaded, or sensationalized language and likely manipulative intent.
2. **Logical structure & fallacy detection** — checks argument soundness and flags fallacies (ad hominem, strawman, false dilemma, oversimplification, etc.).
3. **Assertion & evidence scrutiny** — treats each factual claim as unverified and assesses whether credible, verifiable sources back it.
4. **Provenance & source context** — looks for textual clues about the source's nature and synthesizes a final hypothesis.

The model returns only a raw JSON object, for example:

```json
{
  "verdict": "Fake",
  "confidence_score": 88,
  "reason": "Relies on an anonymous 'consortium' with no verifiable sources for an extraordinary claim.",
  "analysis_summary": {
    "psychological_intent": "Designed to evoke fear and urgency.",
    "logical_fallacies": ["Appeal to anonymous authority"],
    "evidence_quality": "Non-existent"
  }
}
```

## Features

- **Zero-shot LLM detection** — no model training required; uses `gemini-1.5-pro-latest` via the Google Generative AI SDK.
- **Structured forensic output** — verdict, confidence score, reasoning summary, detected logical fallacies, and an evidence-quality rating.
- **Robust JSON handling** — cleans markdown fencing from responses and handles empty input, parsing errors, and API errors gracefully.
- **Batch evaluation** — `evaluate.py` runs a full test set, computes accuracy, and writes a detailed per-article results CSV with the model's reasoning.
- **Dataset preparation** — `prepare_data.py` samples and balances articles from the Kaggle Fake/Real News datasets and the LIAR benchmark into a single labeled test set.
- **Challenger augmentation** — `add_challengers.py` appends a set of hand-written, plausible-but-fabricated articles to stress-test the detector.

## Tech stack

- **Python 3**
- **[google-generativeai](https://pypi.org/project/google-generativeai/)** — Google Gemini API client
- **[pandas](https://pandas.pydata.org/)** — dataset loading, sampling, and results export
- **Datasets:** Kaggle Fake/Real News (`Fake.csv`, `True.csv`) and the [LIAR benchmark](https://www.cs.ucsb.edu/~william/data/liar_dataset.zip) (`train1.csv`, `test1.csv`, `valid1.csv`)

## Getting started

### Prerequisites

- Python 3.9+
- A Google Gemini API key ([Google AI Studio](https://aistudio.google.com/))

### Install

```bash
git clone https://github.com/hrakashchauhan/Fake-news-checker.git
cd Fake-news-checker

pip install google-generativeai pandas
```

### Configure your API key

The detector reads the API key from the `GOOGLE_API_KEY` environment variable.

```bash
# macOS / Linux
export GOOGLE_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:GOOGLE_API_KEY="your-api-key-here"
```

### Run a single analysis

`detector.py` includes a built-in test article you can run directly:

```bash
python detector.py
```

Or import `analyze_article` in your own code:

```python
from detector import analyze_article

result = analyze_article("Your news article text here...")
print(result)
```

### Build the evaluation set (optional)

This requires the source CSVs (`True.csv`, `Fake.csv`, `test1.csv`) to be present in the project directory.

```bash
python prepare_data.py        # creates test_data.csv (balanced real/fake samples)
python add_challengers.py     # appends 10 fabricated "challenger" articles
```

### Evaluate accuracy

```bash
python evaluate.py
```

This reads `test_data.csv`, runs every article through the detector (with a short delay between calls to respect API rate limits), prints overall accuracy, and saves a detailed forensic breakdown to `evaluation_results_V3.csv`.

## Project structure

```
Fake-news-checker/
├── detector.py          # Core: Gemini-powered forensic analysis + analyze_article()
├── evaluate.py          # Runs the detector over test_data.csv, reports accuracy
├── prepare_data.py      # Builds a balanced test_data.csv from Kaggle + LIAR data
├── add_challengers.py   # Appends fabricated challenger articles to test_data.csv
├── README               # LIAR dataset documentation (original benchmark notes)
├── True.csv / Fake.csv  # Kaggle real/fake news datasets (input)
├── train1.csv / test1.csv / valid1.csv  # LIAR benchmark splits (input)
├── test_data.csv        # Generated balanced evaluation set
└── evaluation_results*.csv  # Generated evaluation output
```

## Notes & limitations

- **Verdicts depend on the LLM.** Output quality and accuracy are tied to the Gemini model and prompt; results are not deterministic and may vary between runs.
- **API costs and rate limits apply.** Each article is a separate Gemini API call; `evaluate.py` sleeps ~1.1s between calls to stay within rate limits, so large evaluations take time.
- **Text-only analysis.** The detector reasons solely from the supplied text — it does not fetch external sources or perform live fact-checking.
- **Datasets are large.** The Kaggle and LIAR CSVs are sizable; they are inputs to the pipeline and are not required to run a single `analyze_article` call.

## Author

**Akash Kumar** ([@hrakashchauhan](https://github.com/hrakashchauhan))
