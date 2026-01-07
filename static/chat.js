function show(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'))
  document.getElementById(id).classList.add('active')
}

function goOptions(){show('options')}
function startChat(){
  show('chat')
  add('bot','السلام عليكم، معك المساعد الذكي فراس. كيف يمكنني خدمتك؟')
}
function openTicket(){show('ticket')}
function submitTicket(){
  alert('تم استلام التذكرة وسيتم التواصل معك')
  show('end')
}

function send(){
  const i=document.getElementById('input')
  const t=i.value.trim()
  if(!t)return
  add('user',t)
  i.value=''
  fetch('/ask',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({message:t})
  })
  .then(r=>r.json())
  .then(d=>{
    add('bot',d.reply)
    setTimeout(()=>show('end'),1000)
  })
}

function add(type,text){
  const d=document.createElement('div')
  d.className='msg '+type
  d.innerText=text
  document.getElementById('messages').appendChild(d)
}

function rate(){show('rate')}
function finish(){alert('شكرًا لتقييمك');location.reload()}
