python - << 'EOF'
import os
from collections import Counter

log='forwarded.log'
if not os.path.exists(log):
    print('NO DATA')
    exit()

with open(log,encoding='utf-8') as f:
    qs=[l.split('|',1)[1].strip() for l in f if '|' in l]

c=Counter(qs)
print('MOST FREQUENT UNANSWERED:')
for q,n in c.most_common(10):
    print(n,'-',q)
EOF
