const input=document.getElementById('input')
const messages=document.getElementById('messages')

input.addEventListener('keydown',function(e){
  if(e.key==='Enter'){send()}
})

function send(){
  const t=input.value.trim()
  if(!t)return
  const u=document.createElement('div')
  u.innerText=t
  messages.appendChild(u)
  input.value=''
  fetch('/ask',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({message:t})
  })
  .then(r=>r.json())
  .then(d=>{
    const b=document.createElement('div')
    b.innerText=d.reply
    messages.appendChild(b)
    messages.scrollTop=messages.scrollHeight
  })
}
