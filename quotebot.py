"""Create a slack quotebot.
	
	This module performs the actual business logic operations of the quotebot.
	There are four possible functions that can be performed by the bot; 
		add_quote, retrieve_random_quote, retrieve_specific_quote, and remove_quote.

	Quotes are added and retrieved from the database via the data module.
"""

import data


def add_quote(quote):
	"""Adds a quote to the database via the data layer.

		Arguments:
			- quote (string) the quote to be added to the database

		Returns:
			- message (string) a message indicating whether or not the quote has been
				added to the database
	"""
	return "Addquote"


def retrieve_random_quote():
	"""Fetches a random quote from the database.
	
		Returns:
			- quote (string) the quote retrieved from the database, or an error 
				message
	"""
	return "Somequote"


def retrieve_specific_quote(quote_id):
	"""Fetches a specific quote from the database.
	
		Arguments:
			- quote_id (integer) the id of the quote to be retrieved

		Returns:
			- quote (string) the quote retrieved from the database, or an error 
				message
	"""
	pass


def remove_quote(quote_id):
	"""Removes a specific quote from the database.
	
		Arguments:
			- quote_id (integer) the id of the quote to be removed

		Returns:
			- message (string) a message indicating whether or not the quote has been
				removed from the database
	"""
	return "Removed quote"


def command_not_found(cmd):
	return "Command {} not found".format(cmd)
