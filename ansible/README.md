# Utilisation d'Ansible sur Windows via Docker

## Solution 1 : Docker Compose (recommandé)

### Build l'image Ansible
```bash
cd ansible
docker compose build
```

### Exécuter le playbook
```bash
docker compose run ansible -i inventory.ini deploy.yml
```

Pour un test dry-run :
```bash
docker compose run ansible -i inventory.ini deploy.yml --check
```

---

## Solution 2 : WSL2 + Ubuntu (meilleure option à long terme)

1. Installer WSL2
2. Installer Ubuntu depuis le Microsoft Store
3. Dans Ubuntu WSL :
```bash
sudo apt-get update
sudo apt-get install ansible
cd /mnt/c/Users/frede/OneDrive\ -\ Ecole-IT/Bureau/Assistance\ Saas/ansible
ansible-playbook -i inventory.ini deploy.yml
```

---

## Solution 3 : Développement local avec Vagrant

Pour tester le playbook localement avant de le déployer en production :

### Prérequis
- Vagrant installé
- VirtualBox ou Hyper-V

### Étapes

1. Créer un `Vagrantfile` dans le dossier ansible :

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.network "private_network", ip: "192.168.33.10"
  
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3 python3-pip openssh-server
  SHELL
end
```

2. Lancer Vagrant :
```bash
vagrant up
```

3. Configurer l'inventaire pour Vagrant :
```ini
[web_servers]
default ansible_host=192.168.33.10 ansible_user=vagrant
```

4. Exécuter le playbook :
```bash
docker compose run ansible -i inventory.ini deploy.yml
```

---

## Prochaines étapes

1. Utiliser la solution Docker Compose pour valider le playbook
2. Une fois prêt, exécuter sur un serveur Ubuntu réel
3. Adapter `inventory.ini` avec l'IP du serveur de production
