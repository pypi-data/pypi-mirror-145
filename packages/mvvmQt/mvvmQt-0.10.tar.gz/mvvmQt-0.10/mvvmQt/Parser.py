# -*- coding: utf-8 -*-
import re
from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop
import sys, asyncio, os
from jinja2 import FileSystemLoader, Environment
from pyquery import PyQuery as pq
from mvvmQt.Widget import Widget
from mvvmQt.Attributes import Attribute
from mvvmQt.Events import Event
from mvvmQt.Elements import Element
from mvvmQt.attrConfig import ElementAttr
from mvvmQt.alignConfig import ElementAlign

class Parser:
    ElementAttrConfig = ElementAttr
    ElementAlignConfig = ElementAlign

    def __init__(self, src, tempDir='templates', indexName='index', obj={}, models=None, events=None):
        self.env = Environment(loader=FileSystemLoader(searchpath=os.path.join(src, tempDir), encoding='utf-8'))
        self.obj = obj
        self.indexName = indexName
        self.elements = [] #元素列表
        self.models = models
        self.events = events

    def build(self):
        t = self.env.get_template("%s.jinja2" % self.indexName)
        self.app = QApplication(sys.argv)
        html = t.render(**self.obj)
        doc = pq(html)
        self.createElements(doc)
        for e in self.elements:
            e.make()
        self.run()

    def run(self):
        loop = QEventLoop(self.app)
        asyncio.set_event_loop(loop)
        # self.ui.run()
        with loop:
            loop.run_forever()

    def createElements(self, doc):
        list(map(self.loopChild, doc.children()))

    def tagName(self, dom):
        s = str(dom).strip()
        c = re.compile(r'\<(.*?)\>')
        return c.findall(s)[0].split(' ')[0]

    def loopChild(self, e, parent=None):
        dom = pq(e)
        tagName = self.tagName(dom)
        #检查是否为属性设置
        if tagName.startswith('attr'):
            ob_value = dom.attr('ob')
            if ob_value:
                value = getattr(self.models, ob_value)
            else:
                value = dom.attr('v')
            return Attribute(tagName.replace('attr-', ''), value, dom)
        
        if tagName.startswith('event'):
            name = dom.attr('v')
            f = getattr(self.events, name)
            return Event(tagName.replace('event-', ''), f)

        e = Element(self, parent, tagName, dom)
        l = list(map(lambda c: self.loopChild(c, e), dom.children()))
        attrs = []
        events = []
        childs = []
        for c in l:
            if type(c) is Attribute:
                attrs.append(c)
            elif type(c) is Event:
                events.append(c)
            elif type(c) is Element:
                childs.append(c)

        e.childs = childs
        e.attrs = attrs
        e.events = events
        self.elements.append(e)
        return e

if __name__ == "__main__":
    p = Parser('./')
    p.parser()