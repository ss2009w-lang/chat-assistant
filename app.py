from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

with open("knowledge.json", encoding="utf-8-sig") as f:
    KB = json.load(f)

def find_answer(user_input):
    text = user_input.lower()
    for item in KB:
        if item["question"] in text:
            return item["answer"]
    return "لا أملك إجابة على هذا السؤال ضمن المعلومات المتاحة."

@app.route("/")
def chat():
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("message", "")
    answer = find_answer(question)
    return jsonify({"reply": answer})

if __name__ == "__main__":
    app.run()
# test commit author
