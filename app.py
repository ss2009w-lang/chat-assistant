from flask import Flask, request, jsonify, render_template, session, send_file
import json, os, re, sqlite3
from datetime import datetime
from docx import Document
from openpyxl import Workbook

app = Flask(__name__)
app.secret_key = 'firas-secret'

DATA_FILE='info.json'
DB_FILE='service.db'

def db():
    return sqlite3.connect(DB_FILE)

with open(DATA_FILE,'r',encoding='utf-8-sig') as f:
    INFOS=json.load(f)

def normalize(t):
    t=t.lower()
    t=re.sub(r'[^\w\s]','',t)
    return t.split()

def similarity(q,text):
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
    d=request.json
    conn=db()
    c=conn.cursor()
    c.execute(
      'INSERT INTO reports (user_id,category,priority,message,status,created_at) VALUES (?,?,?,?,?,?)',
      (session['user'].get('email'),d['category'],d['priority'],d['message'],'جديد',datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return jsonify({'ok':True})

@app.route('/admin')
def admin():
    conn=db()
    c=conn.cursor()
    c.execute('SELECT id,category,priority,message,status,created_at FROM reports ORDER BY created_at DESC')
    reports=c.fetchall()

    c.execute('SELECT category,COUNT(*) FROM reports GROUP BY category')
    stats=c.fetchall()
    conn.close()

    return render_template('admin.html',reports=reports,stats=stats)

@app.route('/admin/update',methods=['POST'])
def update():
    d=request.json
    conn=db()
    c=conn.cursor()
    c.execute('UPDATE reports SET status=? WHERE id=?',(d['status'],d['id']))
    conn.commit()
    conn.close()
    return jsonify({'ok':True})

@app.route('/admin/export')
def export():
    wb=Workbook()
    ws=wb.active
    ws.append(['ID','Category','Priority','Message','Status','Date'])

    conn=db()
    c=conn.cursor()
    c.execute('SELECT id,category,priority,message,status,created_at FROM reports')
    for r in c.fetchall():
        ws.append(r)
    conn.close()

    file='reports.xlsx'
    wb.save(file)
    return send_file(file,as_attachment=True)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
