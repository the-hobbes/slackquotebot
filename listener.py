"""Create an event listener for the quotebot. 

  This module will perform the following actions:
  - wait for input on the slack channel directed at the bot
  - parse that input into commands
  - trigger handlers based on those commands
"""

import quotebot
import settings
import time
from ConfigParser import SafeConfigParser
from slackclient import SlackClient

# Set constants
READ_WEBSOCKET_DELAY = 1 # 1 second delay between sampling the firehose
COMMANDS = ['!addquote', '!deletequote', '!quote']


def write_response(response, channel, slack_client):
  """Write responses back to the chat channel.

    Arguments:
    - response (string) the response to write
    - channel (string) the id of the channel to write to
    - slack_client (SlackClient) the client to perform the call
  """
  slack_client.api_call(
    'chat.postMessage', channel=channel, text=response, as_user=True)


def handle_command(command):
  """Receives commands directed at the bot and takes the appropriate action.

    The actual work of executing the command is performed by the business logic 
    layer of the quotebot. This function chooses the right portion of that logic
    to execute. 

    Arguments:
      - command (string) the command to perform
    Returns:
      - response (string) the response to write to the channel
  """
  cmd_list = command.split(' ', 1)
  cmd = cmd_list[0]

  if cmd == '!addquote':
    if len(cmd_list) <= 1:
      return "gimme a quote to add"
    response = quotebot.add_quote(cmd_list[1])
  elif cmd == '!deletequote':
    if len(cmd_list) <= 1:
      return "gimme a quote number to delete"
    response = quotebot.remove_quote(cmd_list[1])
  elif cmd == '!quote':
    if len(cmd_list) != 1:  # TODO: test this
      return "I don't understand that stuff after '!quote'"
    response = quotebot.retrieve_random_quote()
  else:
    response = quotebot.command_not_found(cmd)

  return response


def parse_slack_input(slack_rtm_output):
  """Decides if a message has been directed at the bot.

    Takes the firehose of information from the Slack Real Time Messaging API and
    determines if a command has been entered.

    Arguments:
      - slack_rtm_input (list) the result of calling rtm_read() from a slack
        client, which reads from the RTM websocket and creates a json array for
        each response.

    Returns:
    - command (string) the command directed at the bot
    - channel (string) the channel the command originated from
 """
  output_list = slack_rtm_output
  if output_list and len(output_list) > 0:
    for output in output_list:
      if ('text' in output 
          and any(output['text'].startswith(cmd) for cmd in COMMANDS)):
        return output['text'], output['channel']

  return None, None


def parse_config():
  """Parses a config file containing connection secrets."""
  parser = SafeConfigParser()
  parser.read("secrets")

  settings.SECRETS['slack_bot_token'] = parser.get(
    "slack_credentials", "bot_api_access_token")
  settings.SECRETS['dbname'] = parser.get(
    "db_credentials", "dbname")
  settings.SECRETS['user'] = parser.get(
    "db_credentials", "role_account")
  settings.SECRETS['password'] = parser.get(
    "db_credentials", "password")


def main():
  settings.init()
  parse_config()
  slack_client = SlackClient(settings.SECRETS['slack_bot_token'])
  if slack_client.rtm_connect():
    print("Quotebot is connected and running.")
    # infinite loop to continuously consume slack data from rtm api
    while True:
      command, channel = parse_slack_input(slack_client.rtm_read())
      if command and channel:
        response = handle_command(command)
        write_response(response, channel, slack_client)
      time.sleep(READ_WEBSOCKET_DELAY)
  else:
    print("Connection failed. Invalid Slack token or bot ID?")


if __name__ == "__main__":
  main()
  