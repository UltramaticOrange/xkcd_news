#!/usr/bin/python

import argparse
from lxml import etree
from requests import get

START='start'
END='end'
EVENTS=(START, END)

def inspectRSS(feedURL):
  tree = ''
  indent = ''
  feed = etree.fromstring(get(feedURL).content)
  for action,elem in etree.iterwalk(feed, events=EVENTS):
    if action == START:
      indent += '  '
      attrs = elem.keys()
      tree += '%s%s: %s :: %s\n'%(indent, elem.tag, ', '.join(attrs if attrs else ['None']), elem.text[:100].replace('\n', '') if elem.text else '')
    else:
      indent = indent[0:-2]

  return tree.encode('ascii', 'ignore')

inspectRSS('https://news.google.com/news?cf=all&hl=en&pz=1&ned=us&topic=h&num=3&output=rss')

parser = argparse.ArgumentParser()
parser.add_argument('--rss-url', dest='url', type=str, help='The URL of the RSS feed.')
args = parser.parse_args()
url = args.url if args.url.lower().startswith('http') else 'http://%s'%args.url
print inspectRSS(url) if url else 'You forgot to specify --rss-url, dummy!'
