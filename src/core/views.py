from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
import csv
from .models import Invoice, Company
from .forms import InvoiceForm

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
    
    # --- LOGIQUE DU FORMULAIRE ---
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.company = company # On lie la facture à l'entreprise actuelle
            invoice.save()
            return redirect('dashboard')
    else:
        from datetime import date
        form = InvoiceForm(initial={
            'date': date.today(),
            'tva_rate': 20.0,
            'status': 'DRAFT'
        })
    # -----------------------------

    invoices = Invoice.objects.filter(company=company).order_by('-date')

    context = {
        'company': company,
        'invoices': invoices,
        'form': form, # On passe le formulaire au template
        'total_ht': sum(inv.amount_ht for inv in invoices),
        'pending_count': invoices.filter(status='SENT').count(),
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
            inv.client_name,
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

