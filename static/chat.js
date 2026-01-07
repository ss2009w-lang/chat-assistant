const input=document.getElementById('input')
const messages=document.getElementById('messages')

input.addEventListener('keydown',e=>{if(e.key==='Enter')send()})

function add(text,type){
  const d=document.createElement('div')
  d.className='msg '+type
  d.innerText=text
  messages.appendChild(d)
  messages.scrollTop=messages.scrollHeight
}

function send(){
  const t=input.value.trim()
  if(!t)return
  add(t,'user')
  input.value=''
  fetch('/ask',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({message:t})
  })
  .then(r=>r.json())
  .then(d=>{
    add(d.reply,'bot')
    setTimeout(()=>endFlow(),800)
  })
}

function endFlow(){
  add('هل ترغب في خدمة أخرى؟ اكتب نعم أو لا','bot')
}

function rate(v){
  fetch('/rate',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({rating:v})
  }).then(()=>location.reload())
}
