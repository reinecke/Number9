#!/usr/bin/env python
import maya.cmds as cmds
import sys, tempfile
sys.path = ['/Users/eric/grim-proj'] + sys.path
from lecFormats import modl

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
    mesh.writeObjToFile(f, includeShaders=False)
    f.close()
    
    # import that obj data
    nodes = cmds.file(fpath, i=True, type="OBJ", options="mo=1;lo=0", 
            returnNewNodes=True)

    # Fix up the naming and such
    importedTransform = cmds.ls(nodes, dag=True, type='transform')[0]
    importedMesh = cmds.ls(nodes, dag=True, type='mesh')[0]
    nodes = set(nodes)
    nodes = nodes.difference(set([importedTransform+importedMesh]))
    importedTransform = cmds.rename(importedTransform, mesh.name+'_PLY')
    # @TODO: THis should probably include the renamed shape node too
    nodes.add(importedTransform)
    '''
    # Merge common materials
    newSes = cmds.ls(list(nodes), type='shadingEngine')
    for newSe in newSes:
        matchFound = False
        for se in existingSes:
            if se not in newSe:
                continue
            # Merge the new shading engine with the existing one
            seConns = cmds.listConnections(newSe, plugs=True, type='mesh')
            for i in range(len(seConns)/2):
                src = seConns[i*2]
                dst = seConns[(i*2)+1]
                print src,dst
                import pdb;pdb.set_trace()
                # only interested in things this connects to
                if src.split('.')[0] != newSe:
                    continue
                
                # Only interested in geo connections
                if not cmds.ls(dst.split('.')[0], type='mesh'):
                    continue
                
                # Re-connect to the old shader
                matchFound = True
                cmds.disconnectAttr(src, dst)
                cmds.connectAttr(se+'.'+src.split('.')[-1], dst)
        
        if matchFound:
            cmds.delete(newSe)
    '''
    return list(nodes)

def buildModl(modl):
    '''
    Builds the specified Modl in scene
    '''
    nodes = []
    parentMap = {}
    materialMap = {}
    for i,node in enumerate(modl.nodes):
        # Create the node
        newNode = cmds.createNode('transform', name=node.name)
        
        # Account for the node
        nodes.append(newNode)
        
        # Save the node for parenting later
        if node.has_parent:
            parentMap[newNode] = node.parent_id
        
        # See if this node has a mesh to parent
        if node.mesh_id != None:
            # get the geo for this node and parent
            mesh = modl.geosets[0].meshes[node.mesh_id]
            if not len(mesh.vertices):
                continue
            
            objNodes = importMeshToMaya(mesh)
            importedTransform =cmds.ls(objNodes, dag=True, type='transform')
            cmds.parent(importedTransform, newNode, r=True)

            # Apply Materials
            for i,face in enumerate(mesh.faces):
                if not face.has_material:
                    continue
                material = modl.materials[face.material_index]

                # Get the shadingGroup
                try:
                    sg = materialMap[material]['shadingGroup']
                except KeyError:
                    # Material doesn't exist yet, make it!
                    matInfo = buildMatNetwork(material)
                    materialMap[material] = matInfo
                    sg = matInfo['shadingGroup']
                
                # Assign the face
                facePath = importedTransform[0]+".f[%d]"%i
                cmds.sets(facePath, e=True, forceElement=sg)
        
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
    
    # Parent all the nodes
    for node,i in parentMap.items():
        parentNode = nodes[i]
        cmds.parent(node, parentNode, r=True)
    
    # Return a mapping of source node names to maya transforms
    return zip([node.name for node in modl.nodes], [nodes])




