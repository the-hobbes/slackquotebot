"""Interact with quote storage.

  This module is used to interact with the database, adding and retrieving
  quotes as instructed.
"""
import listener
import logging
import psycopg2
import random
import settings
from prometheus_client import Summary


# prefetch_seconds_count: number of times this function was called
# prefetch_seconds_sum: total amount of time spent in this function
PREFETCH_TIME = Summary(
  "prefetch_seconds", 'Time spent prefetching quotes in seconds.')


def connect():
  """Create a connection to the database.

    This function connects to the postgresql database using the authentication
    information supplied by the settings module, then returns a connection and
    a cursor to the caller.

    Returns:
      - connection (pyscopg2.connection), an encapsulation of a database session
      - cursor (pyscopg2.cursor), a mechanism to execute postgreSQL commands in
        a database session
  """
  conn_s = "host='database' dbname='{0}' user='{1}' password='{2}'".format(
    settings.SECRETS["dbname"], 
    settings.SECRETS["user"], 
    settings.SECRETS["password"])
  connection = psycopg2.connect(conn_s)
  cursor = connection.cursor()

  return connection, cursor


@PREFETCH_TIME.time()  # record summary statistics
def prefetch_quote_ids():
  """Populate an array of existing quote IDs.

    This array is used to store the quote id's of all quotes in the table. Due
    to the expense of this operation, it is done as little as possible; once on
    startup, and once each time a new quote is added to the database.
  """
  try:
    connection, cursor = connect()
    cursor.execute("SELECT quote_id FROM quotetable ORDER BY quote_id;")
    tuples = cursor.fetchall()
    settings.QUOTE_LIST = [t[0] for t in tuples]
    cursor.close()
    connection.close()
  except psycopg2.Error as e:
    logging.error("Problem prefetching records from the db: %s" % e)


def retrieve():
  """Retrieves quotes from the database.

    Returns:
      - quote (string|int) the quote obtained from the database, or an error 
        code, of -1
  """
  quote = -1
  try:
    connection, cursor = connect()
    quote_id = random.choice(settings.QUOTE_LIST)
    cursor.execute(
      "SELECT quote_blob FROM quotetable WHERE quote_id = %s;", (quote_id,))
    quote = cursor.fetchone()[0]
    cursor.close()
    connection.close()
  except psycopg2.Error as e:
    logging.error("Retrieve failed with error: %s" % e)

  return quote
    

def save(quote):
  """Saves a quote to the database.

    Arguments:
      - quote (string) the quote to be saved

    Returns:
      - quote_id (integer) the id of the newly added quote. -1 if the save
        operation failed
  """
  quote_id = -1
  try:
    connection, cursor = connect()
    cursor.execute(
      "INSERT INTO quotetable (quote_blob) VALUES (%s) RETURNING quote_id;",
      (quote,))
    quote_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    prefetch_quote_ids()  # we've updated the quotes, so we need to regenerate
  except psycopg2.Error as e:
    logging.error("Commit failed with error: %s" % e)

  return quote_id


def delete(quote_id):
  """Removes a quote from the database.

    Arguments:
      - quote_id (integer) the id of the quote targetted for removal

    Returns:
      - removal_status (boolean), true if the quote was removed successfully
  """
  status = False
  try:
    connection, cursor = connect()
    cursor.execute("DELETE FROM quotetable WHERE quote_id = %s;", (quote_id,))
    connection.commit()
    cursor.close()
    connection.close()
    status = True
  except psycopg2.Error as e:
    logging.error("Delete failed with error: %s" % e)

  return status
  
