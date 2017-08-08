# -*- coding: utf-8 -*-

# our apps
from weakscraper.base_parser import BaseParser
from weakscraper.exceptions import EndTagDiscrepancy, NodeTypeDiscrepancy

class HtmlParser(BaseParser):
    def handle_starttag(self, tag, attrs):
        attrs_dict = {}
        is_leaf = False
        is_decl = False
        for k, v in attrs:
            if k == 'wp-leaf':
                is_leaf = True
            elif k == 'wp-decl':
                is_decl = True
            else:
                attrs_dict[k] = v

        if tag in ['meta', 'link', 'br', 'img', 'input']:
            is_leaf = True

        if tag == 'html':
            if not is_decl:
                is_leaf = True

        brothers = self.genealogy[-1]

        node = {
                'nodetype': 'tag',
                'name': tag,
                'attrs': attrs_dict,
                }
        brothers.append(node)
        if not is_leaf:
            node['children'] = []
            self.genealogy.append(node['children'])

    def handle_endtag(self, tag):
        parent = self.genealogy[-2][-1]

        if (parent['nodetype'] != 'tag'):
            raise NodeTypeDiscrepancy(self.genealogy, parent['nodetype'])
        elif (parent['name'] != tag):
            raise EndTagDiscrepancy(self.genealogy, parent['name'])
        else:
            self.genealogy.pop()

    def handle_comment(self, text):
        pass

    def handle_decl(self, decl):
        self.handle_starttag('html', [('wp-decl', None)])
