#!/usr/bin/env python
import os, sys, struct
import Image, ImageDraw
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

class TBmHeader(pData.DataStructure):
    '''pascalData DataStructure for main BM file header data'''
    def __init__(self):
        '''
        FileType    : array[0..2] of char;     // 'BM ' - notice space after BM
        Ver         : Byte;                    // Apparently version = $20 - 2.0?
        Unknown1    : Longint;                 // = $46
        Unknown2    : Longint;                 // = 0
        PalInc      : Longint;                 // 0, 1 or 2 ;  2 = palette included
        NumImages   : Longint;                 // number of images in file
        XOffset     : Longint;                 // X-offset (for overlaying on other BMs)
        YOffset     : Longint;                 // Y-offset (for overlaying on other BMs)
        Transparent : Longint;                 // Transparent colour
        Uk3         : Longint;                 // = 1 in 16-bit BMs, = 0 in 8-bit BMs
        NumBits     : Longint;                 // 8 = 8-bit BM, 16 = 16-bit BM
        BlueBits    : Longint;                 // = 5 for 16-bit BMs, else = 0
        GreenBits   : Longint;                 // = 6 for 16-bit BMs, else = 0
        RedBits     : Longint;                 // = 5 for 16-bit BMs, else = 0
        Uk4         : Longint;                 // = 11 in 16-bit BMs, else = 0
        Uk5         : Longint;                 // = 5 in 16-bit BMs, else = 0
        Uk6         : Longint;                 // = 0
        Uk7         : Longint;                 // = 3 in 16-bit BMs, else = 0
        Uk8         : Longint;                 // = 2 in 16-bit BMs, else = 0
        Uk9         : Longint;                 // = 2 in 16-bit BMs, else = 0
        Padding     : Array[0..12] of Longint; // = 0
        '''
        super(TBmHeader, self).__init__()
        self.append(pData.CharArray(3), 'type')
        self.append(pData.U8Int(), 'ver')
        self.append(pData.LongInt(), 'unknown1')
        self.append(pData.LongInt(), 'unknown2')
        self.append(pData.LongInt(), 'palette_included')
        self.append(pData.LongInt(), 'count')
        self.append(pData.LongInt(), 'offsetX')
        self.append(pData.LongInt(), 'offsetY')
        self.append(pData.LongInt(), 'transparent_color')
        self.append(pData.LongInt(), 'uk3')
        self.append(pData.LongInt(), 'bit_depth')
        self.append(pData.LongInt(), 'blue_bits')
        self.append(pData.LongInt(), 'green_bits')
        self.append(pData.LongInt(), 'red_bits')
        self.append(pData.LongInt(), 'uk4')
        self.append(pData.LongInt(), 'uk5')
        self.append(pData.LongInt(), 'uk6')
        self.append(pData.LongInt(), 'uk7')
        self.append(pData.LongInt(), 'uk8')
        self.append(pData.LongInt(), 'uk9')
        self.append(pData.LongIntArray(13), 'pad')

class TBmImageHeader(pData.DataStructure):
    '''pascalData DataStructure for BM texture data header'''
    def __init__(self):
        '''
        sizeX  :  Longint;                  // Image horizontal size in pixels
        sizeY  :  Longint;                  // Image vertical size in pixels
        '''        
        super(TBmImageHeader, self).__init__()
        self.append(pData.LongInt(), 'sizeX')
        self.append(pData.LongInt(), 'sizeY')

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

class ModlFile(object):
    '''
    MODL file format for binary 3do files
    '''
    # http://wiki.multimedia.cx/index.php?title=MODL

class BmImage(object):
    def __init__(self):
        self.file_path = None
        self.bit_depth = None
        self.dataStart = None
        self.sizeX = None
        self.sizeY = None
    
    def image(self):
        '''returns an image object for this'''
        f = open(self.file_path)
        f.seek(self.dataStart)
        bytesPerPixel = (self.bit_depth/8)

        data = f.read(bytesPerPixel*self.sizeX*self.sizeY)
        print bytesPerPixel*self.sizeX*self.sizeY, len(data)
        f.close()
        
        mode = 'F;'+str(self.bit_depth)
        print mode
        image = Image.fromstring('F', (self.sizeX,self.sizeY), data, "raw", mode)
        return image

        # for pixel in range((self.sizeX*sizeY)/bytesPerPixel):
            # pixelData = struct.unpack(
# @TODO: implement image data decompression
# static void decompress_codec3(const char *compressed, char *result) {
    # int bitstr_value = READ_LE_UINT16(compressed);
    # int bitstr_len = 16;
    # compressed += 2;
    # bool bit;

    # for (;;) {
        # GET_BIT;
        # if (bit == 1)
            # *result++ = *compressed++;
        # else {
            # GET_BIT;
            # int copy_len, copy_offset;
            # if (bit == 0) {
                # GET_BIT;
                # copy_len = 2 * bit;
                # GET_BIT;
                # copy_len += bit + 3;
                # copy_offset = *(uint8 *)(compressed++) - 0x100;
            # } else {
                # copy_offset = (*(uint8 *)(compressed) | (*(uint8 *)(compressed + 1) & 0xf0) << 4) - 0x1000;
                # copy_len = (*(uint8 *)(compressed + 1) & 0xf) + 3;
                # compressed += 2;
                # if (copy_len == 3) {
                    # copy_len = *(uint8 *)(compressed++) + 1;
                    # if (copy_len == 1)
                        # return;
                # }
            # }
            # while (copy_len > 0) {
                # *result = result[copy_offset];
                # result++;
                # copy_len--;
            # }
        # }
    # }
# }


class BmFile(object):
    def __init__(self, bmFile):
        self.file_path = bmFile
        self.bit_depth = None
        self.image_count = None
        self.version = None
        self.offsetX = None
        self.offsetY = None
        self.transparent_color = None

        self.images = []
        f = open(bmFile)
        self._parseHeader(f)
        self._parseDataHeaders(f)
        f.close()

    def _parseHeader(self, f):
        headerParser = TBmHeader()
        header = headerParser.dictFromFile(f)
        if header['type'] != 'BM ':
            raise TypeError("%s is not a valid BM file"%self.file_path)
        self.bit_depth = header['bit_depth']
        self.image_count = header['count']
        self.version = header['ver']
        self.offsetX = header['offsetX']
        self.offsetY = header['offsetY']
        self.transparent_color = header['transparent_color']

    def _parseDataHeaders(self, f):
        dataHeaderParser = TBmImageHeader()
        for i in range(self.image_count):
            header = dataHeaderParser.dictFromFile(f)
            img = BmImage()
            img.file_path = self.file_path
            img.bit_depth = self. bit_depth
            img.sizeX = header['sizeX']
            img.sizeY = header['sizeY']
            img.dataStart = f.tell()
            self.images.append(img)

            # Jump past the data for the next header
            f.seek(img.sizeX*img.sizeY*(img.bit_depth/8), 1)


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
                print "Warning: transparent pixel ignored"
                # @TODO: implement pixel transparency handling
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
        
        # Read the mat data
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

# f = open('grim-data/m_s_chest.mat')
# matHeader = TMatHeader().dictFromFile(f)
# print "matHeader", matHeader
# if matHeader['mat_type'] == TMatHeader.MAT_TYPE_COLORS:
    # colorHeader = TColorHeader().dictFromFile(f)
    # print "color header:", colorHeader
# else:
    # texHeaders =[]
    # for tex in range(matHeader['texture_count']):
        # texHeaders.append(TMatTextureHeader().dictFromFile(f))
    # print "texture headers:", texHeaders
    # 
    # print "first texture:", TMatTextureDataHeader().dictFromFile(f)

def convertTextures(matFiles, cmpPath, outdir):
    suitCmp = CmpFile(cmpPath)
    for matPath in matFiles:
        mat = MatFile(matPath)
        for tx in mat.textures:
            im = tx.textureImage(suitCmp)
            imPath = os.path.join(outdir, os.path.splitext(os.path.basename(matPath))[0])
            if mat.count > 1:
                imPath+='-'+str(tx.texture_id)
            imPath += '.tif'
            im.save(imPath, 'TIFF')
    
