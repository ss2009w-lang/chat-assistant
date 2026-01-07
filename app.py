from flask import Flask, request, jsonify, render_template
import json, os, sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'firas-secret'

DATA_FILE = 'info.json'
DB_FILE = 'service.db'

def db():
    return sqlite3.connect(DB_FILE)

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    return jsonify({'reply':'تم استلام سؤالك وسيتم الرد من النظام'})

@app.route('/ticket', methods=['POST'])
def ticket():
    data = request.json
    conn=db()
    c=conn.cursor()
    c.execute(
      'INSERT INTO tickets (name,email,phone,type,created_at) VALUES (?,?,?,?,?)',
      (data['name'],data['email'],data['phone'],data['type'],datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return jsonify({'ok':True})

@app.route('/rate', methods=['POST'])
def rate():
    data=request.json
    conn=db()
    c=conn.cursor()
    c.execute(
      'INSERT INTO ratings (name,rating,created_at) VALUES (?,?,?)',
      (data['name'],data['rating'],datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return jsonify({'ok':True})

if __name__=='__main__':
    app.run(debug=True)
