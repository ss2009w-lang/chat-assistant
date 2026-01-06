let typingIndicator = null;

window.onload = function () {
  addMessage('bot', 'السلام عليكم ورحمة الله وبركاته، معك المساعد الذكي فراس كيف يمكن أن أخدمك؟');
};

function send(textOverride=null) {
  const input = document.getElementById('input');
  const text = textOverride || input.value;
  if (!text) return;

  addMessage('user', text);
  input.value = '';
  showTyping();

  fetch('/ask', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: text})
  })
  .then(res => res.json())
  .then(data => {
    hideTyping();
    addMessage('bot', data.reply);
  });
}

function showTyping() {
  typingIndicator = document.createElement('div');
  typingIndicator.className = 'msg bot';
  typingIndicator.innerText = 'فراس يكتب...';
  document.getElementById('messages').appendChild(typingIndicator);
}

function hideTyping() {
  if (typingIndicator) typingIndicator.remove();
}

function addMessage(type, text) {
  const div = document.createElement('div');
  div.className = 'msg ' + type;

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.innerText = text;

  const time = document.createElement('div');
  time.className = 'time';
  time.innerText = new Date().toLocaleTimeString('ar-SA', {hour: '2-digit', minute:'2-digit'});

  div.appendChild(bubble);
  div.appendChild(time);

  document.getElementById('messages').appendChild(div);
  document.getElementById('messages').scrollTop =
    document.getElementById('messages').scrollHeight;
}

document.addEventListener('keypress', function(e) {
  if (e.key === 'Enter') send();
});
