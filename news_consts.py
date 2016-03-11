import re

#C is for constants ...and that's good enough for me.
class C(object):
  # used in python
  FEEDS_FILE = 'feeds.yaml'
  SUBS_FILE = 'substitutions.yaml'

  # used in yaml conig file
  NAMESPACE = 'namespace'
  STRIP_HTML = 'stripHTML'
  ITEM_ELEM = 'item'
  XPATH_CONFIG = 'xpathParse'
  XP_TITLE = 'title'
  XP_URL = 'url'
  XP_BODY = 'body'
  XP_IMAGE = 'image'

  STRIP_HTML_RE = re.compile('<[^>]+>', flags=re.I)
