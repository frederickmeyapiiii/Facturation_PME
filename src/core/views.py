from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
import csv
from .models import Invoice, Company, Profile
from .forms import InvoiceForm, UserCreationFormSimple # Importe ton nouveau formulaire

# Import pour la génération PDF - Chargé à la demande
WEASYPRINT_AVAILABLE = False

@login_required
def dashboard_redirect(request):
    """Redirige vers le dashboard approprié selon le profil utilisateur"""
    profile = request.user.profile
    
    if profile.role == 'EXPERT':
        # Les experts vont au portail admin pour choisir une entreprise
        return redirect('admin_portal')
    else:
        # Les gérants et collaborateurs vont à leur entreprise
        if profile.company:
            return redirect('dashboard', company_id=profile.company.id)
        else:
            return render(request, 'core/no_company.html')

@login_required
def login_success(request):
    """Redirige l'utilisateur vers le bon dashboard après la connexion"""
    profile = request.user.profile
    if profile.role == 'EXPERT':
        return redirect('admin_portal')
    else:
        # Vérifier que l'utilisateur a une entreprise assignée
        if profile.company:
            return redirect('dashboard', company_id=profile.company.id)
        else:
            # Si pas d'entreprise, rediriger vers la page d'erreur
            return render(request, 'core/no_company.html')

@login_required
def dashboard(request, company_id):
    profile = request.user.profile
    if profile.role != 'EXPERT' and profile.company.id != company_id:
        raise PermissionDenied()

    company = get_object_or_404(Company, id=company_id)
    
    # --- LOGIQUE DU FORMULAIRE ---
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.company = company # On lie la facture à l'entreprise actuelle
            invoice.save()
            return redirect('dashboard', company_id=company.id)
    else:
        from datetime import date
        form = InvoiceForm(initial={
            'date': date.today(),
            'tva_rate': 20.0,
            'status': 'DRAFT'
        })
    # -----------------------------

    invoices = Invoice.objects.filter(company=company).order_by('-date')
    is_collab = (profile.role == 'COLLAB')
    
    context = {
        'company': company,
        'invoices': invoices,
        'form': form, # On passe le formulaire au template
        'is_collab': is_collab,
        'total_ht': sum(inv.amount_ht for inv in invoices) if not is_collab else None,
        'pending_count': invoices.filter(status='SENT').count(),
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def admin_portal(request):
    # On vérifie si l'utilisateur est un staff (pour la sécurité)
    if not request.user.is_staff:
        # Note : Pense à créer un fichier 403.html ou rediriger vers login
        return render(request, '403.html') 

    companies = Company.objects.all()
    total_invoices = Invoice.objects.count()
    
    context = {
        'companies': companies,
        'total_invoices': total_invoices,
    }
    return render(request, 'core/admin_portal.html', context)

@login_required
def add_company(request):
    # Sécurité : Seul l'expert peut ajouter des entreprises
    if not request.user.is_staff:
        raise PermissionDenied("Vous n'avez pas l'autorisation d'ajouter des entreprises.")

    if request.method == 'POST':
        name = request.POST.get('name')
        siret = request.POST.get('siret')
        
        # Validation basique
        if not name or not siret:
            messages.error(request, "Tous les champs sont obligatoires.")
            return redirect('admin_portal')
        
        if len(siret) != 14 or not siret.isdigit():
            messages.error(request, "Le SIRET doit contenir exactement 14 chiffres.")
            return redirect('admin_portal')
        
        try:
            company = Company.objects.create(name=name, siret=siret)
            messages.success(request, f"L'entreprise '{company.name}' a été ajoutée avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout : {str(e)}")
        
        return redirect('admin_portal')
    
    # Si c'est pas POST, rediriger vers le portail
    return redirect('admin_portal')

@login_required
def export_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Importer WeasyPrint seulement quand nécessaire
    try:
        from weasyprint import HTML
    except (ImportError, OSError) as e:
        error_msg = f"""
        PDF export unavailable: WeasyPrint library dependencies not installed.
        
        Error: {str(e)}
        
        WeasyPrint requires GTK+ system libraries that are not installed on this system.
        
        To fix this on macOS, install the required dependencies:
        
        1. Install Homebrew (if not already installed):
           /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        2. Install GTK+ and other dependencies:
           brew install gtk+3 cairo pango gdk-pixbuf libffi
        
        3. Set environment variables (add to your ~/.zshrc or ~/.bash_profile):
           export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
        
        4. Restart your terminal and Django server
        
        Alternative: Use a Docker container with WeasyPrint pre-installed.
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
        pdf_file = HTML(string=html_string).write_pdf()
        
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Facture_{invoice.number}.pdf"'
        return response
    except Exception as e:
        error_msg = f"""
        PDF export failed: {str(e)}
        
        WeasyPrint requires GTK+ system libraries that are not installed on this system.
        
        To fix this on macOS, install the required dependencies:
        
        1. Install Homebrew (if not already installed):
           /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        2. Install GTK+ and other dependencies:
           brew install gtk+3 cairo pango gdk-pixbuf libffi
        
        3. Set environment variables (add to your ~/.zshrc or ~/.bash_profile):
           export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
        
        4. Restart your terminal and Django server
        
        Alternative: Use a Docker container with WeasyPrint pre-installed.
        """
        return HttpResponse(error_msg, content_type='text/plain')

@login_required
def export_invoices_csv(request, company_id):
    # Sécurité : vérifier que l'utilisateur a accès à cette entreprise
    if not request.user.is_staff:
        profile = request.user.profile
        if profile.role != 'EXPERT' and profile.company.id != company_id:
            raise PermissionDenied("Vous n'avez pas l'autorisation d'accéder à ces données.")
    
    company = get_object_or_404(Company, id=company_id)
    invoices = Invoice.objects.filter(company=company).order_by('-date')
    
    # Création du fichier CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="export_factures_{company.name}_{company_id}.csv"'
    
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

@login_required
def add_gerant(request, company_id):
    """Créer un compte gérant pour une entreprise (réservé aux experts)"""
    company = get_object_or_404(Company, id=company_id)
    
    # SÉCURITÉ : Seul un expert (staff) peut ajouter un gérant
    if not request.user.is_staff:
        raise PermissionDenied("Vous n'avez pas l'autorisation de créer des comptes gérants.")

    if request.method == 'POST':
        user_form = UserCreationFormSimple(request.POST)
        if user_form.is_valid():
            # 1. Créer l'utilisateur
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            # 2. Mise à jour du profil (pour éviter l'IntegrityError)
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'company': company,
                    'role': 'GERANT'
                }
            )
            messages.success(request, f"Le compte gérant '{user.username}' a été créé pour l'entreprise '{company.name}'.")
            return redirect('admin_portal')
    else:
        user_form = UserCreationFormSimple()
        
    return render(request, 'core/add_user_form.html', {
        'form': user_form, 
        'company': company, 
        'role': 'Gérant'
    })

@login_required
def add_collaborator(request, company_id):
    """Créer un compte collaborateur pour une entreprise (réservé aux gérants)"""
    company = get_object_or_404(Company, id=company_id)
    
    # SÉCURITÉ : Seul le Gérant de CETTE entreprise peut ajouter un collaborateur
    if request.user.profile.role != 'GERANT' or request.user.profile.company.id != company.id:
        raise PermissionDenied("Vous n'avez pas l'autorisation de recruter pour cette entreprise.")

    if request.method == 'POST':
        user_form = UserCreationFormSimple(request.POST)
        if user_form.is_valid():
            # 1. Création de l'utilisateur
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            # 2. Mise à jour du profil (pour éviter l'IntegrityError)
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'company': company,
                    'role': 'COLLAB'
                }
            )
            messages.success(request, f"Le compte collaborateur '{user.username}' a été créé pour l'entreprise '{company.name}'.")
            return redirect('dashboard', company_id=company.id)
    else:
        user_form = UserCreationFormSimple()
        
    return render(request, 'core/add_user_form.html', {
        'form': user_form, 
        'company': company, 
        'role': 'Collaborateur'
    })