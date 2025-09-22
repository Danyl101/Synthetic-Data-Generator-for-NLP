# 📝 Semi-Synthetic Data Generator for NLP

This project is a **semi-synthetic dataset generator for NLP tasks**, designed to scrape  news, extract article content, paraphrase it using state-of-the-art models, and filter the results for quality.

It was built as a modular pipeline combining **web scraping, article extraction, paraphrasing, semantic filtering, and API/React integration**, to create robust and diverse datasets for downstream machine learning models like **SBERT**.

---

## 🚀 Features

* **Scraper Module**

  * Scrapes financial/economic news sites using **Selenium**.
  * Handles static and dynamic pages.
  * Supports blacklist filtering, error handling, and modular configs via JSON.

* **Extractor Module**

  * Extracts full article content using **newspaper3k**, Selenium, and Playwright fallback.
  * Cleans malformed HTML and JS-heavy sites.
  * Stores articles as clean `.txt` files.

* **Paraphraser Module**

  * Uses **Pegasus** for high-quality paraphrasing.
  * Handles hierarchical file structures with robust dictionary-based storage.
  * Outputs paraphrased versions of extracted text files.

* **SBERT Semantic Filter**

  * Compares paraphrased text with originals using **Sentence-BERT**.
  * Removes files with too high (>0.9) or too low (<0.3) similarity.
  * Applies heuristics to handle chunking/empty embeddings.

* **API Module**

  * Built with **Flask (Python)** and **TypeScript**.
  * Provides endpoints for:
    * Managing filters and site lists
    * Running scraper & extractor
    * Running Paraphrasing and semantic filter
  * Async operations with logging for reliability.

* **Frontend**

  * Built with **React + Vite + Tailwind + Shadcn**.
  * Provides simple UI for interacting with APIs.
  * Clean minimal design suitable for demos.

---

## 🛠️ Tech Stack

* **Backend**: Python (Flask, Selenium, Playwright, Newspaper3k, Pegasus, SBERT, PyTorch)
* **Frontend**: React (Vite, TailwindCSS, Shadcn UI)
* **ML Models**: Pegasus (Paraphrasing), SBERT (Semantic Similarity), LSTM/TCN/BiLSTM (Forecasting)
* **Infrastructure**: JSON-config driven, modular architecture

---

## 📂 Project Structure

```
.
├── scraper/               # Web scraping modules
│   ├── link_extract.py
│   ├── robot.py
│   ├── utils.py
│   └── scrape_run.py
│
├── extractor/             # Article extraction modules
│   ├── selenium_newspaper.py
│   ├── playwright_extract.py
│   ├── content_extract.py
│   └── extract_run.py            
│
├── frontend/              # React + Vite frontend
│    └──src/
|        ├──API/           # Flask APIs
|        └──UI/
|
├── Datasets/              # Scraped & processed datasets
|    ├──BERT_Data/
|    |    └── Raw_Text_Data/
|    |          ├── Raw_Data
|    |          ├── Cleaned_Data
|    |          └── Paraphrased_Data
|    |
|    └──Scraping_Data/
|         ├── Scraped_articles.json
|         └──Site_filters.json
|
└──BERT_Preprocess/
      ├── Clean_Run.py
      ├── Paraphraser.py     #Paraphraser
      ├── Bert_Semantic.py   #SBERT Comparison
      └── Preprocess_run.py
```

---

## ⚙️ Installation

Clone the repo:

```bash
git clone https://github.com/Danyl101/Synthetic-Data-Generator-for-NLP.git
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd frontend
npm install
```

---

## ▶️ Usage

1. **Start Flask API**

   ```bash
   $env:PYTHONPATH = (Get-Location).Path
   python -m frontend.src.api.flask_api.flask_run
   ```

2. **Run Frontend**

   ```bash
   cd frontend
   npm run dev
   ```

---

## 🔁 Iterative Development

This system evolved through multiple iterations:

* **Scraper**: Static → Selenium → Full dynamic scraping with error handling.
* **Extractor**: Newspaper3k → XPath fixes → Playwright fallback.
* **Paraphrase**: Backtranslation → Pegasus with chunk handling.
* **SBERT**: Per-chunk scores → Averaged per-file → Heuristic cleanup.
* **API**: Simple JSON endpoints → Modular Flask services → ML inference integration.
* **React**: Barebones → Functional → Presentable with Tailwind + Shadcn.

---

## 📌 Future Improvements

* Add caching for scraper/extractor.
* Parallelize Playwright for speed.
* More paraphrasing diversity (mix Pegasus + LLM).
* Add dataset export formats (CSV, JSONL, HuggingFace Datasets).
* Containerize with Docker for deployment.

---

## 📜 License

MIT License. See `LICENSE` for details.

---

Would you like me to make this **research-style (academic tone, like a paper)** or **developer-style (GitHub OSS tone, more practical and concise)**?
