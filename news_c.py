import re
import yaml
import arrow
import logging
from rss_parse.rss_parse import RSSParser
from news_consts import C, LogMessages


def load_yaml(file_name):
    try:
        conf_handle = open(file_name)
        raw_yaml = conf_handle.read()
        conf_handle.close()
        return yaml.load(raw_yaml)
    except IOError as e:
        logging.error(LogMessages.E_MISSING_CONFIG % file_name)
    except yaml.scanner.ScannerError as e:
        logging.error(LogMessages.E_MALFORMED_CONFIG % file_name)


class XKCDNews(list):
    def __init__(self):
        news_feeds = load_yaml(C.FEEDS_FILE)
        kwargs = {C.SUBS_KWARG:load_yaml(C.SUBS_FILE)}

        for url,xpathConfig in news_feeds.items():
            self.append(_XKCDNews(url, xpathConfig, **kwargs))


class _XKCDNews(RSSParser):
    def __init__(self, *args, **kwargs):
        self._transformations = kwargs.pop(C.SUBS_KWARG)
        super().__init__(*args, **kwargs)

    def append(self, url, title, body, date, image=None):
        # Note how 'super' is being used here: self is a subclass of RSSParser and RSSParser is a
        # subclass of list. list.append() is needed, so in a sense, we're doing super(super())
        # Think about it as casting our _XKCDNews object into an RSSParser object.
        # Hopefully that last one will make sense because I'm tired of breaking this bit.
        super(RSSParser, self).append(self._Story(url, title, body, date, image, self._transformations))

    # nested class
    class _Story(object):
        def __init__(self, url, title, body, date, image, transformations):
            self.raw = (title, body)
            self.url = url
            self.title = self._transform(title, transformations)
            self.body = self._transform(body, transformations)
            self.date = arrow.get(date)
            self.image = image if not image or image.lower().startswith('http') else 'http://'+image

        @staticmethod
        def _transform(text, transformations):
            for t, r in transformations.items():
                text = re.sub(t, r, text, flags=re.I)
            return text
