from flask import Flask, request, jsonify, render_template, session, send_file, redirect
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

@app.route('/admin/login',methods=['GET','POST'])
def admin_login():
    if request.method=='GET':
        return render_template('admin_login.html')
    d=request.form
    conn=db()
    c=conn.cursor()
    c.execute('SELECT role FROM admins WHERE username=? AND password=?',(d['username'],d['password']))
    r=c.fetchone()
    conn.close()
    if r:
        session['admin_role']=r[0]
        return redirect('/admin')
    return redirect('/admin/login')

@app.route('/admin')
def admin():
    if 'admin_role' not in session:
        return redirect('/admin/login')

    conn=db()
    c=conn.cursor()

    if session['admin_role']!='super':
        c.execute(
          'SELECT id,category,priority,message,status,created_at FROM reports WHERE category IN (SELECT category FROM report_roles WHERE role=?)',
          (session['admin_role'],)
        )
    else:
        c.execute('SELECT id,category,priority,message,status,created_at FROM reports')

    reports=c.fetchall()
    conn.close()
    return render_template('admin.html',reports=reports)

@app.route('/admin/update',methods=['POST'])
def update():
    if 'admin_role' not in session:
        return jsonify({'ok':False})
    d=request.json
    conn=db()
    c=conn.cursor()
    c.execute('UPDATE reports SET status=? WHERE id=?',(d['status'],d['id']))
    conn.commit()
    conn.close()
    return jsonify({'ok':True})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
