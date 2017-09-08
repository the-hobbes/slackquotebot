"""Tests for data.py"""

import data
import logging
import mock
import psycopg2
import settings
import unittest

from mock import MagicMock


class MockConnection():

  def execute(self, *args, **kwargs):
    return True

  def fetchone(self, *args, **kwargs):
    return ["I am a quote"]

  def close(self):
    return None

  def commit(self):
    return True


class TestData(unittest.TestCase):

  def setUp(self):
    logging.disable(logging.ERROR)  # suppress log output for tests
    psycopg2.connect = MockConnection()
    self.conn = psycopg2.connect
    settings.QUOTE_LIST = [1]

  def tearDown(self):
    self.conn = None

  def test_retrieve(self):
    expected_response = "I am a quote"
    data.connect = MagicMock(return_value=[self.conn, self.conn])
    received_response = data.retrieve()
    self.assertEqual(expected_response, received_response)

  def test_retrieve_fails(self):
    expected_response = -1
    data.connect = MagicMock(return_value=[self.conn, self.conn])
    self.conn.fetchone = MagicMock(side_effect=psycopg2.Error)
    received_response = data.retrieve()
    self.assertEqual(expected_response, received_response)
  
  def test_save(self):
    expected_response = 2
    data.connect = MagicMock(return_value=[self.conn, self.conn])
    data.prefetch_quote_ids = MagicMock()
    self.conn.fetchone = MagicMock(return_value=[2])
    received_response = data.save("I am a quote!")
    self.assertEqual(expected_response, received_response)

  def test_save_fails(self):
    expected_response = -1
    data.connect = MagicMock(return_value=[self.conn, self.conn])
    self.conn.fetchone = MagicMock(side_effect=psycopg2.Error)
    received_response = data.save("I am a quote!")
    self.assertEqual(expected_response, received_response)

  def test_delete(self):
    expected_response = True
    data.connect = MagicMock(return_value=[self.conn, self.conn])
    received_response = data.delete(1)
    self.assertEqual(expected_response, received_response)

  def test_delete_fails(self):
    expected_response = False
    data.connect = MagicMock(return_value=[self.conn, self.conn])
    self.conn.commit = MagicMock(side_effect=psycopg2.Error)
    received_response = data.delete(1)
    self.assertEqual(expected_response, received_response)

if __name__ == '__main__':
    unittest.main()
