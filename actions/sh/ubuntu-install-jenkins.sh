#!/bin/bash
#
# Install jenkins!

myServer='{{server.ip}}'

killall apt apt-get

echo "--------------------------------------------"
echo "| Installing java..."
echo "--------------------------------------------"
apt install -y openjdk-8-jdk openjdk-8-jre
cat >> /etc/environment <<EOL
JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
JRE_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre
EOL
source /etc/environment

echo "--------------------------------------------"
echo "| Installing jenkins..."
echo "--------------------------------------------"
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
apt install -y jenkins

echo "--------------------------------------------"
echo "| Firing jenkins UP!..."
echo "--------------------------------------------"
systemctl start jenkins
systemctl status jenkins
echo "--------------------------------------------"
echo "| Jenkins Details:"
echo "--------------------------------------------"
echo "Your jenkins box [http://$myServer:8080]"
myInitPswd=$( cat /var/lib/jenkins/secrets/initialAdminPassword )
echo "Your initialAdminPassword [$myInitPswd]"