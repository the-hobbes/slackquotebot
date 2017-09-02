"""Interact with quote storage.

  This module is used to interact with the database, adding and retrieving
  quotes as instructed.
"""
import listener
import logging
import pprint
import psycopg2
import settings


TABLE = "quotetable"
COLUMN = "quote_blob"


def connect():
  conn_s = "host='localhost' dbname='{0}' user='{1}' password='{2}'".format(
    settings.SECRETS["dbname"], 
    settings.SECRETS["user"], 
    settings.SECRETS["password"])
  connection = psycopg2.connect(conn_s)
  cursor = connection.cursor()

  return connection, cursor


def retrieve():
  """Retrieves quotes from the database.

    Returns:
      - quote (string|int) the quote obtained from the database, or an error 
        code, of -1
  """
  quote = -1
  try:
    connection, cursor = connect()
    quote = None # TODO: grab quote here
  except psycopg2.Error as e:
    logging.error("Retrieve failed with error %s" % e.pgerror)

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
    cursor.execute("INSERT INTO %s (%s) VALUES (%s)", (TABLE, COLUMN, quote))
    quote_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
  except psycopg2.Error as e:
    logging.error("Commit failed with error %s" % e.pgerror)

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
    status = True # TODO: set this properly from the delete
  except psycopg2.Error as e:
    logging.error("Delete failed with error %s" % e.pgerror)

  return status
  
