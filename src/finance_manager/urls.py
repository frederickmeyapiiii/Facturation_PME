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
from django.urls import path, include
from django.shortcuts import redirect
from core.views import (
    home, dashboard, export_invoice_pdf, login_success, export_invoices_csv, custom_logout,
    client_list, client_create, client_edit, client_delete,
    add_payment, payment_history, invoice_detail, invoice_create, invoice_edit
)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard, name='dashboard'),
    path('login-success/', login_success, name='login_success'),
    path('logout/', custom_logout, name='custom_logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('invoice/<int:invoice_id>/pdf/', export_invoice_pdf, name='export_invoice_pdf'),
    path('invoice/new/', invoice_create, name='invoice_create'),
    path('invoice/<int:invoice_id>/', invoice_detail, name='invoice_detail'),
    path('invoice/<int:invoice_id>/edit/', invoice_edit, name='invoice_edit'),
    path('invoice/<int:invoice_id>/payment/', add_payment, name='add_payment'),
    path('export-csv/', export_invoices_csv, name='export_invoices_csv'),
    path('clients/', client_list, name='client_list'),
    path('clients/new/', client_create, name='client_create'),
    path('clients/<int:client_id>/edit/', client_edit, name='client_edit'),
    path('clients/<int:client_id>/delete/', client_delete, name='client_delete'),
    path('payments/', payment_history, name='payment_history'),
    path('metrics/', include('django_prometheus.urls')),
]