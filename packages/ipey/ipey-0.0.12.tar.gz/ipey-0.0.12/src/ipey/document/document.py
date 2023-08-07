from collections import defaultdict
from typing import Tuple
from ipey.document import Writer
from ipey.primitive import Primitive
from ipey.document import Page
import xml.etree.ElementTree as ET
import sys

class Margin:
    '''
    Wrapper class for document margin property.
    '''
    def __init__(self, top=64, bottom=64, left=64, right=64):
        '''
        Initialize a margin wrapper object with values for the four margins
        '''
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

class Document:
    '''
    Representation for an IPE drawing. 
    '''

    def __init__(self, settings_path=None, styles=[]) -> None:
        '''
        Initialize a new document object.

        Parameters:
        settings_path (str): not really required ATM
        styles (list(str)): list of paths to style sheets.

        Returns:
        None
        '''
        self.Writer = Writer(settings_path, styles)
        self.Pages = []
        self.crop = False
        self.width = 595
        self.height = 842
        self.margin = Margin()

    def clear(self) -> None:
        '''
        Clear the document object of all pages.
        
        Parameters:
        None

        Returns:
        None
        '''
        self.Pages = []

    def createPage(self) -> Page:
        '''
        Create a new page in the drawing and add it to the end of the page list.

        Parameters:

        Returns:
        (Page): Page object
        '''
        page = Page()
        self.Pages.append(page)

        return page

    def copyPage(self, page : Page) -> Page:
        '''
        Copy a given page and return a new page with the same structure. Add the new page to the list of pages.

        Parameters:
        page (Page): The page to be copied.

        Returns:
        (Page): The newly created page
        '''
        newPage = page.copyA()
        self.Pages.append(newPage)

        return newPage

    def getSize(self) -> Tuple[Tuple[int, int]]:
        '''
        Get the rectangular bounding box of all elements in the document.

        Parameters:

        Returns:
        ((int,int), (int,int)): Returns a tuple of points (x_min,y_min),(x_max,y_max) that represents the bounding box of the drawing
        '''
        minX = sys.maxsize
        maxX = -sys.maxsize - 1
        minY = sys.maxsize
        maxY = -sys.maxsize - 1

        if self.crop:
            for page in self.Pages:
                for elem in page.Scene:
                    (p1, p2) = elem.getBB()
                    minX = min(minX, p1[0], p2[0])
                    maxX = max(maxX, p1[0], p2[0])
                    minY = min(minY, p1[1], p2[1])
                    maxY = max(maxY, p1[1], p2[1])

            Primitive.xP = self.margin.left - minX
            Primitive.yP = self.margin.bottom - minY
            # for page in self.Pages:
            #     for elem in page.Scene:
            #         elem.pX = self.margin.left - minX
            #         elem.pY = self.margin.bottom - minY          

            return ((0, (maxX - minX) + self.margin.right + self.margin.left), (0, (maxY - minY) + self.margin.top + self.margin.bottom))
        else:
            return ((0, self.width), (0, self.height))

    def write(self, path) -> None:
        '''
        Create the drawing and write it to the disk.

        Parameters:
        path (str): path where the created ipe drawing is saved to.
        
        Returns:
        None
        '''
        pages = []
        size = self.getSize()
        colors = dict()

        for page in self.Pages:
            p = page.draw()
            pages.append(p)

            c = page.getColors()
            colors.update(c)
        
        self.Writer.write(pages, path, size, colors)
    