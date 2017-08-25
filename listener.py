"""Create an event listener for the quotebot. 

  This module will perform the following actions:
  - wait for input on the slack channel directed at the bot
  - parse that input into commands
  - trigger handlers based on those commands
"""

import argparse
import quotebot
import time
from slackclient import SlackClient

# Set constants
READ_WEBSOCKET_DELAY = 1 # 1 second delay between sampling the firehose
COMMANDS = ['!quote', '!addquote', '!deletequote']


def handle_command(command, channel):
  """Receives commands directed at the bot and takes the appropriate action.

    The actual work of executing the command is performed by the business logic 
    layer of the quotebot. This function chooses the right portion of that logic
    to execute. 

    Arguments:
      - command (string) the command to perform
      - channel (string) the channel to send the response 

    The responses constructed by the quotebot layer are sent to the appropriate
    slack channel.
  """
  print(command, channel)


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


def parse_arguments():
  """Pull the bot token from the command line.

    Returns:
    - slack_bot_token (string) the bot api access token
 """
  parser = argparse.ArgumentParser(
    description='listen for bot commands on slack')
  parser.add_argument(
    '--slack_bot_token', type=str, help='the Token of the slack chatbot')
  args = parser.parse_args()
  slack_bot_token = args.slack_bot_token
  if not slack_bot_token:
    parser.error('Slack Bot Token not given')

  return slack_bot_token


def main():
  slack_bot_token = parse_arguments()
  slack_client = SlackClient(slack_bot_token)
  if slack_client.rtm_connect():
    print("Quotebot is connected and running.")
    # infinite loop to continuously consume slack data from rtm api
    while True:
      command, channel = parse_slack_input(slack_client.rtm_read())
      if command and channel:
        handle_command(command, channel)
      time.sleep(READ_WEBSOCKET_DELAY)
  else:
    print("Connection failed. Invalid Slack token or bot ID?")


if __name__ == "__main__":
  main()
  