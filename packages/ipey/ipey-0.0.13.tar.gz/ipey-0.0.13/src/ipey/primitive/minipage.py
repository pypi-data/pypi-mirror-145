import xml.etree.ElementTree as ET
from ipey.primitive import Label

class Minipage(Label):

    def __init__(self, text, anchor, prototype = None):
        super().__init__(text, anchor, prototype=prototype)

        self.type = 'minipage'
        self.size = "normal" 
        self.vAlign = 'top'
        self.hAlign = 'left'
        self.width = None
        self.style = 'normal'


    def rotate(self, a, pivot=None):
        return 

    def draw(self):
        elem = ET.Element('text')
        self.addProperties(elem)

        elem.set('pos', f'{self.anchor[0]} {self.anchor[1]}')
        elem.set('type', self.type)
        
        elem.set('style', self.style)

        elem.set('valign', self.vAlign)
        elem.set('halign', self.hAlign)

        if self.width:
            elem.set('width', str(self.width))

        elem.set('size', self.size)

        elem.text = self.text
        return elem
