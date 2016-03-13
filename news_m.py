import re
import yaml
import arrow
import requests
from lxml import etree
from news_consts import C
from dateutil import parser # I'd rather just import dateutil and call dateutil.parser.parse(), but python has a hard time finding parser. Old-style class, maybe?

# TODO: pull in the publication date

class news_feed(list):
  def __init__(self, url, xpathConfig):
    self._transformations = open(C.SUBS_FILE) # TODO: news_feed.__init__: handle errors from open()
    self._transformations = self._transformations.read() # TODO: news_feed.__init__: I expect that read() can throw errors.
    self._transformations = yaml.load(self._transformations) # TODO: news_feed.__init__: handle errors from yaml.load

    # TODO: news_feed.__init__: handle authenticated proxy nonsense.
    result = requests.get(url) # TODO: news_feed.__init__: handle errors from requests.get
    elem = etree.fromstring(result.content) # TODO: news_feed.__init__: handle errors from etree.fromstring

    for e in elem.xpath(xpathConfig[C.XPATH_CONFIG][C.ITEM_ELEM]):
      # REMINDER! You overrode the append method.
      self.append(*self._parse(e, xpathConfig[C.XPATH_CONFIG]))

  def _parse(self, e, xpathConfig):
    url = self._safe_xpath(e, xpathConfig[C.XP_URL], xpathConfig[C.NAMESPACE])
    title = self._safe_xpath(e, xpathConfig[C.XP_TITLE], xpathConfig[C.NAMESPACE])
    body = self._safe_xpath(e, xpathConfig[C.XP_BODY], xpathConfig[C.NAMESPACE])
    date = self._safe_xpath(e, xpathConfig[C.XP_DATE], xpathConfig[C.NAMESPACE])
    image = self._safe_xpath(e, xpathConfig[C.XP_IMAGE], xpathConfig[C.NAMESPACE])

    body = C.STRIP_HTML_RE.sub('', body) if xpathConfig[C.STRIP_HTML] else body
    return url, title, body, date, image

  def _safe_xpath(self, e, xp, ns):
    try:
      item = e.xpath(xp, namespaces=ns)
    except:
      # TODO: news_feed._safe_xpath: handle whatever errors lxml.etree.xpath throws when there's a syntax mistake in the path.
      return None

    # TODO: news_feed._safe_xpath: detect and transform text encoding instead of throwing stuff out.
    return item[0].encode('ascii', 'ignore') if item else None

  # override the append function
  def append(self, url, title, body, date, image=None):
    return super(news_feed, self).append(self._story(url, title, body, date, image, self._transformations))
  
  ### nested class
  class _story(object):
    def __init__(self, url, title, body, date, image, transformations):
      self.raw = news_feed._raw(title, body) # not sure if this is the correct syntax for accessing an outter's inner class (sibling class?).
      self.url = url
      self.title = self._transform(title, transformations)
      self.body = self._transform(body, transformations)
      self.date = arrow.get(parser.parse(date)) # TODO: _story.__init__: arrow.get and dateutil.parser.parse probably can throw all sorts of errors that need handled.
      self.image = image if not image or image.lower().startswith('http') else 'http://'+image

    def _transform(self, text, transformations):
      for t,r in transformations.items():
        text = re.sub(t, r, text, flags=re.I)
      return text

  ### nested class
  class _raw(object):
    def __init__(self, title, body):
      self.title = title
      self.body = body

class xkcd_news(list):
  def __init__(self):
    news_feeds = open(C.FEEDS_FILE) # TODO: xkcd_news:__init__: handle being unable to open a file
    news_feeds = news_feeds.read()
    news_feeds = yaml.load(news_feeds)

    for url,xpathConfig in news_feeds.items():
      self.append(news_feed(url, xpathConfig))
