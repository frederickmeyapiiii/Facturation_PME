import os
import sys
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.filter(username='admin').first()
if not u:
    print('MISSING')
else:
    print('EXISTS', u.username, u.is_superuser, u.is_staff, u.check_password('Admin123!'))
