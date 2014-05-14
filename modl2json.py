import json, random

from lecFormats import modl

TRIANGLE = 0
QUAD = 1
FACE_MATERIAL = 1 << 1
FACE_UV = 1 << 2
FACE_VERTEX_UV = 1 << 3
FACE_NORMAL = 1 << 4
FACE_VERTEX_NORMAL = 1 << 5
FACE_COLOR = 1 << 6
FACE_VERTEX_COLOR = 1 << 7


def default_material():
    return {
        "DbgColor" : 15658734,
        "DbgIndex" : 0,
        "DbgName" : "dummy",
        "colorDiffuse" : [ 0, 1, 0 ]
    }

def random_rgb_color():
    int_val = (random.randint(0,255), random.randint(0,255), 
            random.randint(0,255))
    float_val = tuple([i/255.0 for i in int_val])
    return float_val, int_val

def convert_manny():
    manny = modl.ModlFile("/Volumes/eric/grim-proj/grim-data/mannysuit.3do")

    head = [m for m in manny.geosets[0].meshes if 'head' in m.name][0]
    
    verts = reduce(lambda x,y:x+list(y), head.vertices, [])
    
    materials = []
    faces = []
    for face in head.faces:
        if len(face.vertex_indices) == 3:
            face_type = TRIANGLE | FACE_MATERIAL
        elif len(face.vertex_indices) == 4:
            face_type = QUAD | FACE_MATERIAL
        else:
            print "unsupported face count"
            continue
        
        faces.append(face_type)
        faces.extend(face.vertex_indices)

        # Generate and add material
        mat_color_float, mat_color_int = random_rgb_color()
        color_value = (mat_color_int[2] | (mat_color_int[1] << 8) 
                | (mat_color_int[0] << 16))
        mat_index = len(materials)
        mat = {#"DbgColor" : color_value,
        #"DbgIndex" : mat_index,
        #"DbgName" : "mat%d"%mat_index,
        "type": "MeshLambertMaterial",
        #"color" : mat_color_float}
        "color" : color_value,
        "ambient": color_value,
        "emissive": color_value,
        "blending": 0,
        "opacity": 0,
        "transparent": False,
        "wireframe": False}
        
        faces.append(mat_index)
        materials.append(mat)

        
    outdict = {"metadata": {
        "version" : 3,
        #"type":"object",
        "generator":"modl2json"},
        "materials": materials, 
        #"geometries" : [
            #"metadata" : {"version":4.3,
             #       "type":"geometry",
             #       "generator": "modl2json"},
                "vertices":verts, 
                "faces":faces}

    f=open('/Users/eric/Desktop/mannyhead.js', 'w')
    f.write(json.dumps(outdict))
    f.close()

if __name__ == "__main__":
    convert_manny()
