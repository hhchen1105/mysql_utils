#!/usr/bin/env python

import MySQLdb
import MySQLdb.cursors
import os
import sys

from nose.tools import assert_equal

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

  def test_does_tbl_exist(self):
    assert_equal(mysql_util.does_tbl_exist('foo'), True)
    assert_equal(mysql_util.does_tbl_exist('bar'), True)
    assert_equal(mysql_util.does_tbl_exist('not_exist_tb'), False)

  def test_drop_tbl(self):
    mysql_util.drop_tbl('bar')
    assert_equal(mysql_util.does_tbl_exist('bar'), False)


