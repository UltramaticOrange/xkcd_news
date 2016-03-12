import socket
from   flask import Flask
from   news_consts import C
from   news_c import xkcd_news

app = Flask(__name__)

@app.route('/')
def news():
  # TODO: news: pre-fetch, resize and base64 the images so we can easily toss them out if they 404 (I'm looking at YOU, Al Jazeera...)
  # TODO: news: don't use story.HTML() to generate formatting. Let's read an HTML doc and give it some fancy CSS.
  # ....or at least as "fancy" as I can manage.

  # TODO: news: handle being unable to open the template
  # TODO: news: handle being unable to read the template
  htmlTemplate = open(C.HTML_TEMPLATE).read()

  html = ''
  news = xkcd_news()
  for site in news:
    for story in site:
      body = C.HTML_DIV.format(**{C.CLASS:C.STORY_BODY, C.CONTENT:story.body})
      title = C.HTML_DIV.format(**{C.CLASS:C.STORY_TITLE, C.CONTENT:story.title})
      title = C.HTML_A.format(**{C.CLASS:C.STORY_TITLE, C.URL:story.url, C.CONTENT:title})
      image = C.HTML_IMG.format(**{C.CLASS:C.STORY_IMAGE, C.CONTENT:story.image})
      htmlStory = C.HTML_DIV.format(**{C.CLASS:C.STORY_WRAPPER, C.CONTENT:title+image+body})
      html += htmlStory

  # TODO: handle bad formatting in the template (read: someone didn't use {{ and }} in CSS)
  return htmlTemplate.format(**{C.HTML_BODY:html, C.HTML_TITLE:'your mom is a hoe bag, lulz.'})

def main():
  print news()

if __name__ == "__main__":
    # TODO: Take args if we just want to dump to screen for testing. 
    app.run(host='0.0.0.0')
    #main()
