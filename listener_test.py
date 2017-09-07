"""Tests for listener.py"""

import listener
import quotebot
import unittest
from mock import MagicMock


class TestListener(unittest.TestCase):

  def test_handle_addquote(self):
    expected_response = "quote added"
    quotebot.add_quote = MagicMock(return_value=expected_response)
    fake_command = "!addquote add this quote"
    received_response = listener.handle_command(fake_command)
    self.assertEqual(expected_response, received_response)

  def test_handle_addquote_fails(self):
    expected_response = "gimme a quote to add"
    quotebot.add_quote = MagicMock(return_value=expected_response)
    fake_command = "!addquote"
    received_response = listener.handle_command(fake_command)
    self.assertEqual(expected_response, received_response)

  def test_handle_deletequote(self):
    expected_response = "quote deleted"
    quotebot.remove_quote = MagicMock(return_value=expected_response)
    fake_command = "!deletequote 12"
    received_response = listener.handle_command(fake_command)
    self.assertEqual(expected_response, received_response)

  def test_handle_deletequote_fails(self):
    expected_response = "gimme a quote number to delete"
    fake_command = "!deletequote"
    received_response = listener.handle_command(fake_command)
    self.assertEqual(expected_response, received_response)

  def test_handle_deletequote_fails_non_integer(self):
    expected_response = "gimme an actual quote number to delete"
    fake_command = "!deletequote 12.1"
    received_response = listener.handle_command(fake_command)
    self.assertEqual(expected_response, received_response)

  def test_handle_getquote(self):
    expected_response = "quote retrieved"
    quotebot.retrieve_random_quote = MagicMock(return_value=expected_response)
    fake_command = "!quote"
    received_response = listener.handle_command(fake_command)
    self.assertEqual(expected_response, received_response)

  def test_handle_getquote_fails(self):
    expected_response = "I don't understand that stuff after '!quote'"
    fake_command = "!quote blahblah"
    received_response = listener.handle_command(fake_command)
    self.assertEqual(expected_response, received_response)

  def test_handle_bad_command(self):
    expected_response = "Command !iwontwork not found"
    fake_command = "!iwontwork"
    received_response = listener.handle_command(fake_command)
    self.assertEqual(expected_response, received_response)

  def test_parse_slack_input(self):
    fake_input = [{
    u'source_team': u'SOMETEAM', u'text': u'!quote blah blah',
    u'ts': u'1503633307.000114', u'user': u'SOMEUSER', u'team': u'SOMETEAM',
    u'type': u'message', u'channel': u'SOMECHANNEL'}]
    expected_command, expected_channel = u'!quote blah blah', u'SOMECHANNEL'
    received_command, received_channel = listener.parse_slack_input(fake_input)
    self.assertEqual(expected_command, received_command)
    self.assertEqual(expected_channel, received_channel)

  def test_parse_slack_input_no_command(self):
    fake_input = [{
    u'source_team': u'SOMETEAM', u'text': u'blah !quote blah',
    u'ts': u'1503633307.000114', u'user': u'SOMEUSER', u'team': u'SOMETEAM',
    u'type': u'message', u'channel': u'SOMECHANNEL'}]
    expected_command, expected_channel = None, None
    received_command, received_channel = listener.parse_slack_input(fake_input)
    self.assertEqual(expected_command, received_command)
    self.assertEqual(expected_channel, received_channel)


if __name__ == '__main__':
    unittest.main()
