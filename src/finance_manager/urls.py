"""
URL configuration for finance_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import dashboard, admin_portal, export_invoice_pdf, dashboard_redirect, login_success, export_invoices_csv, add_company, custom_logout, add_gerant, add_collaborator # Ajoute admin_portal ici
from django.urls import path, include # Importe include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('dashboard_redirect'), name='home'),  # Redirect root to dashboard redirect
    path('admin/', admin.site.urls),
    path('dashboard/<int:company_id>/', dashboard, name='dashboard'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    path('login-success/', login_success, name='login_success'),
    path('portal/', admin_portal, name='admin_portal'),
    path('add-company/', add_company, name='add_company'),
    path('logout/', custom_logout, name='custom_logout'),
    # Ajoute ceci pour gérer login/logout automatiquement
    path('accounts/', include('django.contrib.auth.urls')), 
    path('invoice/<int:invoice_id>/pdf/', export_invoice_pdf, name='export_invoice_pdf'),
    path('export-csv/<int:company_id>/', export_invoices_csv, name='export_invoices_csv'),
    path('add-gerant/<int:company_id>/', add_gerant, name='add_gerant'),
    path('add-collaborator/<int:company_id>/', add_collaborator, name='add_collaborator'),
]