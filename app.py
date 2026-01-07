from flask import Flask, render_template, request, jsonify, session, redirect
import json, re, sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'firas-secret'

DATA_FILE='info.json'
DB_FILE='service.db'

def db():
    return sqlite3.connect(DB_FILE)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/login',methods=['POST'])
def login():
    session['user']=request.json
    return jsonify({'ok':True})

@app.route('/ask',methods=['POST'])
def ask():
    return jsonify({'reply':'الواجهة عادت للعمل بنجاح'})

@app.route('/admin/login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)
