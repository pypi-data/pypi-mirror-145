import xml.etree.ElementTree as ET
from ipey.primitive import Primitive

class Label(Primitive):

    def __init__(self, text, anchor, prototype = None):
        super().__init__(prototype=prototype)

        self.text = text
        self.isMath = False
        self.type = 'label'
        self.size = "normal" 
        self.anchor = anchor
        self.vAlign = 'baseline'
        self.hAlign = 'left'

    def getBB(self):
        return (self.anchor, self.anchor)


    def translate(self, x, y):
        self.anchor = (self.anchor[0] + x, self.anchor[1] + y)


    def rotate(self, a, pivot=None):
        return 

    def draw(self):
        elem = ET.Element('text')
        self.addProperties(elem)

        elem.set('pos', f'{self.anchor[0]+ self.xP} {self.anchor[1]+ self.yP}')
        elem.set('type', self.type)
        
        if self.isMath:
            elem.set('style', 'math')

        elem.set('valign', self.vAlign)
        elem.set('halign', self.hAlign)

        elem.set('size', self.size)

        elem.text = self.text
        return elem
