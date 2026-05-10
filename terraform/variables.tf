# Variables pour le déploiement AWS

variable "aws_region" {
  description = "Région AWS"
  type        = string
  default     = "eu-west-3"
}

variable "environment" {
  description = "Environnement (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Nom du projet"
  type        = string
  default     = "facturation-pme"
}

variable "ssh_key_name" {
  description = "Nom de la clé SSH AWS"
  type        = string
  default     = "facturation-pme-key"
}

variable "db_username" {
  description = "Nom d'utilisateur PostgreSQL"
  type        = string
  sensitive   = true
  default     = "facturationpme"
}

variable "db_password" {
  description = "Mot de passe PostgreSQL"
  type        = string
  sensitive   = true
}

variable "domain_name" {
  description = "Nom de domaine pour l'application"
  type        = string
  default     = "facturation-pme.com"
}
