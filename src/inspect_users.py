import os
import sys
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from core.models import Company
User = get_user_model()
for username in ['assistant', 'admin']:
    u = User.objects.filter(username=username).first()
    if not u:
        print('MISSING USER', username)
        continue
    profile = None
    try:
        profile = u.profile
    except Exception:
        pass
    print('USER', username, 'is_superuser', u.is_superuser, 'is_staff', u.is_staff, 'profile', bool(profile), 'role', getattr(profile, 'role', None), 'company', getattr(profile.company, 'name', None) if profile else None)
print('COMPANIES', Company.objects.count(), [c.name for c in Company.objects.all()])
