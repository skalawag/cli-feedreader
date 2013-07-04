#! /usr/bin/env python

import os
import time
import textwrap as tw
import feedparser as fp

wrapper = tw.TextWrapper()

# feeds
feeds = {"Slashdot": "http://rss.slashdot.org/Slashdot/slashdot",
         "Think Progress": "http://thinkprogress.org/feed/",}
keys = feeds.keys()

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
    print feed.entries[n].title
    print "-" * len(feed.entries[n].title)
    print
    print wrapper.fill(summary[:summary.find("<")])
    print
    print feed.entries[n].link
    print

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
