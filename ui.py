from email.policy import default
import bpy



# Materials Tools sub-panel
class ZGSWTOR_PT_materials_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Materials Tools"

    def draw(self, context):
        layout = self.layout
        
        # process_uber_mats UI
        tool_section = layout.box().column(align=True)
        tool_section.operator("zgswtor.process_uber_mats", text="Process Uber Materials")
        tool_section.prop(context.scene, "use_overwrite_bool", text="Overwrite Uber Materials")
        tool_section.prop(context.scene, "use_collect_colliders_bool", text="Collect Collider Objects")


        # deduplicate_nodegroups UI
        tool_section = layout.box()
        tool_section.operator("zgswtor.deduplicate_nodegroups", text="Deduplicate All Nodegroups")


        # set_backface_culling UI
        tool_section = layout.box()
        row = tool_section.row(align=True)
        row.operator("zgswtor.set_backface_culling", text="Set Backface Culling On").action="BACKFACE_CULLING_ON"
        
        in_row = row.row()  # for setting a non-50% contiguous row region
        in_row.scale_x = 0.35
        in_row.operator("zgswtor.set_backface_culling", text="Off").action="BACKFACE_CULLING_OFF"



# Objects Tools sub-panel
class ZGSWTOR_PT_objects_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Objects Tools"

    def draw(self, context):
        layout = self.layout
        
        # remove_doubles UI
        tool_section = layout.box()
        tool_section.operator("zgswtor.remove_doubles", text="Merge Double Vertices")

        # quickscale UI
        tool_section = layout.box()
        row = tool_section.row(align=True)
        row.operator("zgswtor.quickscale", text="Downscale").action="DOWNSCALE"
        in_row = row.row()  # for a non-50% contiguous row region
        in_row.scale_x = 0.9
        in_row.prop(context.scene, "zgswtor_quickscale_factor", text="")
        row.operator("zgswtor.quickscale", text="Upscale").action="UPSCALE"




# Scene Tools sub-panel
class ZGSWTOR_PT_scene_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Scene Tools"

    def draw(self, context):
        layout = self.layout

        # Simplify (copy of existing operators)
        tool_section = layout.box()
        row = tool_section.row(align=True)
        row.prop(context.scene.render, "use_simplify", text=" Simplify")
        in_row = row.row()  # for a non-50% contiguous row region
        in_row.scale_x = 1.2
        in_row.prop(context.scene.render, "simplify_subdivision", text="Max SubD")

        
# Registrations

classes = [
    ZGSWTOR_PT_materials_tools,
    ZGSWTOR_PT_objects_tools,
    ZGSWTOR_PT_scene_tools
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    
if __name__ == "__main__":
    register()