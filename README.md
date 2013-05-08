mysql_utils
==============

Providing commonly used MySQL utilities.

Contact
-------
Hung-Hsuan Chen (hhchen@psu.edu)

Required library
----------------
<ol>
  <li>MySQL-Python: http://mysql-python.sourceforge.net/</li>
</ol>

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
<ol>
  <li>Backup all tables in the given database</li>
  <li>Add index to a certain column of a table</li>
<ol>
