#!/usr/bin/env python

import MySQLdb
import MySQLdb.cursors
import os
import shutil
import sys
import tempfile

from nose.tools import assert_equal, assert_true, assert_false

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

import mysql_util

class TestMySQLUtil():
  def setUp(self):
    self.db_info = mysql_util.get_db_info()
    self.db = MySQLdb.connect(host=self.db_info['host'], user=self.db_info['user'], \
        passwd=self.db_info['passwd'], unix_socket=self.db_info['socket'])
    self.cursor = self.db.cursor()
    if mysql_util.does_db_exist(self.db_info['db']):
      self.cursor.execute("DROP DATABASE " + self.db_info['db'])
    self.cursor.execute("CREATE DATABASE " + self.db_info['db'] + " DEFAULT CHARACTER SET 'utf8'")
    self.db.select_db(self.db_info['db'])
    self._create_test_tables()
    self.db.select_db(self.db_info['db'])

  def tearDown(self):
    self.cursor.execute("DROP DATABASE " + self.db_info['db'])
    mysql_util.close_db(self.db, self.cursor)

  def _create_test_tables(self):
    self.cursor.execute('CREATE TABLE foo (' +
        'id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, ' +
        'col1 VARCHAR(255), ' +
        'col2 INT(11))')

    self.cursor.execute('CREATE TABLE bar (' +
        'id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, ' +
        'field1 TEXT, ' +
        'field2 INT(10))')

  def test_does_db_exist(self):
    assert_equal(mysql_util.does_db_exist(self.db_info['db']), True)
    assert_equal(mysql_util.does_db_exist('37a_23yumaro208dlzj_sdlfkzqpo'), False)

  def test_does_table_exist(self):
    assert_equal(mysql_util.does_table_exist('foo'), True)
    assert_equal(mysql_util.does_table_exist('bar'), True)
    assert_equal(mysql_util.does_table_exist('not_exist_tb'), False)

  def test_get_tables(self):
    tables = mysql_util.get_tables()
    assert_equal(len(tables), 2)
    assert_true('foo' in tables)
    assert_true('bar' in tables)

  def test_backup_tables(self):
    tmp_backup_dir = tempfile.mkdtemp()
    mysql_util.backup_all_tables(tmp_backup_dir, is_archive=False)
    assert_true('foo.sql' in os.listdir(tmp_backup_dir))
    assert_true('bar.sql' in os.listdir(tmp_backup_dir))
    shutil.rmtree(tmp_backup_dir)

  def test_col_exist(self):
    assert_true(mysql_util.does_col_exist('foo', 'col1'))
    assert_true(mysql_util.does_col_exist('foo', 'col2'))
    assert_false(mysql_util.does_col_exist('foo', 'col3'))
    assert_true(mysql_util.does_col_exist('bar', 'field1'))
    assert_true(mysql_util.does_col_exist('bar', 'field2'))
    assert_false(mysql_util.does_col_exist('bar', 'field3'))

  def test_add_index(self):
    mysql_util.add_index('foo', 'col1', 'index')
    mysql_util.add_index('foo', 'col2', 'unique index')
    mysql_util.add_index('bar', 'field1', 'fulltext')

    self.cursor.execute("SHOW INDEX FROM foo where column_name = 'col1'")
    row = self.cursor.fetchone()
    assert_true(row is not None)
    non_unique = row[1]
    index_type = row[10]
    assert_equal(non_unique, 1)
    assert_equal(index_type, 'BTREE')

    self.cursor.execute("SHOW INDEX FROM foo where column_name = 'col2'")
    row = self.cursor.fetchone()
    assert_true(row is not None)
    non_unique = row[1]
    index_type = row[10]
    assert_equal(non_unique, 0)
    assert_equal(index_type, 'BTREE')

    self.cursor.execute("SHOW INDEX FROM bar where column_name = 'field1'")
    row = self.cursor.fetchone()
    assert_true(row is not None)
    non_unique = row[1]
    index_type = row[10]
    assert_equal(non_unique, 1)
    assert_equal(index_type, 'FULLTEXT')

  def test_drop_table(self):
    mysql_util.drop_table('bar')
    assert_equal(mysql_util.does_table_exist('bar'), False)

