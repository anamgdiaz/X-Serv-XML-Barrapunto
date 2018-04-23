#!/usr/bin/python3
# -*- coding: utf-8 -*-


from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
from urllib import request

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""


    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.line = "Title: " + self.theContent + "."
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                link = "<a href='" + self.theContent + "'>" + self.line + "</a></br>"
                file = open("barrapunto.html","a")
                file.write(link)
                file.close()
                self.inContent = False
                self.theContent = ""
                self.line = ""
                file.close()

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

if len(sys.argv) < 1:
    print ("Usage: python xml-parser-barrapunto.py <document>")
    print (" <document>: file name of the document to parse")
    sys.exit(1)


# Load parser and driver
theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!
file = open("barrapunto.html","w")
file.write("<h1>Lista de contenido </h1>")
file.close()
url = "http://barrapunto.com/index.rss"
xmlURL = request.urlopen(url)
theParser.parse(xmlURL)

print ("Parse complete")
