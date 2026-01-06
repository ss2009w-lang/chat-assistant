window.onload=function(){
  add('bot','السلام عليكم ورحمة الله وبركاته، معك المساعد الذكي فراس. كيف يمكنني خدمتك؟')
  document.getElementById('input').addEventListener('keydown',function(e){
    if(e.key==='Enter'){send()}
  })
}

function send(){
  const i=document.getElementById('input')
  const t=i.value.trim()
  if(!t)return
  add('user',t)
  i.value=''
  document.getElementById('typing').style.display='block'

  fetch('/ask',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({message:t})
  })
  .then(r=>r.json())
  .then(d=>{
    document.getElementById('typing').style.display='none'
    add('bot',d.reply)
  })
}

function add(type,text){
  const d=document.createElement('div')
  d.className='msg '+type
  d.innerText=text
  const m=document.getElementById('messages')
  m.appendChild(d)
  m.scrollTop=m.scrollHeight
}
