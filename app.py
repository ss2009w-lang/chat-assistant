from flask import Flask, request, jsonify, render_template
import json, os, sqlite3, re
from datetime import datetime
from docx import Document

app = Flask(__name__)
app.secret_key = 'firas-secret'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

DATA_FILE = 'info.json'
UPLOAD_DIR = 'uploads'

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

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

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/ask',methods=['POST'])
def ask():
    return jsonify({'reply':'تم استلام سؤالك'})

@app.route('/admin/upload',methods=['POST'])
def upload_word():
    file = request.files.get('file')
    category = request.form.get('category','عام')

    if not file or not file.filename.endswith('.docx'):
        return jsonify({'error':True})

    path = os.path.join(UPLOAD_DIR,file.filename)
    file.save(path)

    doc = Document(path)
    text = '\\n'.join([p.text for p in doc.paragraphs if p.text.strip()])

    chunks = split_text(text)

    for c in chunks:
        INFOS.append({'text':c,'category':category})

    with open(DATA_FILE,'w',encoding='utf-8') as f:
        json.dump(INFOS,f,ensure_ascii=False,indent=2)

    return jsonify({'ok':True,'saved':len(chunks)})

if __name__=='__main__':
    app.run(debug=True)
