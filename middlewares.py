# -*- coding: utf-8 -*-
# set proxy to privoxy and use Tor to change Ip

from tormanager import ConnectionManager


class ProxyMiddleware(object):

    def __init__(self):
        self.cm = ConnectionManager('tor_password')

    def process_request(self, request, spider):
        # new tor IP
        self.cm.new_identity()
        # get request from spider and ask it to go through a proxy (privoxy = 'http://127.0.0.1:8118'
        # - privoxy acts like a man-in-the-middle in the computer
        request.meta['proxy'] = 'http://127.0.0.1:8118'
        spider.log('Proxy : %s' % request.meta['proxy'])