python - << 'EOF'
import json, os
print('BOT: FIRAS')
print('INFOS:', len(json.load(open('info.json', encoding='utf-8-sig'))))
print('FORWARDED LOG EXISTS:', os.path.exists('forwarded.log'))
print('STATUS: OK')
EOF
