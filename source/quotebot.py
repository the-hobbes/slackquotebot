"""Create a slack quotebot.
	
	This module performs the actual business logic operations of the quotebot.
	There are four possible functions that can be performed by the bot; 
		add_quote, retrieve_random_quote, retrieve_specific_quote, and remove_quote.

	Quotes are added and retrieved from the database via the data module.
"""

import data
from prometheus_client import Counter


QUOTE_REQUESTS = Counter(
	"quote_commmand_total_requests", 
	"Total quotebot requests, by request type and result.",
	["command_type", "result"])


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
		QUOTE_REQUESTS.labels(command_type="addquote", result="failure").inc()
		return "There was an error saving the quote"

	QUOTE_REQUESTS.labels(command_type="addquote", result="success").inc()
	return "Quote #{} saved".format(id)


def retrieve_random_quote():
	"""Fetches a random quote from the database.
	
		Returns:
			- result (string) the quote retrieved from the database, or an error 
				message
	"""
	result = data.retrieve()
	if result == -1:
		QUOTE_REQUESTS.labels(command_type="quote", result="failure").inc()
		return ":( there was an error getting a quote."

	QUOTE_REQUESTS.labels(command_type="quote", result="success").inc()
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
		QUOTE_REQUESTS.labels(command_type="deletequote", result="failure").inc()
		return "There was an error deleting quote {}".format(quote_id)

	QUOTE_REQUESTS.labels(command_type="deletequote", result="success").inc()
	return "Quote {} successfully removed".format(quote_id)
