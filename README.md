mysql_utils
==============

Providing commonly used MySQL utilities.

Required library
----------------
1. MySQL-Python: http://mysql-python.sourceforge.net/

Usage
-----
Renaming settings/mysql_settings.sample to settings/mysql_settings, and set the
fields to the correct values.  A typical mysql_settings file may look like this:

host: "localhost"<br>
user: "root"<br>
passwd: "password-of-root"<br>
socket: "/var/lib/mysql/mysql.sock"<br>
db: "database_name"

TODO
----
1. Add the testing files

2. Add a function to backup all tables in the given database
