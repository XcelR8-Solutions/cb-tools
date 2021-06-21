#!/bin/bash
#
# Install apache (RHEL/CentOS)

sudo su -

echo "Installing apache..."
yum update -y
yum install -y httpd

echo "Configuring apache..."
firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --reload
systemctl enable --now httpd
