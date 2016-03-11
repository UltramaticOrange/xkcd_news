import yaml
from news_consts import C
from news_m import news_feed

class xkcd_news(list):
  def __init__(self):
    news_feeds = open(C.FEEDS_FILE) # TODO: xkcd_news:__init__: handle being unable to open a file
    news_feeds = news_feeds.read() # TODO: xkcd_news:__init__: handle being unable to read a file
    news_feeds = yaml.load(news_feeds) # TODO: xkcd_news:__init__: handle being unable to parse yaml/syntax error

    for url,xpathConfig in news_feeds.items():
      self.append(news_feed(url, xpathConfig))
