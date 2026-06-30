"""
chatbot_engine.py
-----------------
Core engine for the FAQ Chatbot.

Pipeline:
1. Load FAQ data (question -> answer pairs).
2. Preprocess text using NLTK (lowercasing, tokenization, stopword removal, lemmatization).
3. Vectorize all FAQ questions using TF-IDF.
4. For a new user query, preprocess + vectorize it the same way,
   then compute cosine similarity against all FAQ questions.
5. Return the answer of the best-matching FAQ if similarity is above a threshold,
   otherwise return a fallback "I don't understand" message.
"""

import json
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------------------------
# One-time NLTK resource download (safe to call repeatedly; skips if present)
# ---------------------------------------------------------------------------
def _ensure_nltk_resources():
    resources = {
        "tokenizers/punkt": "punkt",
        "tokenizers/punkt_tab": "punkt_tab",
        "corpora/stopwords": "stopwords",
        "corpora/wordnet": "wordnet",
        "corpora/omw-1.4": "omw-1.4",
    }
    for path, name in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name, quiet=True)


_ensure_nltk_resources()

_lemmatizer = WordNetLemmatizer()
try:
    _stop_words = set(stopwords.words("english"))
except LookupError:
    _stop_words = set()


def preprocess(text: str) -> str:
    """Clean, tokenize, remove stopwords, and lemmatize input text."""
    text = text.lower().strip()
    try:
        tokens = word_tokenize(text)
    except LookupError:
        tokens = text.split()

    cleaned_tokens = [
        _lemmatizer.lemmatize(tok)
        for tok in tokens
        if tok.isalnum() and tok not in _stop_words
    ]
    return " ".join(cleaned_tokens)


class FAQChatbot:
    """A simple retrieval-based FAQ chatbot using TF-IDF + cosine similarity."""

    def __init__(self, faq_path: str, similarity_threshold: float = 0.25):
        self.faq_path = faq_path
        self.similarity_threshold = similarity_threshold
        self.faqs = self._load_faqs(faq_path)

        self.questions = [item["question"] for item in self.faqs]
        self.answers = [item["answer"] for item in self.faqs]
        self.processed_questions = [preprocess(q) for q in self.questions]

        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.processed_questions)

    @staticmethod
    def _load_faqs(path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"FAQ data file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_response(self, user_query: str):
        """
        Return a dict with the matched answer, matched question,
        and the similarity score for transparency/debugging.
        """
        if not user_query or not user_query.strip():
            return {
                "answer": "Please type a question so I can help you.",
                "matched_question": None,
                "score": 0.0,
            }

        processed_query = preprocess(user_query)
        if not processed_query:
            return {
                "answer": "Sorry, I didn't understand that. Could you rephrase your question?",
                "matched_question": None,
                "score": 0.0,
            }

        query_vector = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.question_vectors).flatten()

        best_idx = similarities.argmax()
        best_score = float(similarities[best_idx])

        if best_score < self.similarity_threshold:
            return {
                "answer": (
                    "Sorry, I don't have an answer for that. "
                    "Try asking about the internship, tasks, certificates, or submission process."
                ),
                "matched_question": None,
                "score": best_score,
            }

        return {
            "answer": self.answers[best_idx],
            "matched_question": self.questions[best_idx],
            "score": best_score,
        }

    def all_questions(self):
        """Useful for displaying suggested questions in the UI."""
        return self.questions


if __name__ == "__main__":
    # Quick CLI test mode
    bot = FAQChatbot(os.path.join(os.path.dirname(__file__), "faqs.json"))
    print("FAQ Chatbot (CLI mode) — type 'exit' to quit\n")
    while True:
        query = input("You: ")
        if query.lower() in ("exit", "quit"):
            break
        result = bot.get_response(query)
        print(f"Bot: {result['answer']}  (score: {result['score']:.2f})\n")
