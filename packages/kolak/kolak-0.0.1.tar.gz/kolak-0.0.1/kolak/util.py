import logging
import os
import sys
import re


class util(object):

    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    """
	url validator.
	
	url_validator(url:str) -> bool
	"""
    def url_validator(url):
        try:
            from urlparse import urlparse  # python2
        except:
            from urllib.parse import urlparse
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    """
	logging file wrapper.
	
	log_file(path_file:str, text:str, level:str) -> None
	"""
    def log_file(path_file, text, level="info"):
        write_log = {"debug": (logging.debug, logging.DEBUG), "info": (logging.info, logging.INFO), "warning": (
            logging.warning, logging.WARNING), "error": (logging.error, logging.ERROR), "critical": (logging.critical, logging.CRITICAL)}
        logging.basicConfig(
            filename=path_file, format='[%(asctime)s] %(levelname)s: %(message)s', level=write_log[level][1])
        write_log[level][0](text)

    """
	get_contents(url:str) -> str | bool(False)
	"""
    def get_contents(uri):
        try:
            from urllib.request import Request, urlopen
            request = Request(uri)
            request.add_header('User-Agent', "Flipboard")
            response = urlopen(request)
            content = response.read()
            response.close()
            return content.decode("utf-8")
        except:
            return False

    """
	html entities decode.
	
	html_decode(text:str) -> str
	"""
    def html_decode(text):
        try:
            from html import unescape  # python 3.4+
        except ImportError:
            try:
                from html.parser import HTMLParser  # python 3.x (<3.4)
            except ImportError:
                from HTMLParser import HTMLParser  # python 2.x
            unescape = HTMLParser().unescape
        return unescape(text)

    """
	html to text converter.
	
	html2text(text:str) -> str
	"""
    def html2text(text):
        text = util.cdata_clean(text)
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    """
	cdata cleaner.
	cdata_clean(text:str) -> str
	"""
    def cdata_clean(text):
        c = re.compile('<!\[CDATA\[(.*?)\]\]>', re.S)
        if c.search(text) is not None:
            return c.search(text).group(1).strip()
        return text
