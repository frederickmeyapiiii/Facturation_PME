#!/bin/bash

# Script d'aide pour l'initialisation AWS
# Ce script guide l'utilisateur à travers la configuration initiale

set -e

echo "🚀 Configuration initiale pour le déploiement AWS"
echo "============================================"
echo ""

# Vérification de Terraform
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform n'est pas installé."
    echo "📦 Installation de Terraform..."
    
    # Détection de l'OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
        echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
        sudo apt update && sudo apt install terraform
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew tap hashicorp/tap
        brew install hashicorp/tap/terraform
    else
        echo "❌ OS non supporté. Installez Terraform manuellement depuis https://terraform.io/downloads"
        exit 1
    fi
    
    echo "✅ Terraform installé avec succès"
else
    echo "✅ Terraform est déjà installé (version: $(terraform --version | cut -d' ' -f2))"
fi

# Vérification de AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI n'est pas installé."
    echo "📦 Installation de AWS CLI..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        sudo unzip awscliv2.zip
        sudo ./aws/install
        rm awscliv2.zip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install awscli
    else
        echo "❌ OS non supporté. Installez AWS CLI manuellement depuis https://aws.amazon.com/cli/"
        exit 1
    fi
    
    echo "✅ AWS CLI installé avec succès"
else
    echo "✅ AWS CLI est déjà installé (version: $(aws --version | cut -d' ' -f2))"
fi

# Configuration des credentials AWS
echo ""
echo "🔑 Configuration des credentials AWS..."
echo "Veuillez entrer vos credentials AWS (disponibles dans la console AWS IAM)"
echo ""

read -p "AWS Access Key ID: " AWS_ACCESS_KEY_ID
read -sp "AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
echo ""
read -p "AWS Region (par défaut: eu-west-3): " AWS_REGION
AWS_REGION=${AWS_REGION:-eu-west-3}

# Création du répertoire .aws
mkdir -p ~/.aws

# Écriture des credentials
cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = $AWS_ACCESS_KEY_ID
aws_secret_access_key = $AWS_SECRET_ACCESS_KEY
EOF

# Écriture de la configuration
cat > ~/.aws/config << EOF
[default]
region = $AWS_REGION
output = json
EOF

echo "✅ Credentials AWS configurés"

# Vérification des credentials
echo ""
echo "🔍 Vérification des credentials AWS..."
if aws sts get-caller-identity &> /dev/null; then
    echo "✅ Credentials AWS valides"
    aws sts get-caller-identity
else
    echo "❌ Credentials AWS invalides. Veuillez vérifier vos credentials."
    exit 1
fi

# Vérification de la clé SSH
echo ""
echo "🔑 Vérification de la clé SSH..."
SSH_KEY_NAME="facturation-pme-key"
SSH_KEY_FILE="$SSH_KEY_NAME.pem"

if [ -f "$SSH_KEY_FILE" ]; then
    echo "✅ Clé SSH trouvée: $SSH_KEY_FILE"
else
    echo "⚠️  Clé SSH non trouvée: $SSH_KEY_FILE"
    echo "📝 Instructions pour créer une clé SSH:"
    echo "   1. Allez dans la console AWS EC2 > Key Pairs"
    echo "   2. Cliquez sur 'Create Key Pair'"
    echo "   3. Nommez-la '$SSH_KEY_NAME'"
    echo "   4. Téléchargez le fichier .pem"
    echo "   5. Déplacez-le dans le dossier terraform:"
    echo "      mv ~/Downloads/$SSH_KEY_FILE ."
    echo "   6. Changez les permissions:"
    echo "      chmod 400 $SSH_KEY_FILE"
fi

# Initialisation Terraform
echo ""
echo "🏗️  Initialisation de Terraform..."
terraform init

# Validation de la configuration
echo ""
echo "🔍 Validation de la configuration Terraform..."
if terraform validate; then
    echo "✅ Configuration Terraform valide"
else
    echo "❌ Configuration Terraform invalide"
    exit 1
fi

# Plan Terraform
echo ""
echo "📋 Plan Terraform (dry-run)..."
terraform plan -out=tfplan

echo ""
echo "✅ Configuration terminée avec succès !"
echo ""
echo "🚀 Prochaines étapes:"
echo "   1. Vérifiez le plan Terraform ci-dessus"
echo "   2. Si tout est correct, appliquez l'infrastructure:"
echo "      terraform apply tfplan"
echo "   3. Une fois l'instance créée, déployez l'application:"
echo "      ./deploy.sh <IP_PUBLIQUE> $SSH_KEY_FILE"
echo ""
echo "📚 Pour plus d'informations, consultez le README.md"
