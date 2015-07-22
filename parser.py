#!/usr/bin/python
import feedparser
import re
import psycopg2

import smtplib
from email.mime.text import MIMEText



conn = psycopg2.connect("dbname=allegro host=localhost user=allegro password=allegro")
cur = conn.cursor()

feed_url = "http://allegro.pl/rss.php/cat?category=89958"

feed = feedparser.parse(feed_url)

message = ""

def link2id(link):
    p = re.compile('i([0-9]+)\.html')
    out = p.search(link)
    if out:
        return out.group(1)

def testLink(id,cur):
    cur.execute("select count(*) from wpis where id = %s" %id)
    out = cur.fetchone()
    count = out[0]
    if count == 0 :
        cur.execute ("insert into wpis (id) values (%s)" % id )
        conn.commit()
        return True
    return False

for cell in feed['entries']:
    link =  cell['link']
    id =  link2id(link)
    if testLink(id,cur):
        title =  cell['title']
        summary = cell['summary']
        print title
        message = message + title + summary

        
if message != "":
    msg = MIMEText(message.encode('utf-8'))
    msg['Subject'] = "Allegro Informacja"
    msg['From'] = 'allegro@darevee.pl'
    msg['To'] = 'adam.kurowski@gmail.com'
    s = smtplib.SMTP('10.20.20.10')
    s.sendmail('allegro@darevee.pl','adam.kurowski@gmail.com',msg.as_string())
    s.quit()
    print message
