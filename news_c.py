import yaml
import logging
from news_consts import C, log_messages
from news_m import news_feed

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
      self.append(news_feed(url, xpathConfig))
