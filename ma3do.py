#!/usr/bin/env python
import maya.cmds as cmds
import os, sys, tempfile
sys.path = ['/Users/eric/grim-proj'] + sys.path
from lecFormats import modl
from lecFormats import mat

#select -r m_chest1_PLY.f[1] ;
#select -tgl m_chest1_PLY.f[19] ;
#sets -e -forceElement lambert2SG;

def buildMatNetwork(name):
    '''
    Builds a network up for a 2D texture file using the base name provided

    Returns a dictionary:
    shadingGroup - the shadingGroup
    lambert      - The lambert
    file         - file node
    place2d      - the place2dTexture node
    '''
    # Pre-condition the name to suppress warnings
    name = name.replace('.','_')
    
    # Create the lambert
    lambert = cmds.shadingNode("lambert", asShader=True, n=name+"_lambert")
    
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True,
            name=name)
    cmds.connectAttr(lambert+'.outColor', sg+'.surfaceShader', f=True)
    
    #cmds.defaultNavigation(createNew=True, destination=lambert+".color")
    #cmds.createRenderNode(allWithTexturesUp="defaultNavigation -force true -connectToExisting -source %node -destination lambert2.color" "";
    #defaultNavigation -defaultTraversal -destination "lambert2.color";
    
    fileIn = cmds.shadingNode("file", asTexture=True, name=name+'_file')
    place2d = cmds.shadingNode("place2dTexture", asUtility=True, 
            name = name+"_place")
    
    # Connect up the nodes
    attrList = [".coverage", ".translateFrame", ".rotateFrame", ".mirrorU",
            ".mirrorV", ".stagger", ".wrapU", ".wrapV", ".repeatUV",
            ".offset", ".rotateUV", ".noiseUV", ".vertexUvOne",
            ".vertexUvTwo", ".vertexUvThree", ".vertexCameraOne"]
    for attr in attrList:
        cmds.connectAttr(place2d+attr, fileIn+attr, f=True)
    cmds.connectAttr(place2d+".outUV", fileIn+".uv")
    cmds.connectAttr(place2d+".outUvFilterSize", fileIn+".uvFilterSize")

    #defaultNavigation -force true -connectToExisting -source file1 -destination lambert2.color;
    cmds.connectAttr(fileIn+".outColor", lambert+".color", f=True)

    return {'shadingGroup':sg, 'lambert':lambert, 'file':fileIn, 
            'place2d':place2d}
    
def importMeshToMaya(mesh):
    '''
    Imports the provided modl mesh to maya. Returns the imported nodes.
    '''
    # Store the existing shadingEngines for later
    existingSes = cmds.ls(type='shadingEngine')

    # Get a temp file to write obj data to
    suffix = mesh.name+'.obj'
    fpath = tempfile.mktemp(suffix=suffix, prefix='lecFormatsTmp')
    
    # Write the obj data out
    f = open(fpath, 'w')
    f.write('\n')
    mesh.writeObjToFile(f, includeShaders=False)
    f.write('\n')
    f.close()
    
    # import that obj data
    try:
        nodes = cmds.file(fpath, i=True, type="OBJ", options="mo=1;lo=0", 
                returnNewNodes=True)
    except RuntimeError:
        print >> sys.stderr, "Error: mesh: '%s'would not convert"%mesh.name
        #print >> sys.stderr, e
        print >> sys.stderr, "Attempting to continue"
        return None

    # Remove the intermediate obj
    os.remove(fpath)

    # Fix up the naming and such
    importedTransform = cmds.ls(nodes, dag=True, type='transform')[0]
    importedMesh = cmds.ls(nodes, dag=True, type='mesh')[0]
    nodes = set(nodes)
    nodes = nodes.difference(set([importedTransform+importedMesh]))
    importedTransform = cmds.rename(importedTransform, mesh.name+'_PLY')
    # @TODO: THis should probably include the renamed shape node too
    nodes.add(importedTransform)
    
    return list(nodes)


def meshForNode(node, modl):
    '''
    Returns ModlMesh object for node and modl
    '''
    # @TODO: Should this move to the object itself?
    if node.mesh_id == None:
        return None
    return modl.geosets[0].meshes[node.mesh_id]

def buildNode(node, modl):
    '''
    Builds the specificed modlNode in scene. Uses info from the modl object
    that it belongs to, so that must be provided as well.

    returns a dictionary:
    nodePath    - dag path to the transform for this node
    meshPath    - dag path to mesh that is directly under this node, if any
    '''
    # Create the node
    newNode = cmds.createNode('transform', name=node.name)
    
    nodeInfo = {'nodePath':newNode, 'meshPath':None}

    # See if this node has a mesh to parent
    mesh = meshForNode(node, modl)
    if mesh != None and mesh.vertices:
        # Import the mesh and parent it
        objNodes = importMeshToMaya(mesh)
        if objNodes:
            importedTransform = cmds.ls(objNodes, dag=True,
                    type='transform')
            importedTransform = cmds.parent(importedTransform, newNode,
                    r=True)
            nodeInfo['meshPath'] = importedTransform[0]
    
    # Setup the pivot
    cmds.xform(newNode, t=node.pivot)
    cmds.xform(newNode, pivots=[-axis for axis in node.pivot],
            preserve=False)
    cmds.makeIdentity(newNode, apply=True, t=True, r=True, s=True, 
            n=False)
    
    # Apply the transforms
    cmds.xform(newNode, t=node.position) 
    # x = pitch
    # y = roll
    # z = yaw
    cmds.xform(newNode, ro=(node.pitch, node.roll, node.yaw))
    
    return nodeInfo

def materialForFace(face, modl):
    '''
    Returns material name for the given face and modl
    '''
    # @TODO: Should this move to the object itself?
    if not face.has_material:
        return None
    return modl.materials[face.material_index]


def applyMaterials(mesh, modl, meshInScene, materialMap={}):
    '''
    Applies materials for mesh using those specified in modl.

    materialMap is a dictionary with material names from the modl as keys,
    and dictionaries with in-scene material definitions. See buildMatNetwork
    for mor info about the dict format.

    Returns a mapping of newly created materials in scene, if any. This
    will be the same format as materialMap, but only new things
    '''
    newMaterials = {}
    for i,face in enumerate(mesh.faces):
        material = materialForFace(face, modl)
        if not material:
            continue

        # Get the shadingGroup
        try:
            if materialMap.has_key(material):
                sg = materialMap[material]['shadingGroup']
            else:
                sg = newMaterials[material]['shadingGroup']
        except KeyError:
            # Material doesn't exist yet, make it!
            matInfo = buildMatNetwork(material)
            newMaterials[material] = matInfo
            sg = matInfo['shadingGroup']
        
        # Assign the face
        facePath = meshInScene+".f[%d]"%i
        cmds.sets(facePath, e=True, forceElement=sg)

    return newMaterials

def buildModl(modl, textureDir):
    '''
    Builds the specified Modl in scene
    '''
    nodes = []
    parentMap = {}
    materialMap = {}
    for i,node in enumerate(modl.nodes):
        nodeInfo = buildNode(node, modl)
        newNode = nodeInfo['nodePath']
        newMesh = nodeInfo['meshPath']
        
        # Account for the node
        nodes.append(newNode)
        
        # Save the node for parenting later
        if node.has_parent:
            parentMap[newNode] = node.parent_id
        
        # If a mesh was brought in, apply it's materials
        if newMesh:
            newMats = applyMaterials(meshForNode(node, modl), modl, newMesh,
                    materialMap)
            materialMap.update(newMats)
           
    # Parent all the nodes
    for node,i in parentMap.items():
        parentNode = nodes[i]
        cmds.parent(node, parentNode, r=True)
    
    # set the texture paths
    for material, matInfo in materialMap.items():
        fileNode = matInfo['file']
        matPath = os.path.join(os.path.dirname(modl.file_name), material)
        matObj = mat.MatFile(matPath)
        if matObj.count == 1:
            txPath = os.path.join(textureDir, 
                    os.path.splitext(material)[0] + '.tif')
        else:
            txPath = os.path.join(textureDir, 
                    os.path.splitext(material)[0] + '-0.tif')

        cmds.setAttr(fileNode+'.fileTextureName', txPath, type='string')
    
    # Return a mapping of source node names to maya transforms
    return zip([node.name for node in modl.nodes], [nodes])


