import bpy
import bmesh

# Main

class ZGSWTOR_OT_remove_doubles(bpy.types.Operator):

    bl_idname = "zgswtor.remove_doubles"
    bl_label = "SWTOR Tools"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Removes double vertices (does a Merge by Distance\nto the vertices of selected objects using a\nthreshold of 0.0000001).\nProcesses each selected object individually.\n\nREQUIRES A SELECTION OF OBJECTS"

    def execute(self, context):

        if bpy.context.object:

            selected_objects = [obj for obj in bpy.context.selected_editable_objects if obj.type == "MESH" and not "skeleton" in obj.name]

            if selected_objects:

                temp_mesh = bmesh.new()

                for obj in selected_objects:
                    
                    temp_mesh.from_mesh(obj.data)

                    bmesh.ops.remove_doubles(temp_mesh, verts = temp_mesh.verts, dist = 1e-06)

                    temp_mesh.to_mesh(obj.data)

                    obj.data.update()

                    temp_mesh.clear()

        return {"FINISHED"}


# UI is set in ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_remove_doubles)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_remove_doubles)