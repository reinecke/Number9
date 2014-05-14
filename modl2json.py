import json, random

from lecFormats import modl

METADATA_GENERATED_BY = "Number 9 Converter"

# Three.js face definition flags
TRIANGLE = 0
QUAD = 1
FACE_MATERIAL = 1 << 1
FACE_UV = 1 << 2
FACE_VERTEX_UV = 1 << 3
FACE_NORMAL = 1 << 4
FACE_VERTEX_NORMAL = 1 << 5
FACE_COLOR = 1 << 6
FACE_VERTEX_COLOR = 1 << 7

def random_material_dict():
    '''
    returns a randomly generated material
    '''
    return {
	#"DbgColor" : 15658734,
	#"DbgIndex" : 0,
	#"DbgName" : "monster",
	"colorAmbient" : [random.random(), random.random(), random.random()],
	"colorDiffuse" : [random.random(), random.random(), random.random()],
    "colorSpecular" : [random.random(), random.random(), random.random()],
	#"mapDiffuse" : "monster.jpg",
	#"mapDiffuseWrap" : ["repeat", "repeat"],
	"shading" : "Lambert",
	"specularCoef" : 50,
	#"transparency" : 1.0,
	"vertexColors" : False
	}

def face_list_for_mesh(mesh, material_index_map = None):
    '''
    given a ModlMesh object, returns a face list for the Three.js json
    format.

    if material_index_map is provided, the keys should be the index of the
    original material and values should be the new material index to use
    '''
    faces = []
    for face in mesh.faces:
        # Identify the vert count
        vert_count = len(face.vertex_indices)
        if vert_count == 3:
            face_flags = TRIANGLE
        elif vert_count == 4:
            face_flags = QUAD
        else:
            # TODO: Tessellate here?
            print "unsupported face count:", vert_count
            continue
        
        # Determine if we'll be writing a material index
        if face.has_material:
            face_flags |= FACE_MATERIAL
        
        faces.append(face_flags)
        faces.extend(face.vertex_indices)
        
        # add the material index
        if face.has_material:
            if material_index_map is None:
                mat_idx = face.material_index
            else:
                mat_idx = material_index_map.get(face.material_index, 0)
            faces.append(mat_idx)
    
    return faces

def modl_mesh_to_dict(mesh, material_index_map = None):
    '''
    given a ModlMesh object, returns a dictionary suitable for conversion
    to Three.js json.

    if material_index_map is provided, the keys should be the index of the
    original material and values should be the new material index to use
    '''
    mesh_dict = {"metadata" :
        {
        "formatVersion" : 3,
        "generatedBy"   : METADATA_GENERATED_BY,
        #"vertices"      : 444,
        #"faces"         : 884,
        #"normals"       : 444,
        #"colors"        : 0,
        #"uvs"           : 322,
        #"materials"     : 1,
        #"morphTargets"  : 24
        },
        # Grim models were rediculously small, make 'em bigger
        "scale" : 0.001
    }
    mesh_dict['name'] = mesh.name

    # Create the flat vert and uv list
    mesh_dict['vertices'] = reduce(lambda x,y:x+list(y), mesh.vertices, [])
    mesh_dict['uvs'] = [reduce(lambda x,y:x+list(y), mesh.texture_vertices, 
        [])]

    # Create the face index list
    mesh_dict['faces'] = face_list_for_mesh(mesh, material_index_map)

    return mesh_dict

def convert_manny():
    # seed the random generator to keep stable output between runs
    random.seed("Manny Calavera")

    # Load manny through the LECFormats modl parser
    manny = modl.ModlFile("/Volumes/eric/grim-proj/grim-data/mannysuit.3do")
    
    # grab his head mesh
    head = [m for m in manny.geosets[0].meshes if 'head' in m.name][0]
    
    outdict = modl_mesh_to_dict(head)
    
    outdict['materials'] = [random_material_dict() for i in manny.materials]

    f=open('/Users/eric/Desktop/mannyhead.js', 'w')
    f.write(json.dumps(outdict))
    f.close()

if __name__ == "__main__":
    convert_manny()
