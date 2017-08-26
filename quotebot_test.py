"""Tests for quotebot.py"""

import data
import quotebot
import unittest
from mock import MagicMock

class TestQuotebot(unittest.TestCase):

  def test_add_quote(self):
    expected_response = "Quote 123 saved"
    data.save = MagicMock(return_value=123)
    received_response = quotebot.add_quote("Some quote")
    self.assertEqual(expected_response, received_response)

  def test_add_quote_failure(self):
    expected_response = "There was an error saving the quote"
    data.save = MagicMock(return_value=-1)
    received_response = quotebot.add_quote("Some quote")
    self.assertEqual(expected_response, received_response)

  def test_retrieve_random_quote(self):
    expected_response = "Here's a quote!"
    data.retrieve = MagicMock(return_value=expected_response)
    received_response = quotebot.retrieve_random_quote()
    self.assertEqual(expected_response, received_response)

  def test_remove_quote_quote(self):
    expected_response = "Quote 123 successfully removed"
    data.delete = MagicMock(return_value=True)
    received_response = quotebot.remove_quote(123)
    self.assertEqual(expected_response, received_response)

  def test_remove_quote_quote_failure(self):
    expected_response = "There was an error deleting quote 123"
    data.delete = MagicMock(return_value=False)
    received_response = quotebot.remove_quote(123)
    self.assertEqual(expected_response, received_response)


if __name__ == '__main__':
    unittest.main()
