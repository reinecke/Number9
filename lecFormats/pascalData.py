#!/usr/bin/env python
import os, sys, struct, copy

'''
Pascal units
Byte     = 0 to 255    unsigned 8 bit
Word     = 0 to 65,535 unsigned 16 bit
SmallInt = -32768 to 32767 (signed 16 bit)
LongInt  = -2,147,483,648 to 2,147,483,648 signed 32 bit
Char     =  ( 1 byte) ascii character
String   =  String of ascii character
Boolean  =  True/False
Hexidecimal values are represented as either $01  or  0x01
'''

# pascal unit lengths in bytes
P_BYTE_SZ = 1
P_FLOAT_SZ = 4
P_WORD_SZ = 2
P_SMALLINT_SZ = 2
P_LONGINT_SZ = 4
P_CHAR_SZ = 1

# Format chars for struct by type
P_LONGINT_FMT = 'i'
P_CHAR_FMT = 'c'
P_U8INT_FMT = 'B'
P_BYTE_FMT = 'c'  # Use char for lack of better idea
P_FLOAT_FMT = 'f'

class DataMismatchError(Exception): pass
class DataConversionError(Exception): pass

class PDataType(object):
    '''Abstract class to describe a pascal datatype'''
    def __init__(self):
        self.size = None    # size in bytes of data type
        self.formatString = None  # format string for struct
        self.length = 1   # Number of elements in the struct.unpack tuple
        self.seek_only = False  # If set to true, data reader will advance through data, but
                                # Not store any data

    # def translateFromStructUnpack(self, unpackTuple, startIndex):
        # '''
        # Reads data of this dataType from a tuple returned by struct.unpack.

        # returns a tuple (data, endIndex) where data is python native data
        # as described by this tuple
    
    def readFromFile(self, f):
        '''
        Returns data as type describes byt this dataType from data in f starting from
        the current pointer location. The pointer will be advanced by the size of this data.
        '''
        data = f.read(self.size)
        return self.readFromData(data)

    def readFromData(self, data, startIndex=0):
        '''
        returns data of type described by this dataType translated from
        data.

        You may specify an index to start reading the data from.
        '''
        unpacked = struct.unpack(self.formatString,
                data[startIndex:self.size])
        
        # If this isn't an array type, just return the data
        if self.length == 1:
            return unpacked[0]

        return [item for item in unpacked]


class LongInt(PDataType):
    def __init__(self):
        super(LongInt, self).__init__()
        self.size = P_LONGINT_SZ
        self.formatString = P_LONGINT_FMT

class LongIntArray(PDataType):
    def __init__(self, length):
        super(LongIntArray, self).__init__()
        self.size = length*P_LONGINT_SZ
        self.formatString = P_LONGINT_FMT*length
        self.length = length

class Char(PDataType):
    def __init__(self):
        super(Char, self).__init__()
        self.size = P_CHAR_SZ
        self.formatString = P_CHAR_FMT

class CharArray(PDataType):
    def __init__(self, length):
        super(CharArray, self).__init__()
        self.size = P_CHAR_SZ*length
        self.formatString = P_CHAR_FMT*length
        self.length = length
    
    def readFromData(self, data, startIndex=0):
        '''
        returns data from data as a string.

        You may specify an index to start reading the data from.
        '''
        unpacked = struct.unpack(self.formatString,
                data[startIndex:self.size])
        
        return ''.join([char for char in unpacked if char not in ['\x00', '\xcc']])

class Float(PDataType):
    def __init__(self):
        super(Float, self).__init__()
        self.size = P_FLOAT_SZ
        self.formatString = P_FLOAT_FMT

class FloatArray(PDataType):
    def __init__(self, length):
        super(FloatArray, self).__init__()
        self.size = P_FLOAT_SZ*length
        self.formatString = P_FLOAT_FMT*length
        self.length = length

class Byte(PDataType):
    def __init__(self):
        super(Byte, self).__init__()
        self.size = P_BYTE_SZ
        self.formatString = P_BYTE_FMT

class ByteArray(PDataType):
    def __init__(self, length):
        super(ByteArray, self).__init__()
        self.size = P_BYTE_SZ*length
        self.formatString = P_BYTE_FMT*length
        self.length = length

class U8Int(PDataType):
    def __init__(self):
        super(U8Int, self).__init__()
        self.size = P_BYTE_SZ
        self.formatString = P_U8INT_FMT

class U8IntArray(PDataType):
    def __init__(self, length):
        super(U8IntArray, self).__init__()
        self.size = P_BYTE_SZ*length
        self.formatString = P_U8INT_FMT*length
        self.length = length

class DataStructure(object):
    '''
    Describes a data structure in pascal terms
    The described structure can then be returned as a python dict with
    native python data types
    '''
    def __init__(self):
        self._keyList = []
        self._dataTypeMap = {}

    def append(self, pDataType, key, seek_only=False):
        '''
        Appends a data element to the structure
        '''
        if self._dataTypeMap.has_key(key):
            raise KeyError("key '%s' already exists in struct"%key)

        pDataType.seek_only = seek_only
            
        self._dataTypeMap[key] = pDataType
        self._keyList.append(key)
    
    def dictFromData(self, data):
        '''
        Given an array of data, returns a dictionary processed using this
        structure's description
        '''
        if len(data) != len(self.size):
            msg = 'This struct required data of length %d'%self.size
            raise DataMismatchError(msg)

        # unpack using struct
        # dataTuple = struct.unpack(self.structFormatString, data)

        # load the tuple data to a dictionary
        dataDict = {}
        pos = 0     # Postion in tuple
        for key in self._keyList:
            # Get the dataType object
            dataType = self._dataTypeMap[key]
            
            # Seek ahead by the size of the data
            if dataType.seek_only:
                pos += dataType.size
                dataDict[key] = None
                continue
            
            # convert the data
            convertedData = dataType.readFromData(data, pos)
            pos += dataType.length
            dataDict[key] = convertedData

        return dataDict
    
    def dictFromFile(self, f):
        '''
        Given an opened file object, reads the struct from the file and
        returns a dictionary
        '''
        dataDict = {}
        for key in self._keyList:
            # Get the dataType object
            dataType = self._dataTypeMap[key]
            
            # If this is a seek only, Move pointer ahead
            if dataType.seek_only:
                f.seek(dataType.size ,1)
                dataDict[key] = None
                continue
            
            # Read the needed number of bytes from the file
            data = f.read(dataType.size)

            # Convert the data
            try:
                convertedData = dataType.readFromData(data)
            except struct.error, e:
                msg = 'Could not read data for key "%s", %s'%(key, str(e))
                raise DataConversionError(msg)

            # Add to the dict
            dataDict[key] = convertedData

        return dataDict
    
    def keyList(self):
        '''
        Returns a list of keys in the struct
        '''
        return copy.copy(self._keylist)
    
    def remove(self, key):
        '''removes the data and key from the struct description'''
        del(_dataTypeMap[key])
        self._keylist.remove(key)
    
    @property
    def structFormatString(self):
        '''format string to be used with struct unpacking'''
        return [self._dataTypeMap[key].formatString for
                key in self._keyList]
    
    @property
    def size(self):
        '''size in bytes of the entire struct'''
        return sum([self._dataTypeMap[key].size for
                key in self._keyList])


