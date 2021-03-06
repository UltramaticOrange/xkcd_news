- [xkcd_news](#)
  - [About xkcd_news:](#about-xkcd_news)
  - [Setup:](#setup)
    - [Setup your environment:](#setup-your-environment)
    - [Get the xkcd_news code from GitHub and test the environment:](#get-the-xkcd_news-code-from-github-and-test-the-environment)
  - [Change substitution values:](#change-substitution-values)
  - [Configure new RSS feeds:](#configure-new-rss-feeds)
  - [Running](#running)
    - [Start the service:](#start-the-service)
    - [Access the service (get the news):](#access-the-service)
    - [Alternative setup for public, internet accessible content:](#alternate-setup-for-public-internet-accessible-content)
  - [Formatting the HTML output:](#formatting-the-html-output)

# xkcd_news
## About xkcd_news:
The web comic XKCD has made suggested, "Substitutions that make reading the news more fun." This code was written to take in RSS feeds from news websites, normalize the content, make the suggested substitutions, and present the content in an easy to read layout specified by an HTML template.

### Substitutions:
![alt tag](http://imgs.xkcd.com/comics/substitutions.png)

### Substitutions 2:
![alt tag](http://imgs.xkcd.com/comics/substitutions_2.png)

### Substitutions 3:
![alt tag](http://imgs.xkcd.com/comics/substitutions_3.png)

### My Friend Catherine (New Favorite Substitution):
![alt tag](http://imgs.xkcd.com/comics/my_friend_catherine.png)

## Setup:
### Setup your environment:
> **NOTE:** xkcd_news Setup instructions assume a Python version >=3.4.2 on Debian Jessie or a similar environment.

#### Verify Python is installed:
By default, python should already be on your host machine. In the `whereis` command below, note the `/usr/bin/python3`.

```
user@linux$ whereis python3
python3: /usr/bin/python3 /usr/bin/python3.4m /usr/bin/python3.4 /usr/lib/python3 /usr/lib/python3.4 /etc/python3 /etc/python3.4 /usr/local/lib/python3.4 /usr/include/python3.4m /usr/share/python3 /usr/share/man/man1/python3.1.gz
user@linux$ python3 -V
Python 3.4.2
```

If Python is missing, run:
```user@linux$ sudo apt-get install python3```

#### Install the Flask module for Python.
```user@linux$ sudo apt-get install python3-flask```

#### Install the YAML module for Python.
```user@linux$ sudo apt-get install python3-yaml```

#### Install the arrow module for Python.
```user@linux$ sudo apt-get install python3-arrow```

> **NOTE:** Ubuntu and derivatives do not have a python3-arrow package available through the APT repos. Running "python3 -m pip install arrow" should resolve this dependancy.

### Get the xkcd_news code from GitHub:
```
user@linux$ git clone https://github.com/UltramaticOrange/xkcd_news.git
Cloning into 'xkcd_news'...
remote: Counting objects: 117, done.
remote: Total 117 (delta 0), reused 0 (delta 0), pack-reused 117
Receiving objects: 100% (117/117), 34.91 KiB | 0 bytes/s, done.
Resolving deltas: 100% (71/71), done.
Checking connectivity... done.
```

### Get the rss_parse module from PyPI:
#### If you'll be running xkcd_news with user permissions (most secure):
```
user@linux$ python3 -m pip install rss_parse --user
```

> **NOTE:** rss_parse is only available for Python versions >= 3.4, so "pip install rss_parse --user" should work just the same.

#### If you're lazy (or having trouble. This is more fool-proof):
```
user@linux$ sudo python3 -m pip install rss_parse
```

### Testing that it works:
```
user@linux$ cd xkcd_news
user@linux$ python3 news_v.py
 * Running on http://127.0.0.1:5000/
```

If a message other than "Running..." appears when testing the configuration, you likely have unmet dependencies. Please report these so documentation can be updated as needed.
If the successful "running" text appears, then press Ctrl+C to stop the process from running.

## Change substitution values:
To change the substitution values, edit the `substitutions.yaml` configuration file. This is a simple list of key:value pairs where the key is the text we wish to replace, and the value is what we wish to read instead. The key is case insensitive and allows for regular expressions.

For example, if we wanted to replace all instances of Trump with Drumpf we'd add the following line:
```
Trump: Drumpf
```

If we wanted to replace all instance of Hillary or Hillary Clinton with Billary, our file becomes
```
Trump: Drumpf
Hillary( Clinton)?: Billary
```

Note how we're using regular expressions to replace both "Hillary" and "Hillary Clinton".

## Configure new RSS feeds:
xkcd_news uses XPaths to identify the various parts of a news article in an RSS feed. XPaths are an entire separate topic not covered in this documentation. However, you can generally think of them as being like a directory structure where the first item in the path encapsulates the subsequent items. So given the XML `<foo><bar><baz1></baz1><baz2>Hi!</baz2></bar></foo>`, the XPath `/foo/bar/baz2` would point us at the data in the `baz2` item and `/foo/bar/baz2/text()` would give us just the text `Hi!`

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
  This will either be `true` or `false` depending on if the RSS feed has undesired HTML content in the main body (description/summary) text. Generally it's a good idea to simply set this to `true`. However, some RSS feeds, such as Google News, add links to recommended stories. Stripping HTML in those cases can make the summary text confusing to read. A future version of xkcd_news will have an additional option to fine-tune what content should be stripped from the feed.

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
  An image is not part of the default RSS specification. The result is that this value will likely need to be changed for every RSS feed added to `feeds.yaml`. The default `feeds.yaml` configuration comes with examples on how to find an image resource in the article summary/body by regular expressions (see uses of the 're' namespace), by non-standard tags (see uses of the 'yahoo' namespace), by simply defaulting to the main image of the feed (see the above starting sample), and by using an XPath that gives us the image URL via regular expression if one is available, otherwise defaulting to the main feed image (effectively mixing two of the previous options).

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
- We updated the image XPath. Note how we're using a relative path and specifying the `yahoo` namespace. The `@` symbol indicates that we're looking at an XML attribute (e.g. `@bar` points at `Hi!` in `<foo bar='Hi!' />`)

## Running
xkcd_news comes with a very minimal run script called `run`. If you've actually made it this far in the documentation, you'll likely want to create something more robust for yourself. Logging is directed to `news.log` in your current directory.

### Start the service:
#### Only accessable to the local machine (localhost):
```user@linux$ ./run```

To restart the service, simply re-run `./run` as above.

#### Accessable to other hosts on the network:
```user@linux$ ./run 0.0.0.0```

To restart the service, simply re-run `./run` as above.

> **NOTE:** If you're running on a machine with multiple network cards, it may be prudent to specify the exact IP of the networking interface you want teh service to be accessable on.

### Access the service (get the news):
Point your web browser at the IP and port you are running on. By default, this will be http://localhost:5000

### Alternative setup for public, internet accessible content:

If you're planning on running a public facing instance of xkcd_news, telling users to point their browsers at a specified port is not a viable option. In this instance, it is recommended that you treat xkcd_news more like a REST service: use `wget` to fetch the output of xkcd_news into a temporary file, and then move that file into your web directory.

Below is my current configuration

getNews.sh:
```
#!/bin/bash

cd /var/www/html
wget http://localhost:5000 -q -O tmp.html
mv tmp.html index.html
```

cron:
```
*/5 *  *   *   *     /var/www/getNews.sh
```

Effectively, cron runs the `getNews.sh` script every five minutes. That script gets the output of xkcd_news (running as a non-root user), puts it in a temporary file, and then replaces the main `index.html` file of the site.

#### Additional run information:
Depending on your use case, xkcd_news might be handling a large number of images, or are resizing large images down to a smaller size. This proved to be time intensive and as a result, xkcd_news has a temporary in-memory cache of 100 images. This improves the overall performance, but it should be noted that after a restart of the service, the individual doing the restart should navigate to the service to rebuild the image cache before permitting users to use the service again.
 
## Formatting the HTML output:
The default appearance of xkcd_news is ....... ugly. However, all HTML tags are given a class identifier so that they can be styled by CSS. To update the CSS styling, edit `template.html`.

The class identifiers are as follows:
* `date` - The publish date
* `wrapper` - A `<div>` tag that wraps an individual news story (image, headline, and summary text)
* `title` - A `<div>` that contains the story headline
* `image` - An `<img>` tag 
* `body` - A `<div>` tag that contains the summary text 
* `url` - An `<a>` (anchor) tag which contains the headline text.
