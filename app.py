from flask import Flask, render_template, request, jsonify
import json
import re

app = Flask(__name__)

with open('knowledge.json', encoding='utf-8-sig') as f:
    KB = json.load(f)

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def score(question, user_words):
    q_words = set(normalize(question).split())
    return len(q_words & user_words)

def find_answer(user_input):
    user_words = set(normalize(user_input).split())
    best_score = 0
    best_answer = None

    for item in KB:
        s = score(item['question'], user_words)
        if s > best_score:
            best_score = s
            best_answer = item['answer']

    if best_score == 0:
        return 'لا أملك إجابة مناسبة ضمن المعلومات المتاحة.'
    return best_answer

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('message', '')
    answer = find_answer(question)
    return jsonify({'reply': answer})

if __name__ == '__main__':
    app.run()
