# getlkdcontacts
Find contacts at a company using BS4 and selenium with Firefox

# Description
Python script to get name, surname and position based of a Company name. The output is stored into a Database.

# Requirements
Tested on Debian 9 64bits and python 3.4+

# Installation
./setup.sh

Default path: /opt/osint/getldkcontacts/

# Database configuration
Edit /opt/osint/getldkcontacts/lib/python/site-package/database_osint.py and set you own Database information.

The default parameters will work but we suggest you to use another user/pass data.

# Examples of use:
 
    /opt/osint/getldkcontacts/bin/python  getlkdcontacts.py 'my company'

    /opt/osint/getldkcontacts/bin/python getlkdcontacts.py 'my company' -n 10 -s 0 -i 10 -la en -p http://127.0.0.1:8080

    /opt/osint/getldkcontacts/bin/python getlkdcontacts.py 'my company' -n 400 -s 0 -i 100
