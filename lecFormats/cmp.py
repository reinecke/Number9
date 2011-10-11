#!/usr/bin/env python
import pascalData as pData
class RGBArray(pData.U8IntArray):
    '''
    For reading the pallette info array from CMP files
    '''
    def __init__(self, length):
        # TODO: finish ths
        super(RGBArray, self).__init__(length)
        self.size *= 3
        self.formatString *= 3
        self.length *= 3
    
    def readFromData(self, data, startIndex=0):
        '''
        returns data from data as a map of byte to tuple

        You may specify an index to start reading the data from.
        '''
        byteArray = super(RGBArray, self).readFromData(data, startIndex)
        colors =[]
        for i in range(len(byteArray)/3):
            rIndex = i*3
            gIndex = rIndex+1
            bIndex = gIndex+1
            colors.append((byteArray[rIndex], byteArray[gIndex], 
                byteArray[bIndex]))

        return colors 

class TCmpHeader(pData.DataStructure):
    def __init__(self):
        '''
        array[0..3] of char;    {'CMP ' - notice space after CMP}
        longint;                {Apparently - version = 20 - 2.0?}
        Longint;                {Transparency - If Not 0 then 256 more TTables - transparency tables }
        array[1..52] of byte; {zeros - padding?}
        '''
        super(TCmpHeader, self).__init__()
        self.append(pData.CharArray(4), 'type')
        self.append(pData.LongInt(), 'ver')
        self.append(pData.LongInt(), 'transparency')
        self.append(pData.CharArray(52), 'pad')
        

class TCmpPaletteData(pData.DataStructure):
    def __init__(self):
        '''
        TPalette=array[0..255] of record
        r,g,b:byte;
        '''
        super(TCmpPaletteData, self).__init__()
        self.append(RGBArray(256), 'palette')

class TCmpLightLevelData(pData.DataStructure):
    def __init__(self):
        '''
        TTable=array[0..255] of byte
        '''
        super(TCmpLightLevelData, self).__init__()
        self.append(pData.ByteArray(255), 'light_levels')

class TCmpTransparencyData(pData.DataStructure):
    def __init__(self):
        '''
        TTable=array[0..255] of byte
        '''
        super(TCmpTransparencyData, self).__init__()
        self.append(pData.ByteArray(255), 'transparency')

class CmpFile(object):
    '''
    CMP File structure:
    TCMPHeader
    TPalette
    64 TTables - light levels 0-63
    256 TTables - transparency tables. May not be present
    (TCMPHeader.HasTransparency determines this).
    
    '''
    def __init__(self, cmpFile):
        # Member attributes
        self.file_path = cmpFile
        self.version = None
        self.transparency = None
        self.palette = []
        self.light_levels = []
        self.transparency_data = []
        
        # Read the cmp file
        f = open(cmpFile)
        self._parseHeader(f)
        self._parsePalette(f)
        # self._parseLightLevels(f)
        # self._parseTransparency(f)
        f.close()

    def _parseHeader(self, f):
        '''
        Parses the cmp header
        '''
        header = TCmpHeader()
        dataDict = header.dictFromFile(f)
        if dataDict['type'] != 'CMP ':
            raise TypeError("%s is not a CMP file"%self.file_path)
        self.version = dataDict['ver']
        self.transparency = (dataDict['transparency'] and True) or False

    def _parsePalette(self, f):
        '''
        Parses the cmp pallette data
        '''
        palette = TCmpPaletteData()
        dataDict = palette.dictFromFile(f)
        self.palette = dataDict['palette']

    def _parseLightLevels(self, f):
        '''
        parses the light level tables
        '''
        levelData = TCmpLightLevelData()
        self.light_levels =[]
        for i in range(64):
            self.light_levels.append(levelData.dictFromFile(f)['light_levels'])

    def _parseTransparency(self, f):
        '''
        parses transparency tables
        '''
        if not self.transparency:
            return
        transparencyStruct = TCmpTransparencyData()
        for i in range(255):
            self.transparency_data.append(transparencyStruct.dictFromFile(f)['transparency'])

