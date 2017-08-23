"""Create an event listener for the quotebot. 

  This module will perform the following actions:
  - wait for input on the slack channel directed at the bot
  - parse that input into commands
  - trigger handlers based on those commands
"""

# TODO: import necessary slack client libraries
# TODO: declare necessary constants
import argparse
from slackclient import SlackClient

# Pull the bot id and bot token from command line arguments
parser = argparse.ArgumentParser(description='listen for bot commands on slack')
parser.add_argument('--bot_id', type=str, help='the ID of the slack chatbot')
parser.add_argument(
  '--slack_bot_token', type=str, help='the Token of the slack chatbot')
args = parser.parse_args()

# Set constants
BOT_ID = args.bot_id
SLACK_BOT_TOKEN = args.slack_bot_token
READ_WEBSOCKET_DELAY = 1 # 1 second delay between sampling the firehose

# Raise an error if a required flag isn't set
if not BOT_ID:
  parser.error('Bot ID not given')
if not SLACK_BOT_TOKEN:
  parser.error('Slack Bot Token not given')


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
  pass


def parse_slack_input():
  """Decides if a message has been directed at the bot.

    Takes the firehose of information from the Slack Real Time Messaging API and
    determines if a command has been directed at the quotebot. The command is 
    then sent to the handle_command function to be properly handled.

    Arguments:
      - slack_rtm_input (list) the result of calling rtm_read() from a slack
        client, which reads from the RTM websocket and creates a json array for
        each response.

    Returns:
    - command (string) the command directed at the bot
    - channel (string) the channel the command originated from
 """
  pass


def main():
  slack_client = SlackClient(SLACK_BOT_TOKEN)
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
  