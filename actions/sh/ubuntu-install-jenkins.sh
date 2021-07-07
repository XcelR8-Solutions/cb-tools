#!/bin/bash
#
# Install jenkins!

myServer='{{server.ip}}'

echo "Installing java..."
apt update 
apt install -y openjdk-8-jdk openjdk-8-jre
cat >> /etc/environment <<EOL
JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
JRE_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre
EOL

echo "Installing jenkins..."
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
apt update
apt install -y jenkins

echo "Firing jenkins UP!..."
systemctl start jenkins
systemctl status jenkins

echo "Your jenkins box [http://$myServer:8080]"
myInitPswd=$( cat /var/lib/jenkins/secrets/initialAdminPassword )
echo "Your initialAdminPassword [$myInitPswd]"