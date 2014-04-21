""" NhacVuiParser - Parser data from http://nhac.vui.vn

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


class NhacVuiParser(HTMLParser):
    def __init__(self, url):
        """Returns new Sequence object with specified url

        url: link to nhacso.net web page
        """
        HTMLParser.__init__(self)
        self.song_name = []
        self.song_artist = []
        self.song_link = []
        self.song_type = []
        self.data_url = ''
        req = urlopen(url)  # open connection to web page
        data = req.read().split("\n")  # split web page with \n
        feed_data = None
        for param in data:
            if (param.find('playlistfile') > -1):
                feed_data = param
                break
        self.feed(feed_data)  # parser html data

    def handle_starttag(self, tag, attrs):
        """Handle html tag to get data
        """
    
    def handle_data(self, data):
        self.data_url = self.data_url + data
    
    def handle_entityref(self, name):
            self.data_url = self.data_url + '&' + name
        
    def get_info(self):
        """Get info
        """
        playlist_id = self.data_url.translate(None, "\t',: ").replace('playlistfile', '')
        playlist_url = 'http://hcm.nhac.vui.vn' + playlist_id
        req = urlopen(playlist_url)
        xml_data = req.read().replace('jwplayer:', '')
        tree = ET.fromstring(xml_data)  # parser xml data
        for name in tree.findall('.//channel/item/title'):
            self.song_name.append(name.text.strip())  # get song name
        for artist in tree.findall('.//channel/item/description'):
            self.song_artist.append(artist.text.replace(u'Th\u1ec3 hi\u1ec7n: ', '').strip())  # get song artist
        for media_url in tree.findall('.//channel/item/file'):
            self.song_link.append(media_url.text)   # get media url
            if media_url.text is not None:
                self.song_type.append(media_url.text.split('.')[-1])  # get media type
            else:
                self.song_type.append(None)

    def music_data(self):
        """Returns data of Object

        song_name: list of song name
        song_artist: list of artist
        song_link: list of mp3 media link
        """
        self.get_info()
        return self.song_name, self.song_artist, self.song_link, self.song_type

