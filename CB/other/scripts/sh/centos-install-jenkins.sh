#!/bin/bash
#
# Install jenkins!

myServer='{{server.ip}}'

echo "--------------------------------------------"
echo "| Installing jenkins..."
echo "--------------------------------------------"
yum install -y wget
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
yum upgrade -y
yum install -y epel-release java-11-openjdk-devel
yum install -y jenkins
systemctl daemon-reload

echo "--------------------------------------------"
echo "| Firing jenkins UP!..."
echo "--------------------------------------------"
systemctl start jenkins
systemctl status jenkins
systemctl enable jenkins

echo "--------------------------------------------"
echo "| Jenkins Details:"
echo "--------------------------------------------"
jenkinsBox="http://$myServer:8080"
echo "Your jenkins box [$jenkinsBox]"
curl $jenkinsBox
myInitPswd=$( cat /var/lib/jenkins/secrets/initialAdminPassword )
echo "Your initialAdminPassword [$myInitPswd]"