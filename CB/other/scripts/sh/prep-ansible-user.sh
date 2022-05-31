#!/bin/bash
#
# Install Ansible server
USERNAME="ansible-user"
PASSWORD="CloudBolt4me!!"
ANSIBLE_USER_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCy8ZJpqD5DkMFP9PZBJO/egcIOlt4zswCW49QwAeDDGimJlb9FhnCMINBP5X9qNDkUuHQMu/0d0dbVUBDpxtTIFdcJYYiJAe7LWO/rbXxOYMSGMExP1SG0us2LrwrTH4q/4l9LswCtDTabaFt2WBRMkCve4w6xKJxinNCV8+4xGuqGnK25UBDTyfdj+myNRAFCYpQJRCCGkLco6142h3W7wb5V03DOZo7VYlzkYo9KPsDqjsLil2f5tJzPZX5fXFOFlWooze6hdsGA6PYtw/5Pt12wXNQ9p93VKElfjVbqE09QNJeATINP4tcdc80cbfZsXNlGdLIgy4lyO5zFLtbR ansible-user@ip-172-31-31-247.us-west-1.compute.internal"

echo "Building Ansible User..."
useradd -m ${USERNAME}

passwd ${USERNAME} << EOD
${PASSWORD}
${PASSWORD}
EOD

usermod --append --groups  wheel ${USERNAME}
touch /etc/sudoers.d/ansible-user
echo "ansible-user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/ansible-user

echo "Installing key..."
mkdir /home/ansible-user/.ssh
touch /home/ansible-user/.ssh/authorized_keys
chmod 700 /home/ansible-user/.ssh
chmod 640 /home/ansible-user/.ssh/authorized_keys
chown -R ansible-user: /home/ansible-user
echo "$ANSIBLE_USER_KEY" >> /home/ansible-user/.ssh/authorized_keys
