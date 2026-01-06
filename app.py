from flask import Flask, render_template, request, jsonify, session, redirect, send_file
import json, re, os, sqlite3
from datetime import datetime
from time import time
from collections import defaultdict
import pandas as pd

app = Flask(__name__)
app.secret_key = os.environ.get('FIRAS_SECRET','firas-secret')

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD','1234')
SUPPORT_TEXT = 'لم أجد المعلومة المطلوبة. يرجى التواصل مع دعم المتدربين عبر البريد psmmc@psmmc.med.sa أو التحويلة 43880.'

DATA_FILE = 'info.json'
DB_FILE = 'unanswered.db'

CATEGORY_HINTS = {
    'دوام': ['دوام','ساعات','وقت','يبدأ','ينتهي'],
    'تواصل': ['اتصال','هاتف','بريد','ايميل','تحويلة'],
    'مواقع': ['اين','موقع','مبنى','قسم','دور']
}

RATE_LIMIT = 5
WINDOW = 60
requests_log = defaultdict(list)

def db():
    return sqlite3.connect(DB_FILE)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE,'w',encoding='utf-8') as f:
        json.dump([],f,ensure_ascii=False)

with open(DATA_FILE,encoding='utf-8-sig') as f:
    INFOS = json.load(f)

def log_unanswered(q):
    conn = db()
    c = conn.cursor()
    c.execute(
        'INSERT INTO unanswered (question, created_at) VALUES (?,?)',
        (q, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def allowed(ip):
    now = time()
    requests_log[ip] = [t for t in requests_log[ip] if now - t < WINDOW]
    if len(requests_log[ip]) >= RATE_LIMIT:
        return False
    requests_log[ip].append(now)
    return True

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words=[]
    for w in text.split():
        if w.startswith('ال') and len(w)>2:
            w=w[2:]
        words.append(w)
    return words

def detect_category(words):
    for c,k in CATEGORY_HINTS.items():
        if any(x in words for x in k):
            return c
    return None

def score(q, t):
    return len(set(q)&set(normalize(t)))

def find_answer(q):
    words=normalize(q)
    cat=detect_category(words)
    candidates=INFOS
    if cat:
        candidates=[i for i in INFOS if i['category']==cat]
    best=None
    best_s=0
    for i in candidates:
        s=score(words,i['text'])
        if s>best_s:
            best_s=s
            best=i
    if best_s>0:
        return best['text']
    log_unanswered(q)
    return SUPPORT_TEXT

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/ask',methods=['POST'])
def ask():
    ip=request.remote_addr
    if not allowed(ip):
        return jsonify({'reply':'يرجى الانتظار قبل إرسال المزيد من الأسئلة'})
    return jsonify({'reply':find_answer(request.json.get('message',''))})

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/admin/login')
    return render_template('admin.html')

@app.route('/admin/login',methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        if request.json.get('pw')==ADMIN_PASSWORD:
            session['admin']=True
            return jsonify({'ok':True})
        return jsonify({'ok':False})
    return render_template('admin_login.html')

@app.route('/admin/export/unanswered')
def export_unanswered():
    if not session.get('admin'):
        return redirect('/admin/login')

    conn = db()
    df = pd.read_sql_query('SELECT * FROM unanswered', conn)
    conn.close()

    file = 'unanswered_questions.xlsx'
    df.to_excel(file, index=False)

    return send_file(file, as_attachment=True)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
