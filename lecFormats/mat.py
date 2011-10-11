#!/usr/bin/env python
import struct
import Image, ImageDraw
import pascalData as pData

class TMatHeader(pData.DataStructure):
    '''pascalData DataStructure for main MAT file header data'''
    MAT_TYPE_COLORS = 0
    MAT_TYPE_TEXTURE = 2
    def __init__(self):
        '''
        header schema
        array[0..3] of char;     {'MAT ' - notice space after MAT}
        ver:Longint;             {Apparently - version = 0x32 ('2')}
        Type:Longint;            {0 = colors(TColorHeader) , 1= ?, 2= texture(TTextureHeader)}
        NumOfTextures:Longint;   {number of textures or colors}
        NumOfTextures1: Longint; { In color MATs, it's 0, in TX ones, it's equal to numOfTextures }
        Longint;                 { = 0 }
        LongInt;                 { = 8 }
        array[0..11]of longint;  {unknown. Some pad?}
        '''    
        super(TMatHeader, self).__init__()
        self.append(pData.CharArray(4), 'type')
        self.append(pData.LongInt(), 'ver')
        self.append(pData.LongInt(), 'mat_type')
        self.append(pData.LongInt(), 'count')
        self.append(pData.LongInt(), 'texture_count')
        self.append(pData.LongInt(), 'unknown1')
        self.append(pData.LongInt(), 'unknown2')
        self.append(pData.LongIntArray(12), 'unknown3')

class TMatColorHeader(pData.DataStructure):
    '''pascalData DataStructure for color MAT file header data'''
    def __init__(self):
        '''
        textype:longint;         {0 = color, 8= texture}
        colornum:longint;        {Color index from the CMP palette}
        array[0..3]of Longint;   {each = 0x3F800000 (check cmp header )}
        '''
        super(TMatColorHeader, self).__init__()
        self.append(pData.LongInt(), 'texture_type')
        self.append(pData.LongInt(), 'color_num')
        self.append(pData.LongIntArray(4), 'check_cmp_header')

class TMatTextureHeader(pData.DataStructure):
    '''pascalData DataStructure for texture MAT file header data'''
    def __init__(self):
        '''
        textype:longint;         {0 = color, 8= texture}
        colornum:longint;        {unknown use}
        array[0..3]of Longint;   {each longint = 0x3F800000 (check cmp header )}
        array[0..1]of Longint;   {unknown}
        Longint;                 {=0xBFF78482}
        CurrentTXNum:Longint     {number of corresponding texture, beginning with 0, ranging to NumOfTextures-1}
        '''
        super(TMatTextureHeader, self).__init__()
        self.append(pData.LongInt(), 'texture_type')
        self.append(pData.LongInt(), 'color_num')
        self.append(pData.LongIntArray(4), 'check_cmp_header')
        self.append(pData.LongIntArray(2), 'unknown')
        self.append(pData.LongInt(), 'unknown2')
        self.append(pData.LongInt(), 'current_tex_num')

class TMatTextureDataHeader(pData.DataStructure):
    '''pascalData DataStructure for MAT texture data header'''
    def __init__(self):
        '''
        SizeX:Longint;             {horizontal size of first MipMap, must be divisable by 2}
        SizeY:Longint;             {Vertical size of first MipMap ,must be divisable by 2}
        Pad:array[0..2]of LongInt; {padding = 0 }
        NumMipMaps:LongInt;        {Number of mipmaps in texture largest one first.}

        The TMatTextureDataHeader is followed by actual texture data.
        The graphics are uncompressed; the top left corner is the start; lines are read first.
        The main texture is directly followed by rest MipMaps (whole number is NumMipMaps).
        '''
        super(TMatTextureDataHeader, self).__init__()
        self.append(pData.LongInt(), 'sizeX')
        self.append(pData.LongInt(), 'sizeY')
        self.append(pData.LongIntArray(3), 'pad')
        self.append(pData.LongInt(), 'mipMap_count')

class MatTexture(object):
    '''Represents a texture map'''
    TEXTURE_TYPE_COLOR = 0
    TEXTURE_TYPE_TEXTURE = 8
    def __init__(self, mat_file):
        self.file_path = mat_file
        self.texture_id = None
        self.texture_data = []
        self.texture_type = None
        self.sizeX = None
        self.sizeY = None
        self.numMipMaps = None
        self.dataStart = None

    def textureImage(self, refCmp):
        '''
        Returns a PIL image object for the texture.
        refCmp is the CmpFile object that will be used for the color palette.
        '''
        f = open(self.file_path)
        f.seek(self.dataStart)
        data = f.read(self.sizeX*self.sizeY)
        f.close()
        
        # Create the image object
        if refCmp.transparency:
            mode = 'RGBA'
        else:
            mode = 'RGB'

        # @TODO: use a PIL native Palette image object and give it the cmp
        img = Image.new(mode,(self.sizeX,self.sizeY))
        draw = ImageDraw.Draw(img)

        for i,pixel in enumerate(data):
            x = i%self.sizeX
            # Rely on the floor behavior of python integer division
            y = i/self.sizeX

            # Handle mapping pixel data through the cmp palette
            pixelIndex = struct.unpack('B',pixel)[0]
            
            # zero index is transparent
            if pixelIndex == 0:
                # @TODO: implement pixel transparency handling?
                continue

            # Draw the pixel
            color = refCmp.palette[pixelIndex]
            draw.point((x,y),fill=color)
        del(draw)

        return img

class MatFile(object):
    '''
    Class for reading mat files from Lucasarts games
    '''

    '''
    All MAT file info comes from: http://jeffz.name/jkspecs_v04/

    File structure:
    {Color MAT}
    MATHeader
    ColorHeaders

    {Texture MAT}
    MATHeader
    TextureHeaders
    TextureDatas
    '''
    def __init__(self, mat_path):
        self.file_path = mat_path
        self.version = None
        self.mat_type = None
        self.count = None
        self.is_texture_mat = None

        self.textures = []
        
        # Read the mat metadata
        f = open(mat_path)
        self._getHeader(f)
        if self.mat_type == TMatHeader.MAT_TYPE_COLORS:
            raise Exception("Color Mat not implemented")
        self._getTextureHeaders(f)
        self._getTextureDataHeaders(f)
        f.close()
    
    def _getHeader(self, f):
        '''
        Reads the mat header
        '''
        header = TMatHeader()
        headerDict = header.dictFromFile(f)
        if headerDict['type'] != 'MAT ':
            raise TypeError("%s is not a MAT file"%self.file_path)
        self.version = headerDict['ver']
        self.mat_type = headerDict['mat_type']
        self.count = headerDict['count']

    def _getTextureHeaders(self, f):
        txHeaderReader = TMatTextureHeader()

        # There is one header per map
        for tex in range(self.count):
            txHeader = txHeaderReader.dictFromFile(f)
            tx = MatTexture(self.file_path)
            tx.texture_id = txHeader['current_tex_num']
            tx.texture_type = txHeader['texture_type']
            self.textures.append(tx)

    def _getTextureDataHeaders(self, f):
        reader = TMatTextureDataHeader()

        for i in range(self.count):
            tx = self.textures[i]
            txDataHeader = reader.dictFromFile(f)
            tx.sizeX = txDataHeader['sizeX']
            tx.sizeY = txDataHeader['sizeY']
            tx.numMipMaps = txDataHeader['mipMap_count']
            tx.dataStart = f.tell()

            # Seek past the texture map for the next header
            f.seek(tx.sizeX*tx.sizeY,1)

