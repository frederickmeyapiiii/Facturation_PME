FROM ansible/ansible:latest

WORKDIR /ansible

RUN apt-get update && apt-get install -y \
    openssh-client \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY ansible /ansible

ENTRYPOINT ["ansible-playbook"]
