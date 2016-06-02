# xkcd_news
## About xkcd_news:
The web comic XKCD has made suggested, "Substituutions that make reading the news more fun." This code was written to take-in RSS feeds from news websites, normalize the content, make the suggested substitutions, and present the content in an easy to read layout specified by an HTML template.

### Substitutions:
![alt tag](http://imgs.xkcd.com/comics/substitutions.png)

### Substitutions 2:
![alt tag](http://imgs.xkcd.com/comics/substitutions_2.png)

### Substitutions 3:
![alt tag](http://imgs.xkcd.com/comics/substitutions_3.png)

## Setup:
### Setup your environment:
```**NOTE:** xkcd_news was built on Python 2.7 on a Debian Jessie host. Setup instructions assume a similar environment.```
#### Verify Python is installed:
By default, python should already be on your host machine. In the `whereis` command below, note the paths `/usr/bin/python2.7` for Python 2.7 resources and `/usr/bin/python` for the executable.
```user@linux$ whereis python
python: /usr/bin/python2.7 /usr/bin/python3.4 /usr/bin/python3.4m /usr/bin/python /etc/python2.7 /etc/python3.4 /etc/python /usr/lib/python2.7 /usr/lib/python3.4 /usr/lib/python2.6 /usr/bin/X11/python2.7 /usr/bin/X11/python3.4 /usr/bin/X11/python3.4m /usr/bin/X11/python /usr/local/lib/python2.7 /usr/local/lib/python3.4 /usr/include/python2.7 /usr/include/python3.4m /usr/share/python /usr/share/man/man1/python.1.gz```

If Python is missing, run:
```user@linux$ sudo apt-get install python```

```**NOTE:** Python 3 will likely become the default version in near future and that specifying Python 2.7 in the `apt-get install` command may become necissary```

#### Install the Flask module for Python.
```user@linux$ sudo apt-get install python-flask```

#### Install the YAML module for Python.
```user@linux$ sudo apt-get install python-yaml```

#### Install the arrow module for Python.
```user@linux$ sudo apt-get install python-arrow```
```**NOTE:** Ubuntu and derivatives do not have a python-arrow package available through the APT repos. Running "pip install arrow" should resolve this dependancy.```

### Get the xkcd_news code from GitHub and test the envronment:
```user@linux$ git clone https://github.com/UltramaticOrange/xkcd_news.git
Cloning into 'xkcd_news'...
remote: Counting objects: 117, done.
remote: Total 117 (delta 0), reused 0 (delta 0), pack-reused 117
Receiving objects: 100% (117/117), 34.91 KiB | 0 bytes/s, done.
Resolving deltas: 100% (71/71), done.
Checking connectivity... done.
user@linux$ cd xkcd_news
user@linux$ python news_v.py
 * Running on http://127.0.0.1:5000/
```

If a message other than "Running..." appears when testing the configuration, you likely have unmet dependancies. Please report these so documentation can be updated as needed.
If the sucessful "running" text appears, then press Ctrl+C to stop the process from running.

## Configure new RSS feeds:
xkcd_news uses XPaths to identify the various parts of a news article in an RSS feed. XPaths are an entire separate topic not covered in this documentation. However, you can generally think of them as beeing like a directory structure where the first item in the path encapsulates the subsuqent items. So given the XML `<foo><bar><baz1></baz1><baz2></baz2>Hi!</bar></foo>`, the XPath `/foo/bar/baz2' would point us at the data in the `baz2` item and `/foo/bar/baz2/text()` would give us just the text `Hi!`.

By default, xkcd_news comes configured with several RSS feeds including Google News and Al Jazeera. To add additional RSS feeds, the `feeds.yaml` configuration file needs to be modified. It is recommended to begin by copying a configuration that is known to be working and modifying it for the new RSS feed. Because RSS is a well specified format, there should be very little that will need to be changed. Let's start with the existing Al Jazeera configuration and modify it for the Washington Post.

### Starting sample:
```
http://www.aljazeera.com/xml/rss/all.xml:
  xpathParse:
    stripHTML: false
    item: '/rss/channel/item'
    namespace: {}
    title: .//title/text()
    url: .//link/text()
    body: .//description/text()
    date: .//pubDate/text()
    image: /rss/channel/image/url/text()
```

####In top-down ordering, we see the following:
#### A URL
   This is the URL to the RSS feed.

#### `xpathParse:`
  This is a static value that will always remain unchanged. It identifies the start of the XPath configuration block and will serve to separate it from other configuration items in future versions of xkcd_news.

#### `stripHTML:`
  This will either be `true` or `false` depending on if the RSS feed has undesired HTML content in the main body (description/summary) text. Generally it's a good idea to simply set this to `true`. However, some RSS feeds, such as Google News, add links to recommeded stories. Stripping HTML in those cases can make the summary text confusing to read. A future version of xkcd_news will have an additional option to fine-tune what content should be stripped from the feed.

#### `item:` 
  This is a fully specified XPath to news items (headlines/articles) in the feed. Generally, this will never need to be changed. The exception might be for Atom feeds wich use a slightly different specification that is similar to RSS.

#### `namespace:` 
 Namespaces are a part of XML and deserve their own section that won't be covered here. In xkcd_news, they're generally used to help specify the XPath to an image associated with a specific news item in the RSS feed. In the example, we'll add a namespace so we can specify a non-standard RSS tag in a format specification provided by Yahoo.

#### `title:`
  This value is a relative XPath where the specific item in the XPath `/rss/channel/item` is handled for you. This is the effectively the headline of the news article. It is unlikely you will need to change this.

#### `url:`
  This is the relative XPath that specifies a link to the full news article. It is unlikely you will need to change this.

#### `body:`
  This is the relative XPath that specifies the summary/description text of the news article. It is unlikely you will need to change this.

#### `date:`
  This is the relative XPath that specifies the publication date of the news article. It is unlikely you will need to change this. This date value determines the order of the final output. 

#### `image:`
  An image is not part of the default RSS specification. The result is that this value will likely need to be changed for every RSS feed added to feeds.yaml. The default `feeds.yaml` configuration comes with examples on how to find an image resource in the article summary/body by regular expressions (see uses of the 're' namespace), by non-standard tags (see uses of the 'yahoo' namespace), by simply defaulting to the main image of the feed (see the above starting sample), and by using an XPath that gives us the image URL via regular expressioin if one is available, otherwise defaulting to the main feed image (effectively mixing two of the previous options).

### Updated sample:
```
http://feeds.washingtonpost.com/rss/national:
  xpathParse:
    stripHTML: false
    item: '/rss/channel/item'
    namespace: 
      yahoo: http://search.yahoo.com/mrss/
    title: .//title/text()
    url: .//link/text()
    body: .//description/text()
    date: .//pubDate/text()
    image: .//yahoo:thumbnail/@url
```

#### What changed?
- The URL changed to point at the RSS feed. Instead of pointing at Al Jazeera U.S. news, it now points at the national coverage for the Washington Post.
- We added the namespace `yahoo` which allows us to point at the non-standard "thumbnail" tag for the article image.
- We updated the image XPath. Note how we're using a relative path and specifying the `yahoo` namespace. The `@` symbol indicates that we're looking at an XML attribute (e.g. `bar` in `<foo bar='Hi!' />`)
