# -*-coding:utf8;-*-
import re
import os
import sys
from zcache import Cache
from urllib import parse
from .util import util
from multiprocessing import Process, Queue


class Parser(object):

    title = ""
    description = ""
    permalink = ""
    updated = ""
    author = ""
    items = []

    def __init__(self, uri, cache_time=600):
        cache = Cache()
        if type(uri) != str:
            raise TypeError("value must be string!")
        self.__cache_time = cache_time
        self.__uri = uri
        self.__log_path = util.path+"/kolak.log"
        self.__matchItems = False
        if util.url_validator(uri):
            enuri = parse.quote_plus(uri)
            if cache.has(enuri):
                self.xmlfeed = cache.get(enuri)
                self.is_load_from_cache = True
            else:
                req = util.get_contents(uri)
                if req != False:
                    self.xmlfeed = req
                    self.is_load_from_cache = False
                    cache.set(enuri, req, ttl=cache_time)
                    cache.set(enuri+"_offline", req)
                else:
                    self.xmlfeed = cache.get(enuri+"_offline")
                    self.is_load_from_cache = True
        else:
            self.xmlfeed = uri
            self.is_load_from_cache = False

    def parse(self, limit=0, debug=False, parallel=False):
        self.__debug = debug
        n_limit = 1
        xmlfeed = self.xmlfeed
        parsed = self.__parse_items(xmlfeed)
        if parallel:
            self.q = Queue()
        for i in parsed:
            if parallel:
                self.__paralleling_parser(i)
            else:
                self.__noparalleling_parser(i)
            if limit != 0:
                if n_limit == int(limit):
                    break
                else:
                    n_limit = n_limit+1
        self.__parse_header()
        return self.items

    def __noparalleling_parser(self, item):
        title = self.__parse_title(item)
        content = self.__parse_content(item)
        link = self.__parse_link(item)
        date = self.__parse_date(item)
        image = self.__parse_image(item)
        podcast = self.__parse_podcast(item)
        items = {"date": date, "title": title, "description": content,
                 "link": link, "link_image": image, "link_podcast": podcast}
        self.items.append(items)

    def __paralleling_parser(self, item):
        items = {}
        q = True
        p1 = Process(target=self.__parse_title, args=(item, q,))
        p2 = Process(target=self.__parse_content, args=(item, q,))
        p3 = Process(target=self.__parse_link, args=(item, q,))
        p4 = Process(target=self.__parse_image, args=(item, q,))
        p5 = Process(target=self.__parse_podcast, args=(item, q,))
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        while not self.q.empty():
            items = dict(items, **self.q.get_nowait())
        self.items.append(items)

    def __parse_items(self, txml):
        txml = str(txml)
        models = []
        models.append(re.compile('<item.*?>(.*?)<\/item>', re.S))
        models.append(re.compile('<entry.*?>(.*?)<\/entry>', re.S))
        for model in models:

            mytry = model.findall(txml)
            if len(mytry) != 0:
                self.__matcItems = model
                return mytry
            else:
                pass
        if self.__debug:
            util.log_file(
                self.__log_path, "parse_items: no model is matching!\n---\n%s" % txml, "critical")
        return []

    def __parse_content(self, item, q=None):
        models = []
        models.append(re.compile('<description.*?>(.*?)<\/description>', re.S))
        models.append(re.compile('<content type.*?>(.*?)<\/content>', re.S))
        models.append(re.compile('<summary.*?>(.*?)<\/summary>', re.S))
        models.append(re.compile(
            '<atom:summary.*?>(.*?)<\/atom:summary>', re.S))
        for model in models:
            mytry = model.search(item)
            if mytry is not None:
                if q is not None:
                    self.q.put_nowait({"description": mytry.group(1)})
                return mytry.group(1)
            else:
                pass
        if self.__debug:
            util.log_file(
                self.__log_path, "parse_content: no model is matching!\n---\n%s" % item, "warning")
        if q is not None:
            self.q.put_nowait({"description": ""})
        return ""

    def __parse_title(self, item, q=None):
        models = []
        models.append(re.compile('<title.*?>(.*?)<\/title>', re.S))
        for model in models:
            mytry = model.search(item)
            if mytry is not None:
                if q is not None:
                    self.q.put_nowait({"title": mytry.group(1)})
                return mytry.group(1)
            else:
                pass
        if self.__debug:
            util.log_file(
                self.__log_path, "parse_title: no model is matching!\n---\n%s" % item, "warning")
        if q is not None:
            self.q.put_nowait({"title": ""})
        return ""

    def __parse_link(self, item, q=None):
        models = []
        models.append(re.compile('<link.*?>(.*?)<\/link>', re.S))
        models.append(re.compile("<link.*?href='(.*?)'", re.S))
        models.append(re.compile('<link.*?href="(.*?)"', re.S))
        models.append(re.compile('<id.*?>(.*?)<\/id>', re.S))
        for model in models:
            mytry = model.search(item)
            if mytry is not None:
                if q is not None:
                    self.q.put_nowait({"link": mytry.group(1)})
                return mytry.group(1)
            else:
                pass
        if self.__debug:
            util.log_file(
                self.__log_path, "parse_link: no model is matching!\n---\n%s" % item, "warning")
        if q is not None:
            self.q.put_nowait({"link": ""})
        return ""

    def __parse_image(self, item, q=None):
        models = []
        models.append(re.compile("<gd:image.*?src='(.*?)'", re.S))
        models.append(re.compile('<gd:image.*?src="(.*?)"', re.S))
        models.append(re.compile('<itunes:image.*?href="(.*?)"', re.S))
        for model in models:
            mytry = model.search(item)
            if mytry is not None:
                if q is not None:
                    self.q.put_nowait({"link_image": mytry.group(1)})
                return mytry.group(1)
            else:
                pass
        if self.__debug:
            util.log_file(
                self.__log_path, "parse_image: no model is matching!\n---\n%s" % item, "warning")
        if q is not None:
            self.q.put_nowait({"link_image": ""})
        return ""

    def __parse_date(self, item, q=None):
        models = []
        models.append(re.compile('<pubDate>(.*?)<\/pubDate>', re.S))
        models.append(re.compile('<published>(.*?)<\/published>', re.S))
        models.append(re.compile('<updated>(.*?)<\/updated>', re.S))
        for model in models:
            mytry = model.search(item)
            if mytry is not None:
                if q is not None:
                    self.q.put_nowait({"date": mytry.group(1)})
                return mytry.group(1)
            else:
                pass
        if self.__debug:
            util.log_file(
                self.__log_path, "parse_date: no model is matching!\n---\n%s" % item, "warning")
        if q is not None:
            self.q.put_nowait({"date": ""})
        return ""

    def __parse_podcast(self, item, q=None):
        models = []
        models.append(re.compile('<enclosure.*?url="(.*?)"', re.S))
        models.append(re.compile("<enclosure.*?url='(.*?)'", re.S))
        models.append(re.compile('<media:content.*?url="(.*?)"', re.S))
        models.append(re.compile("<media:content.*?url='(.*?)'", re.S))
        for model in models:
            mytry = model.search(item)
            if mytry is not None:
                if q is not None:
                    self.q.put_nowait({"link_podcast": mytry.group(1)})
                return mytry.group(1)
            else:
                pass
        if self.__debug:
            util.log_file(
                self.__log_path, "parse_podcast: no model is matching!\n---\n%s" % item, "warning")
        if q is not None:
            self.q.put_nowait({"link_podcast": ""})
        return ""

    def __parse_header(self):
        if not self.__matchItems:
            h = str(self.xmlfeed)
        else:
            h = re.sub(self.__matchItems, '', self.xmlfeed)
        self.title = self.__headerTitle(h)
        self.updated = self.__headerUpdated(h)
        self.permalink = self.__headerLink(h)
        self.author = self.__headerAuthor(h)
        self.description = self.__headerDescription(h)

    def __headerUpdated(self, item):
        models = []
        models.append(re.compile('<updated>(.*?)<\/updated>', re.S))
        models.append(re.compile(
            '<lastBuildDate>(.*?)<\/lastBuildDate>', re.S))
        for model in models:
            mytry = model.search(item)
            if mytry is not None:
                return mytry.group(1)
            else:
                pass
        if self.__debug:
            util.log_file(
                self.__log_path, "headerUpdated: no model is matching!\n---\n%s" % item, "warning")
        return ""

    def __headerAuthor(self, item):
        models = []
        models.append(re.compile(
            '<author>.*?<name>(.*?)<\/name>.*?<\/author>', re.S))
        models.append(re.compile('<author>(.*?)<\/author>', re.S))
        for model in models:
            mytry = model.search(item)
            if mytry is not None:
                return mytry.group(1)
            else:
                pass
        if self.__debug:
            util.log_file(
                self.__log_path, "headerAuthor: no model is matching!\n---\n%s" % item, "warning")
        return ""

    def __headerLink(self, item):
        models = []
        models.append(re.compile('<link>(.*?)<\/link>', re.S))
        models.append(re.compile("<link.*?href='(.*?)'", re.S))
        models.append(re.compile('<link.*?href="(.*?)"', re.S))
        for model in models:
            mytry = model.search(item)
            if mytry is not None:
                return mytry.group(1)
            else:
                pass
        if self.__debug:
            util.log_file(
                self.__log_path, "HeaderLink: no model is matching!\n---\n%s" % item, "warning")
        return ""

    def __headerTitle(self, item):
        models = []
        models.append(re.compile('<title.*?>(.*?)<\/title>', re.S))
        for model in models:
            mytry = model.search(item)
            if mytry is not None:
                return mytry.group(1)
            else:
                pass
        if self.__debug:
            util.log_file(
                self.__log_path, "headerTitle: no model is matching!\n---\n%s" % item, "warning")
        return ""

    def __headerDescription(self, item):
        models = []
        models.append(re.compile('<description.*?>(.*?)<\/description>', re.S))
        models.append(re.compile('<subtitle.*?>(.*?)<\/subtitle>', re.S))
        for model in models:
            mytry = model.search(item)
            if mytry is not None:
                return mytry.group(1)
            else:
                pass
        if self.__debug:
            util.log_file(
                self.__log_path, "headerDescription: no model is matching!\n---\n%s" % item, "warning")
        return ""

    def retry(self, uri=None, cache_time=None):
        if uri == None:
            uri = self.__uri
        if cache_time == None:
            cache_time = self.__cache_time
        self.__init__(uri, cache_time)
