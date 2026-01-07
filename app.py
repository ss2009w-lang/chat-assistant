from flask import Flask, request, jsonify, render_template, redirect, send_file
import json, re, os, sqlite3
from datetime import datetime
from time import time
from collections import defaultdict
import pandas as pd

app = Flask(__name__)
app.secret_key = os.environ.get('FIRAS_SECRET','firas-secret')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD','1234')
SUPPORT_TEXT = 'لم أجد المعلومة المطلوبة. يرجى التواصل مع دعم المتدربين عبر البريد psmmc@psmmc.med.sa أو التحويلة 43880.'

DATA_FILE = 'info.json'
DB_FILE = 'unanswered.db'

SYNONYMS = {
    'دوام': ['دوام','ساعات','عمل','وقت'],
    'موقع': ['اين','أين','موقع','مبنى','مكان'],
    'تواصل': ['اتصال','هاتف','تواصل','رقم','ايميل','بريد','تحويلة']
}

STOP_WORDS = ['متى','هل','في','من','الى','على','ما','ماذا','كيف','كم','هذا','هذه','هناك']

CATEGORY_HINTS = {
    'دوام': ['دوام','ساعات','عمل','وقت'],
    'تواصل': ['اتصال','هاتف','بريد','ايميل','تحويلة'],
    'مواقع': ['اين','أين','موقع','مبنى','مكان']
}

RATE_LIMIT = 5
WINDOW = 60
requests_log = defaultdict(list)

def db():
    return sqlite3.connect(DB_FILE)

if not os.path.exists(DB_FILE):
    conn=db()
    c=conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS unanswered (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, created_at TEXT)')
    conn.commit()
    conn.close()

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE,'w',encoding='utf-8') as f:
        json.dump([],f,ensure_ascii=False)

with open(DATA_FILE,'r',encoding='utf-8-sig') as f:
    INFOS = json.load(f)

def split_text(text, max_len=500):
    parts=[]
    buf=''
    for line in text.splitlines():
        line=line.strip()
        if not line:
            continue
        if len(buf)+len(line) <= max_len:
            buf += ' ' + line
        else:
            parts.append(buf.strip())
            buf = line
    if buf.strip():
        parts.append(buf.strip())
    return parts

def map_synonym(word):
    for k,v in SYNONYMS.items():
        if word in v:
            return k
    return word

def normalize(text):
    text=text.lower()
    text=re.sub(r'[^\w\s]','',text)
    words=[]
    for w in text.split():
        if w in STOP_WORDS:
            continue
        if w.startswith('ال') and len(w)>2:
            w=w[2:]
        words.append(map_synonym(w))
    return words

def detect_category(words):
    for c,k in CATEGORY_HINTS.items():
        if any(x in words for x in k):
            return c
    return None

def score(query_words, text):
    text_words = normalize(text)
    s = 0
    for w in query_words:
        if w in text_words:
            s += 3 if w in SYNONYMS else 1
    return s

def log_unanswered(q):
    conn=db()
    c=conn.cursor()
    c.execute('INSERT INTO unanswered (question, created_at) VALUES (?,?)',(q,datetime.now().isoformat()))
    conn.commit()
    conn.close()

def allowed(ip):
    now=time()
    requests_log[ip]=[t for t in requests_log[ip] if now-t<WINDOW]
    if len(requests_log[ip])>=RATE_LIMIT:
        return False
    requests_log[ip].append(now)
    return True

def find_answer(q):
    words=normalize(q)
    cat=detect_category(words)
    candidates=INFOS if not cat else [i for i in INFOS if i['category']==cat]
    best=None
    smax=0
    for i in candidates:
        s=score(words,i['text'])
        if s>smax:
            smax=s
            best=i
    if smax>0:
        return best['text']
    log_unanswered(q)
    return SUPPORT_TEXT

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/ask',methods=['POST'])
def ask():
    if not allowed(request.remote_addr):
        return jsonify({'reply':'يرجى الانتظار'})
    return jsonify({'reply':find_answer(request.json.get('message',''))})

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/login',methods=['POST'])
def admin_login():
    if request.json.get('pw')==ADMIN_PASSWORD:
        return jsonify({'ok':True})
    return jsonify({'ok':False})

@app.route('/admin/add_info',methods=['POST'])
def add_info():
    text = request.json.get('text','').strip()
    category = request.json.get('category','')

    if not text or not category:
        return jsonify({'error':True})

    chunks = split_text(text)

    for c in chunks:
        INFOS.append({'text':c,'category':category})

    with open(DATA_FILE,'w',encoding='utf-8') as f:
        json.dump(INFOS,f,ensure_ascii=False,indent=2)

    return jsonify({'ok':True,'saved':len(chunks)})

@app.route('/admin/export/unanswered')
def export_unanswered():
    conn=db()
    df=pd.read_sql_query('SELECT * FROM unanswered',conn)
    conn.close()
    file='unanswered_questions.xlsx'
    df.to_excel(file,index=False)
    return send_file(file,as_attachment=True)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
