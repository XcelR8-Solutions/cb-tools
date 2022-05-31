#!/bin/bash
#
# Install Ansible server
USERNAME="ansible-user"
PASSWORD="CloudBolt4me!!"

echo "Installing Ansible..."
yum install -y epel-release
yum install -y ansible

echo "Building Ansible User..."
useradd -m ${USERNAME}

passwd ${USERNAME} << EOD
${PASSWORD}
${PASSWORD}
EOD

usermod --append --groups  wheel ${USERNAME}