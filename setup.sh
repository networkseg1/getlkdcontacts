#!/bin/bash

debian_initialize() {
sc=$(readlink -f "$0")
scriptpath=$(dirname "$sc")
INSTALL_PATH="/opt/osint/getldkcontacts"
apt-get -qq update 
}

install_packages() {
echo "****************************************************"
echo "Installing packages................................."
echo "****************************************************"
apt-get update
apt-get -y install mariadb-server 
apt-get -y install build-essential libssl-dev libffi-dev python-dev
apt-get -y install python3
apt-get -y install python3-pip
apt-get -y install python3-venv
apt-get -y install xvfb
apt-get -y install xauth
apt-get -y install firefox-esr
echo "   "
}

hardening_mysql_DB_system() {
echo "****************************************************"
echo "MySQL Secure Installation .........................."
echo "****************************************************"
/etc/init.d/mysql restart
mysql_secure_installation
echo "     "
echo "setting up mysql directory permissions:"
chown -R root:root /etc/mysql/
chmod 0644 /etc/mysql/my.cnf
echo "     "
echo "setting up mysql DB storage directory permissions:"
echo "     "
echo "setup mysql user shell:"
usermod -s /bin/false mysql > /dev/null 2>&1
}

run_sql_script() {
echo "***********************************"
echo "Creating OSINT DB...............   "
echo "***********************************"
echo "running DBldcontacts.sql script....... Intro your root DB password"
mysql -h "localhost" -u "root" "-p" < "./DBldcontacts.sql"
}


create_python_env() {
echo "**********************************************"
echo "Creating python3 virtual environment.......   "
echo "**********************************************"
mkdir -p $INSTALL_PATH
python3 -m venv $INSTALL_PATH
}

setup_tool() {
echo "**********************************************"
echo "Installing application and dependencies......."
echo "**********************************************"
cp $scriptpath/requirements.txt $INSTALL_PATH
cp $scriptpath/getlkdcontacts.py $INSTALL_PATH
cp $scriptpath/database_osint.py $INSTALL_PATH/lib/python*/site-packages/

# Selenium 
# Firefox-esr 52.5.0 requires (<=) geckodriver-v0.18.0
if [ $(uname -m) == 'x86_64' ]; then
  archi=64
else
  archi=32
fi
cd /tmp
wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux${archi}.tar.gz
tar xzvf geckodriver-v0.18.0-linux${archi}.tar.gz
cp /tmp/geckodriver /usr/sbin/
cp /tmp/geckodriver /usr/local/bin/
rm /tmp/geckodriver

cd $INSTALL_PATH
./bin/pip3 install -r ./requirements.txt > /dev/null 2>&1
}

debian_initialize;
install_packages;
hardening_mysql_DB_system;
run_sql_script;
create_python_env;
setup_tool;

