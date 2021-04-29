#!/bin/bash

dbname='{{server.database_name}}'
dbuser='{{server.database_username}}'
dbpass='{{server.database_password}}'
dbhost='{{blueprint_context.wordpress_database.server.ip}}'

echo "WordPress Install Script"
echo "============================================"
echo "| dbname - $dbname"
echo "| dbuser - $dbuser"
echo "| dbpass - $dbpass"
echo "| dbhost - $dbhost"
echo "============================================"

# wordpress prereqs
apt install -y apache2 php libapache2-mod-php php-opcache php-cli php-gd php-curl php-mysql

# download wordpress
curl -O https://wordpress.org/latest.tar.gz
# unzip wordpress
tar -zxf latest.tar.gz
# change dir to wordpress
cd wordpress

#create wp config
cp wp-config-sample.php wp-config.php
#set database details with perl find and replace
perl -pi -e "s/database_name_here/$dbname/g" wp-config.php
perl -pi -e "s/username_here/$dbuser/g" wp-config.php
perl -pi -e "s/password_here/$dbpass/g" wp-config.php
perl -pi -e "s/localhost/$dbhost/g" wp-config.php

#set WP salts
perl -i -pe'
  BEGIN {
    @chars = ("a" .. "z", "A" .. "Z", 0 .. 9);
    push @chars, split //, "!@#$%^&*()-_ []{}<>~\`+=,.;:/?|";
    sub salt { join "", map $chars[ rand @chars ], 1 .. 64 }
  }
  s/put your unique phrase here/salt()/ge' wp-config.php

#create uploads folder and set permissions
mkdir -p wp-content/uploads
chmod 775 wp-content/uploads

echo "Copying WordPress files to /var/www/html..."
cp -r ~/wordpress/* /var/www/html
systemctl restart apache2

echo "Cleaning..."
rm ../latest.tar.gz

echo "========================="
echo "Installation is complete."
echo "========================="