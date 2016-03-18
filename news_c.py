import re
import yaml
import arrow
import logging
from   dateutil import parser
from   news_m import news_feed
from   news_consts import C, log_messages

class xkcd_news(list):
  def __init__(self):
    try:
      feeds = open(C.FEEDS_FILE)
      newsFeeds = feeds.read() # shouldn't need to put this here as python seems to complain on the open(). Just being safe.
    except IOError as e:
      logging.error(log_messages.E_MISSING_CONFIG%C.FEEDS_FILE)
    finally:
      feeds.close()

    try:
      newsFeeds = yaml.load(newsFeeds)
    except yaml.scanner.ScannerError as e:
      logging.error(log_messages.E_MALFORMED_CONFIG%C.FEEDS_FILE)

    for url,xpathConfig in newsFeeds.items():
      self.append(_xkcd_news(url, xpathConfig))


# This sub-classing layer might seem unneeded, but I want to be able to 
# reuse news_m.news_feed elsewhere without having to modify it.
class _xkcd_news(news_feed):
  def __init__(self, *args):
    try:
      xformFile = open(C.SUBS_FILE)
      self._transformations = xformFile.read()
    except IOError:
      logging.error(log_messages.E_MISSING_CONFIG%C.SUBS_FILE)
    finally:
      xformFile.close()

    try:
      self._transformations = yaml.load(self._transformations)
    except yaml.scanner.ScannerError as e:
      logging.error(log_messages.E_MALFORMED_CONFIG%C.SUBS_FILE)
    super(_xkcd_news, self).__init__(*args)

  def append(self, url, title, body, date, image=None):
    ### Note how 'super' is being used here: self is a subclass of news_feed and news_feed is a subclass of list. list.append() is needed, so in a sense, we're doing super(super())
    return super(news_feed, self).append(self._story(url, title, body, date, image, self._transformations))

  ### nested class
  class _story(object):
    def __init__(self, url, title, body, date, image, transformations):
      self.raw = _xkcd_news._raw(title, body)
      self.url = url
      self.title = self._transform(title, transformations)
      self.body = self._transform(body, transformations)
      self.date = arrow.get(parser.parse(date))
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
