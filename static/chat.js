let user={}

function show(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'))
  document.getElementById(id).classList.add('active')
}

function goOptions(){
  user.name=name.value
  user.email=email.value
  user.phone=phone.value
  show('options')
}

function startChat(){show('chat')}

function openTicket(){show('ticket')}

function submitTicket(){
  fetch('/ticket',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({
      name:user.name,
      email:user.email,
      phone:user.phone,
      type:document.getElementById('ticketType').value
    })
  }).then(()=>show('end'))
}

function send(){
  const t=input.value.trim()
  if(!t)return
  add('user',t)
  input.value=''
  fetch('/ask',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({message:t})
  })
  .then(r=>r.json())
  .then(d=>{
    add('bot',d.reply)
    setTimeout(()=>show('end'),800)
  })
}

function add(type,text){
  const d=document.createElement('div')
  d.className='msg '+type
  d.innerText=text
  messages.appendChild(d)
}

function rate(){
  fetch('/rate',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({
      name:user.name,
      rating:document.getElementById('rating').selectedIndex+1
    })
  }).then(()=>location.reload())
}
