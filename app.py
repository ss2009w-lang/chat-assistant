from flask import Flask, render_template, request, jsonify, session, redirect
import json, re, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('FIRAS_SECRET','firas-secret')

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD','1234')
SUPPORT_TEXT = 'لم أجد المعلومة المطلوبة. يرجى التواصل مع دعم المتدربين عبر البريد psmmc@psmmc.med.sa أو التحويلة 43880.'

DATA_FILE = 'info.json'
FORWARDED_LOG = 'forwarded.log'

CATEGORY_HINTS = {
    'دوام': ['دوام','ساعات','وقت','يبدأ','ينتهي'],
    'تواصل': ['اتصال','هاتف','بريد','ايميل','تحويلة'],
    'مواقع': ['اين','موقع','مبنى','قسم','دور']
}

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE,'w',encoding='utf-8') as f:
        json.dump([],f,ensure_ascii=False)

with open(DATA_FILE,encoding='utf-8-sig') as f:
    INFOS = json.load(f)

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = []
    for w in text.split():
        if w.startswith('ال') and len(w) > 2:
            w = w[2:]
        words.append(w)
    return words

def detect_category(words):
    for cat, keys in CATEGORY_HINTS.items():
        if any(k in words for k in keys):
            return cat
    return None

def score(q_words, info_text):
    return len(set(q_words) & set(normalize(info_text)))

def log_forwarded(q):
    with open(FORWARDED_LOG,'a',encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()} | {q}\n")

def search_infos(q_words, infos):
    best = None
    best_score = 0
    for info in infos:
        s = score(q_words, info['text'])
        if s > best_score:
            best_score = s
            best = info
    return best, best_score

def find_answer(question):
    q_words = normalize(question)
    cat = detect_category(q_words)

    if cat:
        subset = [i for i in INFOS if i['category'] == cat]
        best, sc = search_infos(q_words, subset)
        if sc > 0:
            return best['text']

    best, sc = search_infos(q_words, INFOS)
    if sc > 0:
        return best['text']

    log_forwarded(question)
    return SUPPORT_TEXT

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    return jsonify({'reply': find_answer(request.json.get('message',''))})

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        if request.json.get('pw') == ADMIN_PASSWORD:
            session['admin'] = True
            return jsonify({'ok': True})
        return jsonify({'ok': False})
    return render_template('admin_login.html')

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/admin/login')
    return render_template('admin.html')

@app.route('/admin/data')
def admin_data():
    if not session.get('admin'):
        return jsonify({'error': True})
    forwarded=[]
    try:
        with open(FORWARDED_LOG,encoding='utf-8') as f:
            forwarded=list(dict.fromkeys([l.strip() for l in f if l.strip()]))
    except: pass
    return jsonify({'infos': INFOS,'forwarded':forwarded})

@app.route('/admin/add_info', methods=['POST'])
def add_info():
    if not session.get('admin'):
        return jsonify({'error': True})
    text=request.json.get('text')
    category=request.json.get('category')
    if text and category:
        INFOS.append({'text':text,'category':category})
        with open(DATA_FILE,'w',encoding='utf-8') as f:
            json.dump(INFOS,f,ensure_ascii=False,indent=2)
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
