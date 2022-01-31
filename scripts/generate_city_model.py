import bpy
import os
import bmesh
import glob
import mathutils
import math
import sys
import subprocess
from datetime import datetime
lod = 1+((21-int(sys.argv[8][1:]))/5)
leftx = int(sys.argv[4])
lefty = int(sys.argv[5])

rightx = int(sys.argv[6])
righty = int(sys.argv[7])

originx = 25490000
originy = 6668000


bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
# Model directory
model_dir = sys.argv[3]+'/../../src_3d_files/'
obj_list = []
for dirpath, dirnames, filenames in os.walk(model_dir):
    for filename in [f for f in filenames if f.endswith(".obj")]:
        obj_list.append(os.path.join(dirpath, filename))

# loop through the strings in obj_list and add the files to the scene
for path_to_file in obj_list:
    bpy.ops.import_scene.obj(filepath = path_to_file)
scene = bpy.context.scene
obs = []
for ob in scene.objects:
    if ob.type == 'MESH':
        obs.append(ob)
        
ctx = bpy.context.copy()

ctx['active_object'] = obs[0]

ctx['selected_objects'] = obs

ctx['selected_editable_objects'] = obs
        
bpy.ops.object.join(ctx)
obs[0].rotation_euler[0] = math.radians(0)
bpy.context.view_layer.objects.active = obs[0]
me = obs[0].data
bm = bmesh.new()
bm.from_mesh(me)

center = mathutils.Vector((leftx*0.5+rightx*0.5-originx, lefty*0.5+righty*0.5-originy,50))
height = (righty-lefty)
width = (rightx-leftx)
leftpoint = center + mathutils.Vector((width*-0.5,0,0))
rightpoint = center + mathutils.Vector((width*0.5,0,0))
toppoint = center + mathutils.Vector((0,height*0.5,0))
bottompoint = center + mathutils.Vector((0,height*-0.5,0))

leftnormal = (-1,0,0)
rightnormal = (1,0,0)
topnormal = (0,1,0)
bottomnormal = (0,-1,0)

# select all faces
for f in bm.faces:
    f.select = True


bmesh.ops.bisect_plane(bm,  geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co = leftpoint, plane_no = leftnormal, clear_outer = True, clear_inner = False)
bmesh.ops.bisect_plane(bm,  geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co = rightpoint, plane_no = rightnormal, clear_outer = True, clear_inner = False)
bmesh.ops.bisect_plane(bm,  geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co = toppoint, plane_no = topnormal, clear_outer = True, clear_inner = False)
bmesh.ops.bisect_plane(bm,  geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co = bottompoint, plane_no = bottomnormal, clear_outer = True, clear_inner = False)
bm.to_mesh(obs[0].data)
bm.free()
bpy.ops.object.mode_set( mode   = 'EDIT'   )
bpy.ops.mesh.select_mode( type  = 'FACE'   )
#bisect
bpy.ops.mesh.select_all(action='SELECT')
bpy.context.tool_settings.mesh_select_mode = (False, True, False) 

#me = obs[0].data
bm = bmesh.from_edit_mesh(me)
for edge in bm.edges:
    if edge.is_boundary:
        edge.select = True
        continue
    
    edge.select = False
#THRESHOLDIT PIENEMMÄKS SIT KU ON ISOMPI LOD
bpy.ops.mesh.remove_doubles(threshold = 0.1*lod)
bpy.ops.mesh.select_all(action='DESELECT')
#me = obs[0].data
bm = bmesh.from_edit_mesh(me)
for edge in bm.edges:
    if edge.is_boundary:
        edge.select = True
        continue
    
    edge.select = False

bpy.ops.mesh.remove_doubles(threshold = 0.2*lod)
bpy.ops.mesh.select_all(action='DESELECT')
#me = obs[0].data
bm = bmesh.from_edit_mesh(me)
for edge in bm.edges:
    if edge.is_boundary:
        edge.select = True
        continue
    
    edge.select = False

bpy.ops.mesh.remove_doubles(threshold = 0.4*lod)
bpy.ops.mesh.select_all(action='DESELECT')
#me = obs[0].data
bm = bmesh.from_edit_mesh(me)
for edge in bm.edges:
    if edge.is_boundary:
        edge.select = True
        continue
    
    edge.select = False

bpy.ops.mesh.remove_doubles(threshold = 1*lod)
bpy.ops.mesh.select_all(action='DESELECT')
#me = obs[0].data
bm = bmesh.from_edit_mesh(me)
for edge in bm.edges:
    if edge.is_boundary:
        edge.select = True
        continue
    
    edge.select = False


#get minz

o  = bpy.context.object 
mw = o.matrix_local      # Active object's world matrix

glob_vertex_coordinates = [ mw @ v.co for v in o.data.vertices ] # Global  coordinates of vertices

# Find the lowest Z value amongst the object's verts
minZ = min( [ co.z for co in glob_vertex_coordinates ] ) 

bpy.ops.mesh.extrude_region_move()
bpy.ops.transform.resize(value=(1, 1, 0))

o.update_from_editmode()
me = o.data
verts_sel = [v.co.z for v in me.vertices if v.select]

pivotz = sum(verts_sel) / len(verts_sel)
print(pivotz)
bpy.ops.transform.translate(value=(0, 0, pivotz*-1+minZ-6))
bpy.ops.mesh.extrude_region_move()
bpy.ops.transform.resize(value=(0, 0, 0))
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.mesh.fill_holes(sides=10)
bpy.ops.mesh.remove_doubles(threshold = 0.0001)
#me = obs[0].data
bm = bmesh.new()
bm.from_mesh(me)
bmesh.ops.triangulate(bm, faces=bm.faces[:])
bpy.ops.object.mode_set( mode = 'OBJECT' )
bpy.ops.object.delete()
#BOOLEAN (alternative to bisect, slow since this is hole tolerant exact)
#bpy.ops.mesh.primitive_cube_add(location=(leftx*0.5+rightx*0.5-originx, lefty*0.5+righty*0.5-originy, 50))
#resize the cube
#bpy.ops.transform.resize(value=((rightx-leftx)*0.5, (righty-lefty)*0.5, 300))
#cube = scene.objects.get("Cube")
#bool = obs[0].modifiers.new(name='booly', type='BOOLEAN')
#bool.object = cube
#bool.operation = 'INTERSECT'
#bool.use_hole_tolerant = True
#bpy.context.view_layer.objects.active = obs[0]
#bpy.ops.object.modifier_apply(modifier=bool.name)
#bpy.context.view_layer.objects.active = cube
#bpy.ops.object.delete()

#print(sys.argv[3])
#print(os.path.join(sys.argv[3], '/../result/result.stl'))
#print(sys.argv[3]+'/../result/result.stl')
target_file = sys.argv[3]+'\\..\\..\\result\\result_'+str(datetime.now()).replace(" ", "_").replace(":", "-").replace(".", "_")+'.stl'

bpy.ops.export_mesh.stl(filepath=target_file)
resultpath = os.path.realpath(sys.argv[3]+'\\..\\..\\result')
os.startfile(resultpath)
#OBJ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#target_file = sys.argv[3]+'\\..\\result\\result.obj'

#bpy.ops.export_scene.obj(filepath=target_file)