"""Interact with quote storage.

	This module is used to interact with the database, adding and retrieving
	quotes as instructed.
"""


def retrieve(quote_id=None):
	"""Retrieves quotes from the database.

		Arguments:
			- quote_id (integer) the id of the quote to retrieve. If no quote_id is
				given, then a random quote is retrieved

		Returns:
			- quote (string) the quote obtained from the database, or an error 
				message
	"""
	pass


def save(quote):
	"""Saves a quote to the database.

		Arguments:
			- quote (string) the quote to be saved

		Returns:
			- quote_id (integer) the id of the newly added quote. -1 if the save
				operation failed
	"""
	pass


def delete(quote_id):
	"""Removes a quote from the database.

		Arguments:
			- quote_id (integer) the id of the quote targetted for removal

		Returns:
			- removal_status (boolean), true if the quote was removed successfully
	"""
	pass
