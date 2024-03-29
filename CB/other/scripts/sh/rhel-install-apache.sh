#!/bin/bash
#
# Install apache (RHEL/CentOS)

echo "Installing apache..."
yum install -y httpd

echo "Configuring apache..."
firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --reload
systemctl enable --now httpd
