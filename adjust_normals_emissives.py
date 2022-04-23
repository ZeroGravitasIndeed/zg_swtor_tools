import bpy
import addon_utils


class ZGSWTOR_OT_adjust_normals_emissives(bpy.types.Operator):

    bl_label = "SWTOR Tools"
    bl_idname = "zgswtor.process_uber_mats"
    bl_description = "Scans for Uber materials in selected objects and places in them\nUber shaders and their associated textures.\n\n• Requires a selection of objects.\n• Requires an enabled SWTOR .gr2 Importer Add-on."
    bl_options = {'REGISTER', 'UNDO'}


    # Check that there are SWTOR shaders in the scene) 
    @classmethod
    def poll(cls,context):
        if bpy.data.node_groups["SWTOR"]:
            return True
        else:
            return False



    def execute(self, context):

        # --------------------------------------------------------------
        # Check which version of the SWTOR shaders are available
        if addon_utils.check("io_scene_gr2_legacy")[1]:
            if "Uber Shader" in bpy.data.node_groups:
                gr2_addon_legacy = True
            else:
                self.report({"WARNING"}, "Although the Legacy version of the 'io_scene_gr2' add-on is enabled, no Uber Shader exists yet. Please import any arbitrary .gr2 object to produce an Uber Shader template.")
                return {"CANCELLED"}
        elif addon_utils.check("io_scene_gr2")[1]:
            gr2_addon_legacy = False
        else:
            self.report({"WARNING"}, "No version of the 'io_scene_gr2' add-on is enabled.")
            return {"CANCELLED"}



            
        return {"FINISHED"}


# UI is set in ui.py


# ------------------------------------------------------------------
# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_process_uber_mats)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_process_uber_mats)

if __name__ == "__main__":
    register()