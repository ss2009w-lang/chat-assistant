from flask import Flask, render_template, request, jsonify
import json
import re
from datetime import datetime

app = Flask(__name__)

with open('knowledge.json', encoding='utf-8-sig') as f:
    KB = json.load(f)

LOG_FILE = 'unanswered.log'
SUGGEST_LIMIT = 3
MIN_SUGGEST_SCORE = 1

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def score(question, user_words):
    q_words = set(normalize(question).split())
    return len(q_words & user_words)

def log_unanswered(question):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()} | {question}\n")

def find_answer_with_suggestions(user_input):
    user_words = set(normalize(user_input).split())
    scored = []

    for item in KB:
        s = score(item['question'], user_words)
        scored.append((s, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    best_score, best_item = scored[0]

    if best_score == 0:
        log_unanswered(user_input)
        return {
            'answer': 'عذرًا، لا تتوفر لدي معلومات حول هذا السؤال حاليًا.',
            'suggestions': []
        }

    if best_score < MIN_SUGGEST_SCORE:
        suggestions = [
            i['question']
            for s, i in scored[:SUGGEST_LIMIT]
            if s >= MIN_SUGGEST_SCORE
        ]
        return {
            'answer': 'هل تقصد أحد هذه الأسئلة؟',
            'suggestions': suggestions
        }

    return {
        'answer': best_item['answer'],
        'suggestions': []
    }

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('message', '')
    result = find_answer_with_suggestions(question)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
