python - << 'EOF'
import json, csv
with open('info.json', encoding='utf-8-sig') as f:
    data = json.load(f)
with open('info_export.csv','w',newline='',encoding='utf-8') as c:
    w = csv.writer(c)
    w.writerow(['category','text'])
    for i in data:
        w.writerow([i.get('category',''), i.get('text','')])
print('EXPORT DONE')
EOF
