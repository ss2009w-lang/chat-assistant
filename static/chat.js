window.onload=function(){
  add('bot','السلام عليكم ورحمة الله وبركاته، معك المساعد الذكي فراس. كيف يمكنني خدمتك؟')
}

function send(){
  const i=document.getElementById('txt')
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
  .then(d=>add('bot',d.reply))
}

function add(type,text){
  const d=document.createElement('div')
  d.className='msg '+type
  d.innerText=text
  const m=document.getElementById('msgs')
  m.appendChild(d)
  m.scrollTop=m.scrollHeight
}
