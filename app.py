from flask import Flask, render_template, request, jsonify, session
import json, re

app = Flask(__name__)
app.secret_key = 'firas-secret'

DATA_FILE = 'info.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE,'w',encoding='utf-8') as f:
        json.dump([],f,ensure_ascii=False)

with open(DATA_FILE,'r',encoding='utf-8-sig') as f:
    INFOS = json.load(f)

def normalize(t):
    t = t.lower()
    t = re.sub(r'[^\w\s]','',t)
    return t.split()

def similarity(q, text):
    return len(set(normalize(q)) & set(normalize(text)))

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/login', methods=['POST'])
def login():
    session['user'] = request.json
    return jsonify({'ok': True})

@app.route('/ask', methods=['POST'])
def ask():
    if 'user' not in session:
        return jsonify({'reply':'يرجى تسجيل الدخول أولاً'})
    q = request.json.get('message','')
    best = None
    score = 0
    for i in INFOS:
        s = similarity(q, i['text'])
        if s > score:
            score = s
            best = i['text']
    if not best:
        best = 'لا توجد معلومة مطابقة، يمكنك رفع بلاغ.'
    return jsonify({'reply': best})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
