python - << 'EOF'
import time, collections
RATE_LIMIT = 5
WINDOW = 60
requests = collections.defaultdict(list)

def allow(ip):
    now = time.time()
    requests[ip] = [t for t in requests[ip] if now - t < WINDOW]
    if len(requests[ip]) >= RATE_LIMIT:
        return False
    requests[ip].append(now)
    return True

print('RATE LIMIT MODULE READY')
EOF
