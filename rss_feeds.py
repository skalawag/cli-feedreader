#! /usr/bin/env python

""" Simple Feed Reader: read rss feeds in the terminal. """

import os
import urllib2
import json
import textwrap as tw
import feedparser as fp

__author__ = "Mark Scala"
__license__ = """This work is licensed under the Creative Commons Attribution 3.0
Unported License. To view a copy of this license, visit
http://creativecommons.org/licenses/by/3.0/."""

wrapper = tw.TextWrapper()

# url shortening
try:
    key = open('api_key').readline()
except: pass

def shorten(url):
    data_string = "{'longUrl':'%s'}" % url
    req = urllib2.Request('https://www.googleapis.com/urlshortener/v1/url?key='+key,
                          data=data_string,
                          headers={'Content-Type':'application/json'})
    res = urllib2.urlopen(req)
    return json.load(res)['id']

# feeds
feeds = {"Slashdot": "http://rss.slashdot.org/Slashdot/slashdot",
         "Think Progress": "http://thinkprogress.org/feed/",}
keys = feeds.keys()

# functions
def show_feeds():
    count = 1
    for item in feeds.keys():
        print count, item
        count += 1
    print

def show_titles(feed_name, feed):
    feed_name = "         " + feed_name + "    "
    print feed_name
    print "     " + "-" * len(feed_name)
    print
    for item in feed.entries:
        print feed.entries.index(item), item.title
    print

def view_entry_content(n, feed):
    summary = feed.entries[n].summary
    try:
        url = shorten(feed.entries[n].link)
    except:
        url = feed.entries[n].link
    print "    " + feed.entries[n].title
    print "    " + "-" * len(feed.entries[n].title)
    print
    print wrapper.fill(summary[:summary.find("<")])
    print
    print short_url
    print

if __name__ == '__main__':
    while True:
        os.system('clear')
        show_feeds()
        entry = int(raw_input("View: "))
        os.system('clear')
        feed_name = keys[entry - 1]
        feed = fp.parse(feeds[feed_name])
        while True:
            os.system('clear')
            show_titles(feed_name, feed)
            entry = raw_input("Which title do want? (+ to chose a new feed) ")
            if entry == '+':
                break
            else:
                os.system('clear')
                view_entry_content(int(entry), feed)
                choice = raw_input("Use 1 to open link (requires lynx), Enter to return to list. ")
                if choice == 1:
                    os.system('lynx %s' % sd.entries[entry].link)
