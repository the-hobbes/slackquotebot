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
			- quote (unicode) the quote to be added to the database

		Returns:
			- message (string) a message indicating whether or not the quote has been
				added to the database
	"""
	s_quote = str(quote)
	id = data.save(s_quote)
	if id == -1:
		return "There was an error saving the quote"
	return "Quote #{} saved".format(id)


def retrieve_random_quote():
	"""Fetches a random quote from the database.
	
		Returns:
			- result (string) the quote retrieved from the database, or an error 
				message
	"""
	result = data.retrieve()
	if result == -1:
		return ":( there was an error getting a quote."

	return result
	

def remove_quote(quote_id):
	"""Removes a specific quote from the database.
	
		Arguments:
			- quote_id (integer) the id of the quote to be removed

		Returns:
			- message (string) a message indicating whether or not the quote has been
				removed from the database
	"""
	success = data.delete(quote_id)
	if not success:
		return "There was an error deleting quote {}".format(quote_id)
	return "Quote {} successfully removed".format(quote_id)
