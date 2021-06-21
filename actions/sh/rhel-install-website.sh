#!/bin/bash
#
# Install static website from github

sudo su -

echo "Installing git..."
yum update -y
yum install -y git

echo "Cloning website..."
git clone https://github.com/jjbrassa/cb-tools.git /tmp/cb-tools

echo "Moving files to docroot..."
cp -R /tmp/cb-tools/app-samples/HTTP-App/* /var/www/html/.

echo "Cleaning up..."
rm -rf /tmp/cb-tools

echo "DONE!!"
