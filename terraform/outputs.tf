# Outputs Terraform

output "web_instance_public_ip" {
  description = "IP publique de l'instance web"
  value       = aws_instance.web.public_ip
}

output "web_instance_id" {
  description = "ID de l'instance EC2 web"
  value       = aws_instance.web.id
}

output "ssh_command" {
  description = "Commande SSH pour se connecter à l'instance"
  value       = "ssh -i ${var.ssh_key_name}.pem ubuntu@${aws_instance.web.public_ip}"
}

output "application_url" {
  description = "URL de l'application"
  value       = "http://${aws_instance.web.public_ip}"
}

# Outputs commentés pour RDS et Load Balancer (optionnels)
# output "db_endpoint" {
#   description = "Endpoint de la base de données"
#   value       = aws_db_instance.postgres.endpoint
#   sensitive   = true
# }

# output "load_balancer_dns" {
#   description = "DNS du load balancer"
#   value       = aws_lb.web.dns_name
# }
