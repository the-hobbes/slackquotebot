# A file to store globals.
def init():
  """Use of init ensures other modules don't modify globals before main()."""
  global SECRETS
  SECRETS = {}
