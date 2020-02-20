#!/bin/bash
#
# Quick bash-based example to install apache2 on a centOS instance
#
# Run pkg installers
yum update httpd
yum -y install httpd

# Start!
systemctl start httpd