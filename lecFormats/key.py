#!/usr/bin/env python
import os

class FileReadError(Exception): pass

class KeyFile(object):
    def __init__(self, file_name=None):
        self.file_name = file_name

        self.key_data = {}
        self.fps = None
        self.frames = None
        self.joints = None

        self._section = None

    def readKeyData(self):
        '''
        Reads the key data from the file
        '''
        f = open(self.file_name)
        reading = True
        while reading:
            if not self._section:
                line = f.readline()
                if line == '':
                    # End of file, stop reading
                    reading = False
                    break
                stripline = line.strip()
                if not stripline or stripline.startswith('#'):
                    # ignore comments and blank lines
                    continue
                if stripline.startswith('SECTION'):
                    self._section = line.split('SECTION: ')

            # Start the right reader
            if self._section == 'HEADER':
                self._readHeader(f)
            elif self._section == 'MARKERS':
                self._readMarkers(f)
            elif self._section == 'KEYFRAME NODES':
                self._readKeyNode(f)
        f.close()
    
    def readHeader(self, f):
        '''
        Reads the header section
        '''
        reading = True
        while reading:
            line = f.readline()
            if line == '':
                raise FileReadError('Premature end of file reached')
            stripline = line.strip()
            if not stripline or stripline.startswith('#'):
                # Skip comment lines or blank lines
                continue


                


