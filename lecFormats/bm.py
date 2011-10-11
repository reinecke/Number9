#!/usr/bin/env python
import Image
import pascalData as pData

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

