import bpy

# Main

class ZGSWTOR_OT_remove_doubles(bpy.types.Operator):
    bl_idname = "zgswtor.set_backface_culling"
    bl_label = "SWTOR Tools"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Sets the objects' materials' Backface Culling. If set to on, it'll make\n any single-sided object to be invisible if its visible single-side is facing opposite to the camera. This can be very useful when placing objects inside single side, fully enclosed rooms such as a player spaceship's rooms."

    # Check that there is a selection of objects (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False
    
    def 

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

if __name__ == "__main__":
    register()