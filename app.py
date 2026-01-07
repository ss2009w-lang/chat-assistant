from flask import Flask, request, jsonify, render_template, session
import json, os, sqlite3, re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'firas-session-secret'

DATA_FILE = 'info.json'
DB_FILE = 'service.db'

def db():
    return sqlite3.connect(DB_FILE)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE,'w',encoding='utf-8') as f:
        json.dump([],f,ensure_ascii=False)

with open(DATA_FILE,'r',encoding='utf-8-sig') as f:
    INFOS = json.load(f)

def normalize(t):
    t=t.lower()
    t=re.sub(r'[^\w\s]','',t)
    return t.split()

def score(q,t):
    return len(set(normalize(q)) & set(normalize(t)))

def auto_ticket(q):
    u=session.get('user',{})
    conn=db()
    c=conn.cursor()
    c.execute(
      'INSERT INTO tickets (name,email,phone,department,type,message,source,created_at) VALUES (?,?,?,?,?,?,?,?)',
      (u.get('name'),u.get('email'),u.get('phone'),'عام','سؤال',q,'bot',datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def find_answer(q):
    best=None
    smax=0
    for i in INFOS:
        s=score(q,i['text'])
        if s>smax:
            smax=s
            best=i
    if smax>0:
        return best['text']
    auto_ticket(q)
    return 'تم تحويل سؤالك تلقائيًا إلى تذكرة، وسيتم التواصل معك.'

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login',methods=['POST'])
def login():
    session['user']=request.json
    return jsonify({'ok':True})

@app.route('/ask',methods=['POST'])
def ask():
    return jsonify({'reply':find_answer(request.json.get('message',''))})

@app.route('/rate',methods=['POST'])
def rate():
    u=session.get('user',{})
    conn=db()
    c=conn.cursor()
    c.execute(
      'INSERT INTO ratings (name,rating,created_at) VALUES (?,?,?)',
      (u.get('name'),request.json.get('rating'),datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    session.clear()
    return jsonify({'ok':True})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
