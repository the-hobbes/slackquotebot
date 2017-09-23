# Quotebot
(A Slack bot for storing and retrieving quotes.)

## Purpose
If you've ever found yourself wanting to preserve an amusing statement from a
coworker or friend, this bot is for you. You can add and retrieve quotes from a
slack channel the bot is invited to, providing a context-free window into the
history of your group.

## Usage 
The quotebot listens to the slack channel where it is invited for three
commands: 
- !addquote, used to add a new quote. For example: !quote <user> I'm a quote.
- !quote, used to retrieve a random quote from the database.
- !deletequote, used to delete a specific quote from the database
