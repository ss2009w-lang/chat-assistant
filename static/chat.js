function send(){
  const t=input.value.trim()
  if(!t)return
  const m=document.createElement('div')
  m.innerText=t
  messages.appendChild(m)
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
  })
}
