import xml.etree.ElementTree as ET
import datetime 
import configparser
import pkg_resources
from xml.dom import minidom
import os

class IpeOptions:
    '''
    Class that encapsulates IPE options. Optionally to initialize with a path to a settings.ini file containing ipe version and creator.
    '''
    def __init__(self, settings_path: str = None):
        config = configparser.ConfigParser()

        if settings_path:
            config.read(settings_path)
        else:
            settings = pkg_resources.resource_filename(__name__, '../static/settings.ini')
            config.read(settings)                                     
        
        self.__dict__['_IPE_VERSION'] = config['IPE']['VERSION']
        self.__dict__['_IPE_CREATOR'] = config['IPE']['CREATOR']



class Writer:

    def __init__(self, settings_path: str = None, styles: list = []):
        self._options = IpeOptions(settings_path)
        self.styles = styles

    def write(self, pages, path, size, colors):
        ipe = ET.Element('ipe')
        ipe.set('version', self._options._IPE_VERSION)
        ipe.set('creator', self._options._IPE_CREATOR)

        info = ET.SubElement(ipe, 'info')

        timeNow = datetime.datetime.now().strftime("%Y%M%d%H%M%S")
        info.set('created', f'D:{timeNow}')
        info.set('modified' , f'D:{timeNow}')

        self.appendStyle(ipe, self.styles)
        self.appendSize(ipe, size)
        self.appendColors(ipe, colors)

        for page in pages:
            ipe.append(page)

        xmlPath= os.path.join('' , path) 
        xmlstr= minidom.parseString(ET.tostring(ipe)).toprettyxml(indent = "   ")
        with open(xmlPath, "w") as f:
            f.write(xmlstr)
            f.close()

    def appendSize(self, ipe, size):
        pagesize = ET.SubElement(ipe, 'ipestyle') 
        layout = ET.SubElement(pagesize, 'layout')
        layout.set('paper', f'{size[0][1]} {size[1][1]}')
        layout.set('origin', f'0 0')
        layout.set('frame', f'{size[0][1]} {size[1][1]}') 

    def appendStyle(self, ipe, styles):
        '''
        Append a list of given stylesheets to the ipe drawing.
        '''
        basicPath = pkg_resources.resource_filename(__name__, '../static/basic.xml')
        basic = ET.parse(basicPath).getroot()
        ipe.append(basic)

        for style in styles:
            s = ET.parse(style).getroot()
            ipe.append(s)

    def appendColors(self, ipe, colors : dict):
        '''
        Appends a list of given hex colors to the styles.
        '''

        cStyle = ET.SubElement(ipe, 'ipestyle')
        cStyle.set('name', 'customColors')

        for name, color in colors.items():
            c = ET.SubElement(cStyle, 'color')
            c.set('name', name)
            c.set('value', color)