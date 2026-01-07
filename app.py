from flask import Flask, request, jsonify, render_template, session
import json, os, re, sqlite3
from datetime import datetime
from docx import Document

app = Flask(__name__)
app.secret_key = 'firas-secret'

DATA_FILE = 'info.json'
DB_FILE = 'service.db'
UPLOAD_DIR = 'uploads'

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

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

def similarity(q, text):
    return len(set(normalize(q)) & set(normalize(text)))

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login', methods=['POST'])
def login():
    d=request.json
    conn=db()
    c=conn.cursor()
    c.execute(
      'INSERT INTO users (name,email,phone,created_at) VALUES (?,?,?,?)',
      (d['name'],d['email'],d['phone'],datetime.now().isoformat())
    )
    uid=c.lastrowid
    conn.commit()
    conn.close()
    session['user_id']=uid
    return jsonify({'ok':True})

@app.route('/ask', methods=['POST'])
def ask():
    if 'user_id' not in session:
        return jsonify({'reply':'يرجى تسجيل الدخول أولًا'})
    q=request.json.get('message','')
    best=None
    score=0
    for i in INFOS:
        s=similarity(q,i['text'])
        if s>score:
            score=s
            best=i['text']
    if not best:
        best='لا توجد معلومة مطابقة، تم تحويل طلبك للدعم.'
    conn=db()
    c=conn.cursor()
    c.execute(
      'INSERT INTO questions (user_id,question,answer,created_at) VALUES (?,?,?,?)',
      (session['user_id'],q,best,datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return jsonify({'reply':best})

@app.route('/rate', methods=['POST'])
def rate():
    if 'user_id' not in session:
        return jsonify({'ok':False})
    conn=db()
    c=conn.cursor()
    c.execute(
      'INSERT INTO ratings (user_id,rating,created_at) VALUES (?,?,?)',
      (session['user_id'],request.json.get('rating'),datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    session.clear()
    return jsonify({'ok':True})

@app.route('/admin/upload', methods=['POST'])
def upload():
    file=request.files.get('file')
    if not file or not file.filename.endswith('.docx'):
        return jsonify({'error':True})
    path=os.path.join(UPLOAD_DIR,file.filename)
    file.save(path)
    doc=Document(path)
    INFOS.clear()
    for p in doc.paragraphs:
        t=p.text.strip()
        if len(t)>10:
            INFOS.append({'text':t})
    with open(DATA_FILE,'w',encoding='utf-8') as f:
        json.dump(INFOS,f,ensure_ascii=False,indent=2)
    return jsonify({'ok':True,'count':len(INFOS)})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
