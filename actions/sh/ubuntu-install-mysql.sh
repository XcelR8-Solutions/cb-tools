#!/bin/bash

dbname='{{server.database_name}}'
dbuser='{{server.database_username}}'
dbpass='{{server.database_password}}'
wphost='{{blueprint_context.wordpress_server.server.ip}}'

echo "Installing mysql server"
echo "============================================"
echo " -> | dbname - $dbname"
echo " -> | dbuser - $dbuser"
echo " -> | dbpass - $dbpass"
echo " -> | wphost - $wphost"
echo "============================================"
apt install -y mysql-server

echo " -> Starting mysql server (if not already started)"
systemctl start mysql.service

echo " -> Creating database with the name '$dbname'..."
mysql -u root <<-EOSQL
  CREATE DATABASE $dbname;
  CREATE USER '${dbuser}'@'localhost' IDENTIFIED BY '${dbpass}';
  GRANT ALL PRIVILEGES ON $dbname.* TO '${dbuser}'@'${wphost}';
  FLUSH PRIVILEGES;
EOSQL

# allow login from wordpress server
#cat <<EOF >> /etc/my.cnf
#[mysqld]
#bind-address=0.0.0.0
#EOF

echo " -> MySQL server installation completed."
