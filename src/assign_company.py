import os
import sys
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')
import django
django.setup()
from core.models import Company
from django.contrib.auth import get_user_model
User = get_user_model()
company, created = Company.objects.get_or_create(name='Assistant Saas', siret='12345678901234')
print('COMPANY', 'created' if created else 'existing', company.name)
for username in ['assistant', 'admin']:
    u = User.objects.filter(username=username).first()
    if not u:
        print('MISSING USER', username)
        continue
    try:
        profile = u.profile
    except Exception:
        profile = None
    if not profile:
        print('NO PROFILE', username)
        continue
    profile.company = company
    profile.role = 'GERANT'
    profile.save()
    print('ASSIGNED', username, 'to', company.name)
