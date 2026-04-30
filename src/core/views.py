from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
import csv
from .models import Invoice, Company, Client, Payment
from .forms import InvoiceForm, ClientForm, PaymentForm, InvoiceLineFormSet

def home(request):
    """Page d'accueil publique"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')

@login_required
def dashboard_redirect(request):
    """Redirige l'utilisateur vers son dashboard de facturation"""
    return redirect('dashboard')

@login_required
def login_success(request):
    """Redirige l'utilisateur vers le dashboard après la connexion"""
    return redirect('dashboard')

@login_required
def dashboard(request):
    company = Company.objects.first()
    if not company:
        return render(request, 'core/no_company.html')

    invoices = Invoice.objects.filter(company=company).order_by('-date')
    clients = Client.objects.all()

    # Métriques dashboard
    total_ht = sum(inv.amount_ht for inv in invoices)
    total_ttc = sum(inv.amount_ttc for inv in invoices)
    paid_invoices = invoices.filter(status='PAID')
    unpaid_invoices = invoices.filter(status__in=['DRAFT', 'SENT', 'OVERDUE'])
    overdue_invoices = invoices.filter(status='OVERDUE')

    # Chiffre d'affaires par mois (pour graphique)
    from django.db.models import Sum
    from django.db.models.functions import TruncMonth
    monthly_revenue = (
        invoices.annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount_ht'))
        .order_by('month')
    )

    context = {
        'company': company,
        'invoices': invoices,
        'clients': clients,
        'total_ht': total_ht,
        'total_ttc': total_ttc,
        'paid_count': paid_invoices.count(),
        'unpaid_count': unpaid_invoices.count(),
        'overdue_count': overdue_invoices.count(),
        'client_count': clients.count(),
        'monthly_revenue': list(monthly_revenue),
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def export_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Importer xhtml2pdf seulement quand nécessaire
    try:
        from xhtml2pdf import pisa
    except ImportError as e:
        error_msg = f"""
        PDF export unavailable: xhtml2pdf library not installed.
        
        Error: {str(e)}
        
        Install with: pip install xhtml2pdf
        """
        return HttpResponse(error_msg, content_type='text/plain')
    
    # CALCULS DE TVA POUR LE PDF
    tva_rate = 20  # Ou invoice.company.tva_rate si tu as ajouté ce champ
    amount_tva = float(invoice.amount_ht) * (tva_rate / 100)
    amount_ttc = float(invoice.amount_ht) + amount_tva

    context = {
        'invoice': invoice,
        'company': invoice.company,
        'amount_tva': amount_tva,
        'amount_ttc': amount_ttc,
        'tva_rate': tva_rate,
    }
    
    try:
        html_string = render_to_string('core/invoice_pdf_template.html', context)
        
        # Créer le PDF avec xhtml2pdf
        from io import BytesIO
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html_string, dest=pdf_buffer)
        
        if pisa_status.err:
            return HttpResponse('Erreur lors de la génération du PDF', status=500)
        
        pdf_buffer.seek(0)
        response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Facture_{invoice.number}.pdf"'
        return response
    except Exception as e:
        error_msg = f"""
        PDF export failed: {str(e)}
        
        xhtml2pdf requires proper installation.
        """
        return HttpResponse(error_msg, content_type='text/plain')

@login_required
def export_invoices_csv(request):
    company = Company.objects.first()
    if not company:
        raise PermissionDenied("Aucune entreprise configurée.")

    invoices = Invoice.objects.filter(company=company).order_by('-date')
    
    # Création du fichier CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="export_factures_{company.name}.csv"'
    
    writer = csv.writer(response)
    # En-têtes du CSV
    writer.writerow(['Numéro Facture', 'Client', 'Montant HT', 'TVA (20%)', 'Montant TTC', 'Statut', 'Date'])
    
    # Données des factures
    for inv in invoices:
        tva_amount = float(inv.amount_ht) * 0.20
        ttc_amount = float(inv.amount_ht) + tva_amount
        writer.writerow([
            inv.number,
            inv.client.name if inv.client else 'N/A',
            f"{inv.amount_ht:.2f}",
            f"{tva_amount:.2f}",
            f"{ttc_amount:.2f}",
            inv.get_status_display(),
            inv.date.strftime('%d/%m/%Y')
        ])
        
    return response

@login_required
def custom_logout(request):
    """Vue personnalisée de déconnexion qui redirige vers la page de connexion"""
    from django.contrib.auth import logout
    logout(request)
    return redirect('/accounts/login/')

# --- Client CRUD Views ---

@login_required
def client_list(request):
    company = Company.objects.first()
    clients = Client.objects.all().order_by('name')
    return render(request, 'core/client_list.html', {'clients': clients, 'company': company})

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'core/client_form.html', {'form': form, 'title': 'Nouveau Client'})

@login_required
def client_edit(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'core/client_form.html', {'form': form, 'title': 'Modifier Client'})

@login_required
def client_delete(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'core/client_confirm_delete.html', {'client': client})

# --- Payment Views ---

@login_required
def add_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()
            # Marquer la facture comme payée si le montant total est atteint
            if invoice.remaining_amount <= 0:
                invoice.status = 'PAID'
                invoice.save()
            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = PaymentForm()
    return render(request, 'core/payment_form.html', {'form': form, 'invoice': invoice})

@login_required
def payment_history(request):
    company = Company.objects.first()
    payments = Payment.objects.select_related('invoice').order_by('-date')
    return render(request, 'core/payment_history.html', {'payments': payments, 'company': company})

@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    company = Company.objects.first()
    return render(request, 'core/invoice_detail.html', {'invoice': invoice, 'company': company})

@login_required
def invoice_create(request):
    company = Company.objects.first()
    if not company:
        return render(request, 'core/no_company.html')
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceLineFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.company = company
            invoice.save()
            
            formset.instance = invoice
            formset.save()
            
            # Recalculer le montant HT à partir des lignes sauvegardées
            invoice.amount_ht = sum(line.quantity * line.unit_price for line in invoice.lines.all())
            invoice.save()
            
            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm()
        formset = InvoiceLineFormSet()
    
    return render(request, 'core/invoice_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Nouvelle Facture'
    })

@login_required
def invoice_edit(request, invoice_id):
    company = Company.objects.first()
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceLineFormSet(request.POST, instance=invoice)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.save()
            
            formset.save()
            
            # Recalculer le montant HT à partir des lignes sauvegardées
            invoice.amount_ht = sum(line.quantity * line.unit_price for line in invoice.lines.all())
            invoice.save()
            
            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceLineFormSet(instance=invoice)
    
    return render(request, 'core/invoice_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Modifier Facture',
        'invoice': invoice
    })

