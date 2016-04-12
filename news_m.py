import re
import yaml
import arrow
import logging
import requests
from   lxml import etree
from   dateutil import parser # I'd rather just import dateutil and call dateutil.parser.parse(), but python has a hard time finding parser. Old-style class, maybe?
from   news_consts import C, log_messages

class news_feed(list):
  def __init__(self, url, xpathConfig):
    # TODO: news_feed.__init__: handle authenticated proxy nonsense.
    try:
      result = requests.get(url)
      if result.status_code == 200:
        root = etree.fromstring(result.content)
      else:
        # if we didn't get a solid result, treat it the same as an error.
        # TODO: news_feed.__init__: see if requests.get() handles redirects for us.
        raise requests.exceptions.ConnectionError
    except requests.exceptions.ConnectionError as e:
      logging.error(log_messages.E_UNABLE_TO_FETCH%(result.status_code, url))
    except etree.XMLSyntaxError as e:
      logging.error(log_messages.E_INVALID_XML%url)
    else:
      # effectivly skip doing anything if we couldn't get or parse the feed.
      # TODO: news_feed.__init__: I'm unsure how the rest of the app will behave to an empty (subclassed) list.
      for e in root.xpath(xpathConfig[C.XPATH_CONFIG][C.ITEM_ELEM]):
      ### REMINDER! You overrode the append method.
        self.append(*self._parse(e, xpathConfig[C.XPATH_CONFIG]))

  def _parse(self, e, xpathConfig):
    url = self._safe_xpath(e, xpathConfig[C.XP_URL], xpathConfig[C.NAMESPACE]) or ''
    title = self._safe_xpath(e, xpathConfig[C.XP_TITLE], xpathConfig[C.NAMESPACE]) or ''
    body = self._safe_xpath(e, xpathConfig[C.XP_BODY], xpathConfig[C.NAMESPACE]) or ''
    date = self._safe_xpath(e, xpathConfig[C.XP_DATE], xpathConfig[C.NAMESPACE]) or ''
    image = self._safe_xpath(e, xpathConfig[C.XP_IMAGE], xpathConfig[C.NAMESPACE]) or ''

    body = C.STRIP_HTML_RE.sub('', body) if xpathConfig[C.STRIP_HTML] else body
    return url, title, body, date, image

  def _safe_xpath(self, e, xp, ns):
    try:
      item = e.xpath(xp, namespaces=ns)
    except etree.XPathEvalError:
      logging.error(log_messages.E_INVALID_XPATH%(xp, e.tag))
      return None

    # TODO: news_feed._safe_xpath: detect and transform text encoding instead of throwing stuff out.
    return item[0].encode('ascii', 'ignore') if item else None

  # override the append function
  def append(self, url, title, body, date, image=None):
    return super(news_feed, self).append(self._story(url, title, body, date, image))
  
  ### nested class
  class _story(object):
    def __init__(self, url, title, body, date, image):
      self.url = url
      self.title = self.title
      self.body = self.body
      self.date = arrow.get(parser.parse(date)) # TODO: _story.__init__: arrow.get and dateutil.parser.parse probably can throw all sorts of errors that need handled.
      self.image = image if not image or image.lower().startswith('http') else 'http://'+image
