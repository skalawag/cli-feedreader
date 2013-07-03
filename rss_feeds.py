
import os
import time
import feedparser as fp
import textwrap as tw

wrapper = tw.TextWrapper()

# feeds
slashdot = "http://rss.slashdot.org/Slashdot/slashdot"
sd = fp.parse(slashdot)

def show_titles():
    print "    Slashdot    "
    print "-" * len("    Slashdot    ")
    for item in sd.entries:
        print sd.entries.index(item), item.title
    print

def view_entry_content(n):
    summary = sd.entries[n].summary
    print sd.entries[n].title
    print "-" * len(sd.entries[n].title)
    print wrapper.fill(summary[:summary.find("<")])
    print
    print sd.entries[n].link
    print

while True:
    os.system('clear')
    show_titles()
    entry = int(raw_input("View: "))
    os.system('clear')
    try:
        view_entry_content(entry)
        choice = raw_input("Use 1 to open link (requires lynx), 2 to return to list. ")
        if choice == "1":
            os.system('lynx %s' % sd.entries[entry].link)
        else:
            continue
    except:
        print "You fucked up. Try again."
        time.sleep(3)
