#!/usr/bin/env python
from modl import ModlFile

# None of the image libs work without PIL
# I run into this with maya
try:
    from bm import BmImage
    from bm import BmFile
    from cmp import CmpFile
    from mat import MatTexture
    from mat import MatFile
except ImportError:
    pass

import os

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
    
