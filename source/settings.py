# A file to store globals.
def init():
  """Use of init ensures other modules don't modify globals before main()."""
  global SECRETS
  global QUOTE_LIST
  SECRETS = {}
  QUOTE_LIST = []