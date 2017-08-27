"""Interact with quote storage.

  This module is used to interact with the database, adding and retrieving
  quotes as instructed.
"""
import listener
import psycopg2
import settings


def connect():
  conn_s = "host='localhost' dbname='{0}' user='{1}' password='{2}'".format(
    settings.SECRETS["dbname"], 
    settings.SECRETS["user"], 
    settings.SECRETS["password"])
  conn = psycopg2.connect(conn_s)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM quotetable")
  records = cursor.fetchall()
  pprint.pprint(records)


def retrieve():
  """Retrieves quotes from the database.

    Returns:
      - quote (string) the quote obtained from the database, or an error 
        message
  """
  # TODO: catch and log read errors at this level
  # TODO: pass retrieval information/query to connect
  # TODO: fix password auth failure
  connect()
    

def save(quote):
  """Saves a quote to the database.

    Arguments:
      - quote (string) the quote to be saved

    Returns:
      - quote_id (integer) the id of the newly added quote. -1 if the save
        operation failed
  """
  # TODO: catch and log mutate errors at this level
  pass


def delete(quote_id):
  """Removes a quote from the database.

    Arguments:
      - quote_id (integer) the id of the quote targetted for removal

    Returns:
      - removal_status (boolean), true if the quote was removed successfully
  """
  # TODO: catch and log mutate errors at this level
  pass
