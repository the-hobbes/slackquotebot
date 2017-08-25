"""Tests for listener.py"""

import listener
import unittest

class TestListener(unittest.TestCase):

  def setUp(self):
    pass

  def test_handle_command(self):
    pass

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
