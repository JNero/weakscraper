# -*- coding: utf-8 -*-

# python apps
import collections
import html.parser
import pdb
import pprint
from abc import ABCMeta

# out apps
from .exceptions import AssertCompleteFailure

DEBUG = False


class BaseParser(html.parser.HTMLParser, metaclass=ABCMeta):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.genealogy = [[]]

    def __str__(self):
        return '<BaseParser(genealogy={})>'.format(self.genealogy)

    def assert_complete(self):
        if DEBUG:
            print('\nBaseParser.assert_complete():\n\tself.genealogy:')
            pprint.pprint(self.genealogy)
            # pdb.set_trace()
        assert(len(self.genealogy) == 1)
        root_node = None
        for root_node in self.genealogy[0]:
            if root_node['nodetype'] == 'tag' and root_node['name'] == 'html':
                break
        if not root_node:
            raise AssertCompleteFailure(self.genealogy)
        return root_node

    def get_result(self):
        if DEBUG:
            print('\nBaseParser.get_result():\n\tself.genealogy:')
            pprint.pprint(self.genealogy)
            # pdb.set_trace()
        root_node = self.assert_complete()
        return root_node

    def handle_startendtag(self, tag, attrs):
        attrs.append(('wp-leaf', None))
        self.handle_starttag(tag, attrs)

    def handle_data(self, text):
        if DEBUG:
            print('\nBaseParser.handle_data():\n\ttext: {}\n\tself.genealogy:' \
                    .format(text))
            pprint.pprint(self.genealogy)
        text = text.strip(' \t\n\r')
        if text:
            brothers = self.genealogy[-1]
            myself = {'nodetype': 'text', 'content': text}
            brothers.append(myself)

    def handle_decl(self, decl):
        if DEBUG:
            print('\nBaseParser.handle_decl():\n\tdecl: "{}"\n\tself.genealogy:' \
                    .format(decl))
            pprint.pprint(self.genealogy)
            # pdb.set_trace()
        arr = decl.lower().split()
        if arr:
            self.handle_starttag(arr[0], [('wp-decl', None)])

    def unknown_decl(self, data):
        if DEBUG:
            print('\nBaseParser.unknown_decl():\n\data: "{}"\n\tself.genealogy:' \
                    .format(decl))
            pprint.pprint(self.genealogy)
        # raise ValueError('Unknown declaration.')
        self.handle_decl(data)

    def handle_starttag(self, tag, attrs):
        raise NotImplementedError('action must be defined!')

    def handle_endtag(self, tag):
        raise NotImplementedError('action must be defined!')


