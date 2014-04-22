#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ZingMp3Parser - Parser data from http://mp3.zing.vn

Parser web page to get xml url
Get xml file and parser to get data
"""

from urllib import urlopen
from HTMLParser import HTMLParser
from xml.etree import ElementTree as ET
import gzip
from StringIO import StringIO

__author__ = "Thuan.D.T (MrTux)"
__copyright__ = "Copyright (c) 2011 Thuan.D.T (MrTux) "
__credits__ = ["Thuan.D.T"]

__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Thuan.D.T (MrTux)"
__email__ = "mrtux@ubuntu-vn.org"
__status__ = "Development"


class NhacSoParser(HTMLParser):
    def __init__(self, url):
        """Returns new Sequence object with specified url

        url: link to *.nhac.vui.vn web page
        """
        HTMLParser.__init__(self)
        self.song_name = []
        self.song_artist = []
        self.song_link = []
        self.song_type = []
        req = urlopen(url)  # open connection to web page
        data = None
        if req.info().get('Content-Encoding') == "gzip":
            buf = StringIO( req.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read().split("\n")
        else:
            data = req.read().split("\n")  # split web page with \n
        feed_data = None
        for param in data:
            if (param.find('<param name="flashvars" value="') > -1):
                """Find line to get xml url
                """
                feed_data = param
                break
        self.feed(feed_data)  # parser html data

    def handle_starttag(self, tag, attrs):
        """Handle html tag to get xml data
        """
        if tag == 'param' and dict(attrs)['name'] == 'flashvars':
            """Get param tags and attribute 'flashvars'
            """
            flashvars = dict(attrs)['value']  # get flashvars value
            flashvars = flashvars.split('&')
            for xml_file in flashvars:
                if(xml_file.find('xmlPath=') > -1):
                    xml_url = xml_file.replace('xmlPath=', '')  # get xml url
                    break
            xml_data = urlopen(xml_url)  # get xml data
            if xml_data.info().get('Content-Encoding') == "gzip":
                buf = StringIO( xml_data.read())
                xml_data = gzip.GzipFile(fileobj=buf)
            tree = ET.parse(xml_data)
            for name in tree.findall('.//playlist/song/name'):
                self.song_name.append(name.text.strip())  # get song name
            for artist in tree.findall('.//playlist/song/artist'):
                self.song_artist.append(artist.text.strip())  # get song artist
            for media_url in tree.findall('.//playlist/song/mp3link'):
                self.song_link.append(media_url.text)  # get media url
                if media_url.text is not None:
                    self.song_type.append(media_url.text.split('.')[-1])  # get media type
                else:
                    self.song_type.append(None)
    
    def handle_entityref(self, ref): # No changes here either
        self.handle_data(self.unescape("&%s" % ref))
    
    def music_data(self):
        """Returns data of Object

        song_name: list of song name
        song_artist: list of artist
        song_link: list of mp3 media link
        """
        return self.song_name, self.song_artist, self.song_link, self.song_type
