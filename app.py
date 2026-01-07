from flask import Flask, request, jsonify, render_template, session
import json, os, re, sqlite3
from datetime import datetime
from docx import Document

app = Flask(__name__)
app.secret_key = 'firas-secret'

DATA_FILE = 'info.json'
DB_FILE = 'service.db'
UPLOAD_DIR = 'uploads'

def db():
    return sqlite3.connect(DB_FILE)

with open(DATA_FILE,'r',encoding='utf-8-sig') as f:
    INFOS = json.load(f)

def normalize(t):
    t=t.lower()
    t=re.sub(r'[^\w\s]','',t)
    return t.split()

def similarity(q, text):
    return len(set(normalize(q)) & set(normalize(text)))

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/login',methods=['POST'])
def login():
    session['user']=request.json
    return jsonify({'ok':True})

@app.route('/ask',methods=['POST'])
def ask():
    q=request.json.get('message','')
    best=None
    score=0
    for i in INFOS:
        s=similarity(q,i['text'])
        if s>score:
            score=s
            best=i['text']
    if not best:
        return jsonify({'reply':'لم أجد إجابة، يمكنك رفع بلاغ رسمي.'})
    return jsonify({'reply':best})

@app.route('/report',methods=['POST'])
def report():
    if 'user' not in session:
        return jsonify({'ok':False})
    d=request.json
    conn=db()
    c=conn.cursor()
    c.execute(
      'INSERT INTO reports (user_id,category,priority,message,status,created_at) VALUES (?,?,?,?,?,?)',
      (
        session['user'].get('email'),
        d.get('category'),
        d.get('priority'),
        d.get('message'),
        'جديد',
        datetime.now().isoformat()
      )
    )
    conn.commit()
    conn.close()
    return jsonify({'ok':True})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
