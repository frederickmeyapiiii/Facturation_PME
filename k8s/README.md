# Déploiement Kubernetes pour Facturation PME

## Prérequis
- Docker
- kubectl
- Minikube (ou cluster K8s)

## Installation Minikube (Windows)
1. Télécharge Minikube : https://minikube.sigs.k8s.io/docs/start/
2. Installe kubectl : https://kubernetes.io/docs/tasks/tools/
3. Démarre Minikube :
   ```bash
   minikube start
   ```

## Déploiement
1. Build l'image Docker :
   ```bash
   docker build -t assistancesaas-web:latest .
   ```

2. Charge l'image dans Minikube :
   ```bash
   minikube image load assistancesaas-web:latest
   ```

3. Applique les manifests :
   ```bash
   kubectl apply -f k8s/
   ```

4. Vérifie :
   ```bash
   kubectl get pods
   kubectl get services
   ```

5. Accède à l'app :
   ```bash
   minikube service facturation-web
   ```

## Architecture
- **DB** : PostgreSQL avec PVC
- **Web** : Django app
- **Config** : Variables d'env via ConfigMap

## Nettoyage
```bash
kubectl delete -f k8s/
minikube stop
```