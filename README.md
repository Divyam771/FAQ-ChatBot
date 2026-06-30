# CodeAlpha_FAQChatbot

A retrieval-based **FAQ Chatbot** built for the CodeAlpha AI Internship (Task 2).

## 🧠 How it works

1. **FAQ Data** — A set of question/answer pairs is stored in `faqs.json`.
2. **Preprocessing (NLTK)** — User input and FAQ questions are lowercased, tokenized,
   stripped of stopwords, and lemmatized.
3. **Vectorization** — All FAQ questions are converted into TF-IDF vectors using scikit-learn.
4. **Matching** — A user's query is vectorized the same way, then compared against every
   FAQ question using **cosine similarity**.
5. **Response** — The answer belonging to the highest-scoring FAQ is returned, as long as it
   passes a minimum similarity threshold. Otherwise, a fallback message is shown.

## 📂 Project Structure

```
CodeAlpha_FAQChatbot/
├── app.py                # Flask server (routes + API)
├── chatbot_engine.py      # Core NLP + similarity matching logic
├── faqs.json              # FAQ dataset (questions & answers)
├── requirements.txt
├── templates/
│   └── index.html         # Chat UI page
└── static/
    ├── style.css           # Chat UI styling
    └── script.js            # Chat UI behavior (AJAX calls)
```

## 🚀 Running locally

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000` in your browser.

You can also test the chatbot directly in the terminal:

```bash
python chatbot_engine.py
```

## ✏️ Customizing the FAQs

Edit `faqs.json` and add new objects in the form:

```json
{
  "question": "Your question here?",
  "answer": "Your answer here."
}
```

No retraining step is needed — the TF-IDF vectorizer rebuilds automatically each time the
app starts.

## 🛠️ Tech Stack

- Python
- Flask (web server)
- NLTK (text preprocessing: tokenization, stopwords, lemmatization)
- scikit-learn (TF-IDF vectorization + cosine similarity)
- HTML / CSS / JavaScript (chat UI)

## 📌 Notes

- Similarity threshold is set to `0.25` in `app.py` — lower it to make the bot more lenient,
  raise it to make it stricter about matches.
- Built as part of the **CodeAlpha Artificial Intelligence Internship** — Task 2: Chatbot for FAQs.
