# Terraform configuration pour provisionner l'infrastructure cloud
# Provider: AWS (configurable pour Azure, GCP, etc.)

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  # Backend S3 pour le state (commenté pour le premier déploiement)
  # backend "s3" {
  #   bucket         = "facturation-pme-terraform-state"
  #   key            = "terraform.tfstate"
  #   region         = "eu-west-3"
  #   encrypt        = true
  #   dynamodb_table = "facturation-pme-terraform-locks"
  # }
}

provider "aws" {
  region = var.aws_region
}

# Data source pour trouver le dernier AMI Ubuntu 22.04 LTS
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Réseau VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.project_name}-vpc-${var.environment}"
    Environment = var.environment
  }
}

# Subnet public
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name        = "${var.project_name}-public-subnet-${var.environment}"
    Environment = var.environment
  }
}

# Subnet privé (optionnel pour RDS - commenté pour simplifier)
# resource "aws_subnet" "private" {
#   vpc_id            = aws_vpc.main.id
#   cidr_block        = "10.0.2.0/24"
#   availability_zone = "${var.aws_region}a"
# 
#   tags = {
#     Name        = "${var.project_name}-private-subnet-${var.environment}"
#     Environment = var.environment
#   }
# }

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "${var.project_name}-igw-${var.environment}"
    Environment = var.environment
  }
}

# Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name        = "${var.project_name}-public-rt-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Security Group pour l'application web
resource "aws_security_group" "web" {
  name_prefix = "${var.project_name}-web-${var.environment}"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-web-sg-${var.environment}"
    Environment = var.environment
  }
}

# Security Group pour PostgreSQL (optionnel pour RDS)
# Commenté car on utilise PostgreSQL dans Docker pour simplifier
# resource "aws_security_group" "database" {
#   name_prefix = "${var.project_name}-db-${var.environment}"
#   vpc_id      = aws_vpc.main.id
# 
#   ingress {
#     from_port       = 5432
#     to_port         = 5432
#     protocol        = "tcp"
#     security_groups = [aws_security_group.web.id]
#   }
# 
#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# 
#   tags = {
#     Name        = "${var.project_name}-db-sg-${var.environment}"
#     Environment = var.environment
#   }
# }

# Instance EC2 pour l'application web
resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]
  key_name               = var.ssh_key_name
  user_data              = file("${path.module}/user_data.sh")

  tags = {
    Name        = "${var.project_name}-web-${var.environment}"
    Environment = var.environment
  }
}

# Instance RDS PostgreSQL (optionnel - commenté pour utiliser PostgreSQL dans Docker)
# Décommentez pour une base de données managée en production
# resource "aws_db_instance" "postgres" {
#   identifier             = "${var.project_name}-db-${var.environment}"
#   engine                 = "postgres"
#   engine_version         = "15.4"
#   instance_class         = var.environment == "prod" ? "db.t3.medium" : "db.t3.micro"
#   allocated_storage      = var.environment == "prod" ? 100 : 20
#   storage_type           = "gp2"
#   db_name                = "facturationpme"
#   username               = var.db_username
#   password               = var.db_password
#   db_subnet_group_name   = aws_db_subnet_group.main.name
#   vpc_security_group_ids = [aws_security_group.database.id]
#   skip_final_snapshot    = var.environment == "dev" ? true : false
#   final_snapshot_identifier = var.environment == "prod" ? "${var.project_name}-final-snapshot" : null
# 
#   tags = {
#     Name        = "${var.project_name}-rds-${var.environment}"
#     Environment = var.environment
#   }
# }

# DB Subnet Group (optionnel pour RDS)
# resource "aws_db_subnet_group" "main" {
#   name       = "${var.project_name}-db-subnet-group-${var.environment}"
#   subnet_ids = [aws_subnet.private.id]
# 
#   tags = {
#     Name        = "${var.project_name}-db-subnet-group-${var.environment}"
#     Environment = var.environment
#   }
# }

# Load Balancer (optionnel pour scaling horizontal)
# Commenté pour simplifier le déploiement initial
# resource "aws_lb" "web" {
#   name               = "${var.project_name}-lb-${var.environment}"
#   internal           = false
#   load_balancer_type = "application"
#   security_groups    = [aws_security_group.web.id]
#   subnets            = [aws_subnet.public.id]
# 
#   tags = {
#     Name        = "${var.project_name}-lb-${var.environment}"
#     Environment = var.environment
#   }
# }

# Outputs sont définis dans outputs.tf
