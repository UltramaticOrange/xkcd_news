import socket
from   flask import Flask
from   news_c import xkcd_news

app = Flask(__name__)

@app.route('/')
def news():
  # TODO: news: pre-fetch, resize and base64 the images so we can easily toss them out if they 404 (I'm looking at YOU, Al Jazeera...)
  # TODO: news: don't use story.HTML() to generate formatting. Let's read an HTML doc and give it some fancy CSS.
  # ....or at least as "fancy" as I can manage.

  html = ''
  news = xkcd_news()
  for site in news:
    for story in site:
      html += story.HTML()
  return html

def main():
  print news()

if __name__ == "__main__":
    # TODO: Take args if we just want to dump to screen for testing. 
    app.run(host='0.0.0.0')
#    main()
