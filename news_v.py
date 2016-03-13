import imghdr
import socket
import requests
from   PIL import Image
from   flask import Flask
from   news_consts import C
from   news_c import xkcd_news
from   base64 import b64encode
from   StringIO import StringIO

app = Flask(__name__)

# TODO: image64: would be good to memoize this. Python 2.7 does not have one in functools, so a custom decorator will be needed
# TODO: image64: don't rely on onthe C.IMG_MAX_SIZE -- optional params to allow the user to specify the size or to skip the resize.
def image64(url, imgTag=False): # 'img' is abbriviated to reflect the html <img /> tag.
  # TODO: image64: proxy config
  response = requests.get(url)
  if response.status_code != 200:
    return None # I really hate this sort of logic, but it's easier to read in this instance

  rawImage = response.content # get the image to be manipulated
  imageType = imghdr.what(StringIO(rawImage))
  imageObj = Image.open(StringIO(rawImage))

  # if the image is larger than a 125x125 thumbnail then resize it
  if imageObj.size[0] > C.IMG_MAX_SIZE or imageObj.size[1] > C.IMG_MAX_SIZE:
    # TODO: image64: handle errors 
    imageObj.thumbnail((C.IMG_MAX_SIZE, C.IMG_MAX_SIZE), Image.ANTIALIAS)

    fakeFile = StringIO() # a file-like object to hold the data in memory ... because PIL is an asshole that won't work with strings.
    imageObj.save(fakeFile, imageType.upper())
    fakeFile.seek(0)
    rawImage = fakeFile.read()

  b64image = 'data:image/%s;base64,%s'%(imageType, b64encode(rawImage))
  return '<img src="%s">'%b64image if imgTag else b64image

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
  sortable = {}
  for site in news:
    for story in site:
      body = C.HTML_DIV.format(**{C.CLASS:C.STORY_BODY, C.CONTENT:story.body})
      title = C.HTML_DIV.format(**{C.CLASS:C.STORY_TITLE, C.CONTENT:story.title})
      title = C.HTML_A.format(**{C.CLASS:C.STORY_TITLE, C.URL:story.url, C.CONTENT:title})
      image = C.HTML_IMG.format(**{C.CLASS:C.STORY_IMAGE, C.CONTENT:image64(story.image)}) if story.image else ''
      htmlStory = C.HTML_DIV.format(**{C.CLASS:C.STORY_WRAPPER, C.CONTENT:title+image+body})
      #html += htmlStory

      if story.date in sortable:
        sortable[story.date].append(htmlStory)
      else:
        sortable[story.date] = [htmlStory]

  for key in sorted(sortable):
    html += ''.join(sortable[key])

  # TODO: handle bad formatting in the template (read: someone didn't use {{ and }} in CSS)
  return htmlTemplate.format(**{C.HTML_BODY:html, C.HTML_TITLE:'your mom is a hoe bag, lulz.'})

def main():
  print news()

if __name__ == "__main__":
    # TODO: Take args if we just want to dump to screen for testing. 
    app.run(host='0.0.0.0')
    #main()
