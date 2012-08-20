#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" NhacSoParser - Parser data from http://nhacso.net

Parser web page to get xml url
Get xml file and parser to get data
"""

__author__ = "Thuan.D.T (MrTux)"
__copyright__ = "Copyright (c) 2011 Thuan.D.T (MrTux) "
__credits__ = ["Thuan.D.T"]

__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Thuan.D.T (MrTux)"
__email__ = "mrtux@ubuntu-vn.org"
__status__ = "Development"

from urllib import urlopen
from HTMLParser import HTMLParser
from xml.etree import ElementTree as ET


class NhacSoParser(HTMLParser):
    def __init__(self, url):
        """Returns new Sequence object with specified url

        url: link to nhacso.net web page
        """
        HTMLParser.__init__(self)
        self.song_name = []
        self.song_artist = []
        self.song_mp3link = []
        req = urlopen(url)  # open connection to web page
        data = req.read().split("\n")  # split web page with \n
        feed_data = None
        for param in data:
            if (param.find('<param name="flashvars" value="xmlPath=') > -1):
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
            tree = ET.parse(xml_data)
            for name in tree.findall('.//song/name'):
                self.song_name.append(unicode(name.text))  # get song name
            for artist in tree.findall('.//song/artist'):
                self.song_artist.append(unicode(artist.text))  # get song artist
            for mp3link in tree.findall('.//song/mp3link'):
                self.song_mp3link.append(unicode(mp3link.text))  # get mp3 link

    def music_data(self):
        """Returns data of Object

        song_name: list of song name
        song_artist: list of artist
        song_mp3link: list of mp3 media link
        """
        return self.song_name, self.song_artist, self.song_mp3link

