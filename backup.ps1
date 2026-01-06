python - << 'EOF'
import shutil, datetime
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy('info.json', f'backup_info_{ts}.json')
print('BACKUP DONE')
EOF
