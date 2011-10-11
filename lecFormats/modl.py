#!/usr/bin/env python
import pascalData as pData
class VArray(pData.FloatArray):
    '''
    For reading float vector data from binary files
    
    '''
    def __init__(self, elem_count, length):
        '''
        elem_count specifies how many elements per vector, ex 3 for (x, y ,z)
        length specifies the count of vector items in the array to read
        '''
        super(VArray, self).__init__(length)
        self.elem_count = elem_count
        self.size *= elem_count
        self.formatString *= elem_count
        self.length *= elem_count
    
    def readFromData(self, data, startIndex=0):
        '''
        returns data from data as a map of byte to tuple

        You may specify an index to start reading the data from.
        '''
        floatArray = super(VArray, self).readFromData(data, startIndex)
        vectors =[]
        # @TODO: cache indexing function for speed?
        for i in range(self.length/self.elem_count):
            v = [floatArray[(i*self.elem_count)+j] for j in range(self.elem_count)]
            vectors.append(tuple(v))
        return vectors 

class ModlFile(object):
    '''
    MODL file format for binary 3do files
    '''
    # http://wiki.multimedia.cx/index.php?title=MODL
    def __init__(self, file_name = None):
        self.file_name = file_name

        #init some things
        self.type = None
        self.materials = []
        self.name = None
        self.geosets = []
        self.nodes = []

        # Read the file
        if not self.file_name:
            return
        f=open(self.file_name)
        self.readFromFile(f)
        print "there are", len(f.read()), "leftover bytes"
        f.close()

    def readFromFile(self, f):
        '''
        Reads the MODL from file into memory
        '''
        # Grab the header data
        headerData = TModlHeader().dictFromFile(f)
        self.type = headerData['type']
        self.name = headerData['name']
        self.materials = headerData['mat_names']
        del(headerData)
        
        geosetHeader = TModlGeosetHeader().dictFromFile(f)
        self.geosets = []
        for i in range(geosetHeader['geoset_count']):
            geoset = ModlGeoset(self)
            geoset.readFromFile(f)
            self.geosets.append(geoset)
        
        node_count = TModlNodeHeader().dictFromFile(f)['node_count']
        self.nodes =[]
        for i in range(node_count):
            node = ModlNode()
            node.readFromFile(f)
            self.nodes.append(node)

        footer = TModlFooter().dictFromFile(f)
        self.model_radius = footer['model_radius']
        self.insertion_offset = footer['insertion_offset']
        

class ModlGeoset(object):
    def __init__(self, modlFile):
        self.modlFile = modlFile
        self.meshes = []
    
    def readFromFile(self, f):
        mesh_count = pData.LongInt().readFromFile(f)
        self.meshes = []
        for i in range(mesh_count):
            mesh = ModlMesh(self.modlFile)
            mesh.readFromFile(f)
            self.meshes.append(mesh)


class TModlHeader(pData.DataStructure):
    def __init__(self):
        '''
        "MODL" FOURCC           |4 bytes
        number of materials used|4 bytes
        '''    
        super(TModlHeader, self).__init__()
        self.append(pData.CharArray(4), 'type')
        self.append(pData.LongInt(), 'mat_count')

    def dictFromFile(self, f):
        data = super(TModlHeader, self).dictFromFile(f)
        
        # Read the material names
        matNameReader = pData.DataStructure()
        matNameReader.append(pData.CharArray(32), 'mat_name')
        matNames = [matNameReader.dictFromFile(f)['mat_name'] for 
                i in range(data['mat_count'])]
        data['mat_names'] = matNames
        
        '''
        3d model name|32 bytes, string
        '''
        modelNameReader = pData.DataStructure()
        name = pData.CharArray(32).readFromFile(f)
        data['name'] = name

        return data

# class TModlMaterial(pData.DataStructure):
    # def __init__(self):
        # '''
        # material name|32 bytes, string

        # one per material
        # '''    
        # super(TModlMaterials, self).__init__()
        # self.append(pData.CharArray(32), 'mat_name')

# class TModlName(pData.DataStructure):
    # def __init__(self):
        # '''
        # 3d model name|32 bytes, string
        # '''    
        # super(TModlName, self).__init__()
        # self.append(pData.CharArray(32), 'name')

class TModlGeosetHeader(pData.DataStructure):
    def __init__(self):
        '''
        unknown          |4 bytes
        number of geosets|4 bytes
        '''
        super(TModlGeosetHeader, self).__init__()
        self.append(pData.LongInt(), 'unknown')
        self.append(pData.LongInt(), 'geoset_count')

class TModlNodeHeader(pData.DataStructure):
    def __init__(self):
        '''
        unknown        |4 bytes
        number of nodes|4 bytes
        '''
        super(TModlNodeHeader, self).__init__()
        self.append(pData.LongInt(), 'unknown')
        self.append(pData.LongInt(), 'node_count')

class ModlNode(object):
    def __init__(self):
        self.name = None

    def __str__(self):
        return "<modl.ModlNode '%s'>"%str(self.name)

    def __repr__(self):
        return str(self)

    def readFromFile(self, f):
        data = TModlNode().dictFromFile(f)
        self.name = data['name']
        self.flags = data['flags']
        self.type = data['type']
        self.mesh_id = data['mesh_id']
        self.depth = data['depth']
        self.has_parent = data['has_parent'] != 0
        self.child_count = data['child_count']
        self.has_children = data['has_children'] != 0
        self.has_sibling = data['has_sibling'] != 0
        self.pivot = data['pivot']
        self.position = data['position']
        self.pitch = data['pitch']
        self.yaw = data['yaw']
        self.roll = data['roll']
        
        self.parent_id = data.get('parent_id')
        self.child_id = data.get('child_id')
        self.sibling_id = data.get('sibling_id')

class TModlNode(pData.DataStructure):
    def __init__(self):
        '''
        name                      |64 bytes, string
        flags                     |4 bytes
        unknown                   |4 bytes
        type                      |4 bytes
        mesh id                   |4 bytes
        depth                     |4 bytes
        has parent?               |4 bytes
        number of children        |4 bytes
        has children?             |4 bytes
        has sibling?              |4 bytes
        pivot                     |vector3
        position                  |vector3
        pitch                     |4 bytes, float
        yaw                       |4 bytes, float
        roll                      |4 bytes, float
        unknown                   |48 bytes (whoa!)
        if has parent, parent id  |4 bytes
        if has child, child id    |4 bytes
        if has sibling, sibling id|4 bytes
        '''
        super(TModlNode, self).__init__()
        self.append(pData.CharArray(64), 'name')
        self.append(pData.LongInt(), 'flags')
        self.append(pData.LongInt(), 'unknown', True)
        self.append(pData.LongInt(), 'type')
        self.append(pData.LongInt(), 'mesh_id')
        self.append(pData.LongInt(), 'depth')
        self.append(pData.LongInt(), 'has_parent')
        self.append(pData.LongInt(), 'child_count')
        self.append(pData.LongInt(), 'has_children')
        self.append(pData.LongInt(), 'has_sibling')
        self.append(pData.FloatArray(3), 'pivot')
        self.append(pData.FloatArray(3), 'position')
        self.append(pData.Float(), 'pitch')
        self.append(pData.Float(), 'yaw')
        self.append(pData.Float(), 'roll')
        self.append(pData.LongIntArray(12), 'unknown2', True)

    def dictFromFile(self, f):
        data = super(TModlNode, self).dictFromFile(f)
        if data['has_parent']:
            data['parent_id'] = pData.LongInt().readFromFile(f)
        if data['has_children']:
            data['child_id'] = pData.LongInt().readFromFile(f)
        if data['has_sibling']:
            data['sibling_id'] = pData.LongInt().readFromFile(f)
        return data

class TModlFooter(pData.DataStructure):
    def __init__(self):
        '''
        model radius                |4 bytes, float
        insertion offset (see notes)|vector3
        '''        
        super(TModlFooter, self).__init__()
        self.append(pData.Float(), 'model_radius')
        self.append(pData.FloatArray(3), 'insertion_offset')

# class TModlPerGeosetHeader(pData.DataStructure):
    # def __init__(self):
        # '''
        # number of meshes|4 bytes

        # one per geoset
        # '''
        # super(TModlPerGeosetHeader, self).__init__()
        # self.append(pData.LongInt(), 'mesh_count')

class ModlMesh(object):
    def __init__(self, modlFile):
        self.modlFile = modlFile
        self.name = None
        self.geometry_mode = None
        self.lighting_mode = None
        self.texture_mode = None
        self.vertices = []
        self.texture_vertices = []
        self.extra_light = None
        self.vertex_normals = []
        self.has_shadow = None
        self.mesh_radius = None

    def __str__(self):
        return "<modl.ModlMesh '%s'>"%str(self.name)

    def __repr__(self):
        return str(self)

    def readFromFile(self, f):
        meshReader = TModlMesh()
        data = meshReader.dictFromFile(f)
        self.name = data['mesh_name']
        self.geometry_mode = data['geometry_mode']
        self.lighting_mode = data['lighting_mode']
        self.texture_mode = data['texture_mode']
        self.vertices = data['vertices']
        self.texture_vertices = data['texture_vertices']
        self.faces = data['faces']
        self.extra_light = data['extra_light']
        self.vertex_normals = data['vertex_normals']
        self.has_shadow = data['has_shadow']
        self.mesh_radius = data['mesh_radius']
        
    def writeObjToFile(self, f):
        '''
        Writes the mesh data to an open file in obj format
        '''
        # Write the object name
        f.write('o '+self.name+'\n\n')

        # Write the verts
        for vert in self. vertices:
            f.write('v '+' '.join(["%6f"%axis for axis in vert])+'\n')
        
        # seperate the sections
        f.write('\n')

        # write the texture coordinates
        for vert in self.texture_vertices:
            f.write('vt '+' '.join(["%6f"%axis for axis in vert])+'\n')
        
        # seperate the sections
        f.write('\n')

        # Write the vertex normals out
        for normal in self.vertex_normals:
            f.write('vn '+' '.join(["%6f"%axis for axis in normal])+'\n')
        
        # seperate the sections
        f.write('\n')

        # group the faces by material
        matMap = [(i,face.material_index) for i,face in enumerate(self.faces)]
        matMap = sorted(matMap, key=lambda x:x[1])

        # Write the face definitions
        currentMat = None
        for face_index, mat_index in matMap:
            # If this face has a different material than the last, tell someone!
            if currentMat != mat_index and mat_index:
                f.write('\nusemtl '+self.modlFile.materials[mat_index])
            currentMat = mat_index

            # Start the face definition
            f.write('\nf')

            # Write each vert index out
            face = self.faces[face_index]
            for i, vertIndex in enumerate(face.vertex_indices):
                # a face definition with texture is:
                #    f vert_index/tx_vert_index/vert_normal_index
                # Otherwise:
                #    f vert_index//vert_normal_index
                if face.has_texture:
                    txCoordIndex = face.texture_vertex_indices[i]
                    params = [vertIndex, txCoordIndex, vertIndex]
                else:
                    params = [vertIndex, '', vertIndex]
                f.write(' '+'/'.join([str(param) for param in params]))

class ModlFace(object):
    def __init__(self):
        self.id = None
        self.type = None
        self.geometry_mode = None
        self.lighting_mode = None
        self.texture_mode = None
        self.has_texture = None
        self.has_material = None
        self.extra_light = None
        self.normal_vector = None
        self.vertex_indices = []
        self.texture_vertex_indices = []
        self.material_index = None
    
    def __str__(self):
        return "<modl.ModlFace '%s'>"%str(self.id)

    def __repr__(self):
        return str(self)

    def readFromFile(self, f):
        faceReader = TModlFace()
        data = faceReader.dictFromFile(f)
        self.id = data['face_id']
        self.type = data['face_type']
        self.geometry_mode = data['geometry_mode']
        self.lighting_mode = data['lighting_mode']
        self.texture_mode = data['texture_mode']
        self.has_texture = data['has_texture']
        self.has_material = data['has_material']
        self.extra_light = data['extra_light']
        self.normal_vector = data['normal_vector']
        self.vertex_indices = data['vertex_indices']
        self.texture_vertex_indices = data.get('texture_vertex_indices')
        self.material_index = data.get('material_index')


        

class TModlMesh(pData.DataStructure):
    def __init__(self):
        '''
        mesh name                            |32 bytes, string
        unknown                              |4 bytes
        geometry mode                        |4 bytes
        lighting mode                        |4 bytes
        texture mode                         |4 bytes
        number of mesh vertices              |4 bytes
        number of texture vertices           |4 bytes
        number of faces                      |4 bytes
        '''
        super(TModlMesh, self).__init__()
        self.append(pData.CharArray(32), 'mesh_name')
        self.append(pData.LongInt(), 'unknown')
        self.append(pData.LongInt(), 'geometry_mode')
        self.append(pData.LongInt(), 'lighting_mode')
        self.append(pData.LongInt(), 'texture_mode')
        self.append(pData.LongInt(), 'vert_count')
        self.append(pData.LongInt(), 'texture_vert_count')
        self.append(pData.LongInt(), 'face_count')

    def dictFromFile(self, f):
        # Get the variable length data
        '''
        mesh vertex data                     |vector3 * number of mesh vertices
        texture vertex data                  |vector2 * number of texture vertices
        extra light data (see notes)         |float * number of mesh vertices
        unknown                              |4 bytes * number of mesh vertices        
        '''
        data = super(TModlMesh, self).dictFromFile(f)
        meshReader = pData.DataStructure()
        meshReader.append(VArray(3, data['vert_count']), 'vertices')
        meshReader.append(VArray(2, data['texture_vert_count']), 'texture_vertices')
        '''
        Extra-light values are used to as additional brightness values that are added to
        their corresponding vertex brightness value. This way, for example, for a given
        vertex v, an illumination value of 0.5 will increase v's brightness by 0.5.
        Illumination values (are floats, and) are in the range [0, 1]. All encountered
        models so far have all illumination values of 0.00.
        '''
        meshReader.append(pData.FloatArray(data['vert_count']), 'extra_light')
        meshReader.append(pData.ByteArray(4*data['vert_count']), 'unknown', True)
        data.update(meshReader.dictFromFile(f))
        faces = []
        # faceReader = TModlFace()
        for i in range(data['face_count']):
            # faces.append(faceReader.dictFromFile(f))
            face = ModlFace()
            face.readFromFile(f)
            faces.append(face)
        data['faces'] = faces
        '''
        mesh vertex normal data              |vector3 * number of mesh vertices
        has shadow                           |4 bytes
        unknown                              |4 bytes
        mesh radius                          |4 bytes
        unknown                              |vector3
        unknown                              |vector3
        '''
        meshReader2 = pData.DataStructure()
        meshReader2.append(VArray(3, data['vert_count']), 'vertex_normals')
        meshReader2.append(pData.LongInt(), 'has_shadow')
        meshReader2.append(pData.LongInt(), 'unknown')
        meshReader2.append(pData.LongInt(), 'mesh_radius')
        meshReader2.append(pData.FloatArray(3), 'unknown2')
        meshReader2.append(pData.FloatArray(3), 'unknown3')

        data.update(meshReader2.dictFromFile(f))

        return data
    

class TModlFace(pData.DataStructure):
    def __init__(self):
        '''
        face id (?)                           |4 bytes
        face type                             |4 bytes
        geometry mode                         |4 bytes
        lighting mode                         |4 bytes
        texture mode                          |4 bytes
        number of vertices                    |4 bytes
        unknown                               |4 bytes
        has texture?                          |4 bytes
        has material?                         |4 bytes
        unknown                               |vector3
        extra light                           |4 bytes, float
        unknown                               |vector3
        normal vector                         |vector3

        '''
        super(TModlFace, self).__init__()
        self.append(pData.LongInt(), 'face_id')
        self.append(pData.LongInt(), 'face_type')
        self.append(pData.LongInt(), 'geometry_mode')
        self.append(pData.LongInt(), 'lighting_mode')
        self.append(pData.LongInt(), 'texture_mode')
        self.append(pData.LongInt(), 'vert_count')
        self.append(pData.LongInt(), 'unknown')
        self.append(pData.LongInt(), 'has_texture')
        self.append(pData.LongInt(), 'has_material')
        self.append(VArray(3,1), 'unknown2')
        self.append(pData.Float(), 'extra_light')
        self.append(VArray(3,1), 'unknown3', True)
        self.append(VArray(3,1), 'normal_vector')

    def dictFromFile(self, f):
        
        # Read data in the standard way
        data = super(TModlFace, self).dictFromFile(f)

        # Use values from that data to read the variable length data
        '''
        mesh vertex indices                   |4 bytes, one per vertex
        if has texture, texture vertex indices|4 bytes, one per texture vertex
        if has material, material index       |4 bytes
        '''
        reader = pData.DataStructure()
        reader.append(pData.LongIntArray(data['vert_count']), 'vertex_indices')
        if data['has_texture']:
            reader.append(pData.LongIntArray(data['vert_count']), 'texture_vertex_indices')
        if data['has_material']:
            reader.append(pData.LongInt(), 'material_index')
        
        # Update the variable data into the dict
        data.update(reader.dictFromFile(f))

        return data


