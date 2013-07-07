#! /usr/bin/env python

""" Simple Feed Reader: read rss feeds in the terminal. """

import time
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

# browser
BROWSER = "elinks"

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
f = open('feeds.txt')
feeds = dict([tuple(x.split(':')) for x in f])
keys = feeds.keys()

# functions
def show_feeds():
    count = 0
    for item in feeds.keys():
        print count, item
        count += 1
    print

def show_titles(feed_name, feed):
    os.system('clear')
    feed_name = "         " + feed_name + "    "
    print feed_name
    print "     " + "-" * len(feed_name)
    print
    entries = [t for t in feed.entries]
    start_index = 0
    target_index = 25
    while True:
        if len(entries) < 26:
            os.system('clear')
            head = "Stories on " + feed_name.strip()
            print "     " + head
            print "     " + "-" * len(head)
            for item in entries:
                print entries.index(item), item.title.replace('\n',' ').replace('\r',' ')
            print
            entry = raw_input("Which title do want? (q or Enter to chose a new feed) ")
            try:
                os.system('clear')
                view_entry_content(int(entry), feed)
                choice = raw_input("Use 1 to open link, Enter to return to list. ")
                if choice == "1":
                    os.system('%s %s' % (BROWSER, feed.entries[int(entry)].link))
            except:
                break
        else:
            entries = zip([feed.entries.index(x) for x in feed.entries], feed.entries)
            os.system('clear')
            head = "Stories on " + feed_name.strip()
            print "     " + head
            print "     " + "-" * len(head)
            for x in range(start_index,target_index):
                print entries[x][0], entries[x][1].title.replace('\n', ' ').replace('\r', ' ')
            print
            ans = raw_input("More? (m), Back up? (b), View? (num), Return to feeds? (q) ")
            if ans == 'm':
                start_index = start_index + 25
                if len(entries[start_index:]) >= 25:
                    target_index = target_index + 25
                else:
                    target_index = len(entries[start_index:])
            elif ans == 'b':
                if start_index == 0:
                    pass
                else:
                    target_index = start_index
                    start_index = start_index - 25
            elif ans == 'q':
                break
            else:
                try:
                    view_entry_content(int(ans), feed)
                    choice = raw_input("Use 1 to open link, Enter to return to list. ")
                    if choice == "1":
                        os.system('%s %s' % (BROWSER, feed.entries[int(ans)].link))
                except:
                    print "Input not recognizable."
                    time.sleep(3)

def view_entry_content(n, feed):
    os.system('clear')
    summary = feed.entries[n].summary
    try:
        url = shorten(feed.entries[n].link)
    except:
        url = feed.entries[n].link
    print "    " + feed.entries[n].title
    print "    " + ("-" * len(feed.entries[n].title))
    print
    print wrapper.fill(summary[:summary.find("<")])
    print
    print url
    print

if __name__ == '__main__':
    while True:
        os.system('clear')
        show_feeds()
        entry = raw_input("View (q to quit): ")
        if entry == 'q':
            os.system('clear')
            break
        else:
            os.system('clear')
            feed_name = keys[int(entry)]
            feed = fp.parse(feeds[feed_name])
            show_titles(feed_name, feed)
