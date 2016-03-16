import re

#C is for constants ...and that's good enough for me.
class C(object):
  # used in python
  FEEDS_FILE = 'feeds.yaml'
  SUBS_FILE = 'substitutions.yaml'
  HTML_TEMPLATE = 'template.html'

  # used in yaml conig file
  NAMESPACE = 'namespace'
  STRIP_HTML = 'stripHTML'
  ITEM_ELEM = 'item'
  XPATH_CONFIG = 'xpathParse'
  XP_TITLE = 'title'
  XP_URL = 'url'
  XP_BODY = 'body'
  XP_DATE = 'date'
  XP_IMAGE = 'image'

  STRIP_HTML_RE = re.compile('<[^>]+>', flags=re.I)

  # used in the presentation layer (template.html)
  HTML_TITLE = 'TITLE'
  HTML_BODY = 'BODY'

  # HTML class identifiers for css styling
  # <wrapper div><title div></title div><img /><body div></body div></wrapper div>
  STORY_PUBUBLISH_DATE = 'date'
  STORY_WRAPPER = 'wrapper' # div that includes image, headline, and text
  STORY_TITLE = 'title' # div that contains just the headline
  STORY_IMAGE = 'image' # img tag that does not contain the immense volume of your mom
  STORY_BODY = 'body' # just the text ..... that does not contain the immense volume of your mom
  STORY_URL = 'url'

  # This is probably a step too far, but \/\/hutevs.
  CLASS = 'CLASS'
  URL = 'URL'
  CONTENT = 'CONTENT'

  HTML_A = '<a class="{%s}" href="{%s}">{%s}</a>'%(CLASS, URL, CONTENT)
  HTML_DIV = '<div class="{%s}">{%s}</div>'%(CLASS, CONTENT)
  HTML_IMG = '<img class="{%s}" src="{%s}" />'%(CLASS, CONTENT)
  HTML_PUBLISH_DATE = '<div class="{%s}">{%s}</div>'%(CLASS, CONTENT)

  HTML_FALLBACK = '<html><head><title>{TITLE}</title></head><body>{BODY}</body></html>'

  IMG_MAX_SIZE = 125

class log_messages(object):
  E_MISSING_CONFIG = 'Missing or unreadable configuration file: %s'
  E_MALFORMED_CONFIG = 'Bad syntax in configuration file: %s'

  E_UNABLE_TO_FETCH = 'Unable to fetch URL. Got status %s: %s'
  
  E_INVALID_XML = 'Could not parse XML from feed: %s'
  E_INVALID_XPATH = 'Invalid xpath %s while processing tag %s'

  E_CORRUPT_IMAGE = 'Could not process image file from web: %s'
  E_UNKNOWN_IMAGE_TYPE = 'Unknown image type. Cannot process further.'

  E_TEMPLATE_MALFORMED = 'Template file %s was badly formed. Reverted to minimal formatting.\nDid you use single curly braces (i.e. { and }) in your CSS instead of double?'
  W_TEMPLATE_UNAVAILABLE = 'Template file %s could not be read.'
