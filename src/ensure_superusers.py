import os
import sys
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from core.models import Company

User = get_user_model()
company, created = Company.objects.get_or_create(name='Assistant Saas', siret='12345678901234')
if created:
    print('Created company Assistant Saas')

users = [
    {
        'username': 'admin',
        'password': 'Admin123!',
        'email': 'admin@example.com',
        'is_superuser': True,
        'is_staff': True,
        'role': 'EXPERT',
        'company': None,
    },
    {
        'username': 'assistant',
        'password': 'Assistant123!',
        'email': 'assistant@example.com',
        'is_superuser': False,
        'is_staff': False,
        'role': 'GERANT',
        'company': company,
    },
]

for data in users:
    user = User.objects.filter(username=data['username']).first()
    if user:
        user.set_password(data['password'])
        user.email = data['email']
        user.is_superuser = data['is_superuser']
        user.is_staff = data['is_staff']
        user.save()
        profile = user.profile
        profile.role = data['role']
        profile.company = data['company']
        profile.save()
        print(f"UPDATED {data['username']}")
    else:
        if data['is_superuser']:
            user = User.objects.create_superuser(
                username=data['username'],
                email=data['email'],
                password=data['password'],
            )
        else:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
            )
        profile = user.profile
        profile.role = data['role']
        profile.company = data['company']
        profile.save()
        print(f"CREATED {data['username']}")
