import MySQLdb
import MySQLdb.cursors

def init_db(charset='utf8', create_if_not_exist=False):
  db_info = get_db_info()
  db = MySQLdb.connect(host=db_info['host'], user=db_info['user'], \
      passwd=db_info['passwd'], unix_socket=db_info['socket'])
  cursor = db.cursor()
  if not does_db_exist(db_info['db']):
    if create_if_not_exist:
      cursor.execute("CREATE DATABASE " + db_info['db'] + " DEFAULT CHARACTER SET " + charset)
    else:
      close_db(db, cursor)
      raise Exception('Database ' + db_info['db'] + ' does not exist')
  db.select_db(db_info['db'])

  db.set_character_set(charset)
  cursor.execute('SET NAMES ' + charset + ';')
  cursor.execute('SET CHARACTER SET ' + charset + ';')
  cursor.execute('SET character_set_connection=' + charset + ';')
  return db, cursor

def close_db(db, cursor):
  cursor.close()
  db.close()

def _is_this_a_setting_line(line):
  line = line.strip()
  if line == '':
    return False
  if line[0] == '#':
    return False
  return True

def get_db_info():
  db_info = { }
  f = open('settings/mysql_settings', 'r')
  for line in f:
    if not _is_this_a_setting_line(line):
      continue
    field, val = line.strip().split(':')
    field = field.strip()
    val = val.strip()
    if (val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'"):
      val = val[1:-1]
    db_info[field] = val
  f.close()
  return db_info

def does_db_exist(db_name):
  db_info = get_db_info()
  db = MySQLdb.connect(host=db_info['host'], user=db_info['user'], \
      passwd=db_info['passwd'], unix_socket=db_info['socket'])
  cursor = db.cursor()

  cursor.execute("""SELECT schema_name FROM information_schema.schemata """ + \
     """WHERE schema_name = %s""", (db_name))
  row = cursor.fetchone()

  cursor.close()
  db.close()
  return row != None

def does_tbl_exist(table_name):
  db_info = get_db_info()
  db, cursor = init_db()
  cursor.execute("""SELECT * FROM information_schema.tables """ + \
      """WHERE table_schema = %s AND table_name = %s""", (db_info['db'], table_name))
  row = cursor.fetchone()
  close_db(db, cursor)
  return row != None

def drop_tbl(table_name):
  db, cursor = init_db()
  if does_tbl_exist(table_name):
    cursor.execute("""DROP TABLE """ + table_name)
  close_db(db, cursor)


