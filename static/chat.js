function send() {
  const input = document.getElementById('input');
  const text = input.value;
  if (!text) return;

  addMessage('user', text);
  input.value = '';

  fetch('/ask', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: text})
  })
  .then(res => res.json())
  .then(data => {
    addMessage('bot', data.answer);
    if (data.suggestions && data.suggestions.length > 0) {
      data.suggestions.forEach(s => {
        addMessage('bot', '• ' + s);
      });
    }
  });
}

function addMessage(type, text) {
  const div = document.createElement('div');
  div.className = 'msg ' + type;
  div.innerText = text;
  document.getElementById('messages').appendChild(div);
}
