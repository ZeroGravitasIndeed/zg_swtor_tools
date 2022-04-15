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
        layout.operator("zgswtor.process_uber_mats", text="Process Uber Materials")

        # deduplicate_nodegroups UI
        layout.operator("zgswtor.deduplicate_nodegroups", text="Deduplicate All Nodegroups")


        # set_backface_culling UI
        row = layout.row(align=True)
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
        layout.operator("zgswtor.remove_doubles", text="Merge Double Vertices")

        # upscale_downscale UI
        row = layout.row(align=True)
        row.operator("zgswtor.upscale_downscale", text="Downscale").action="DOWNSCALE"
        # in_row = row.row()
        # in_row.scale_x = 0.35
        # in_row.prop("zgswtor.upscale_downscale", "manual_scaling_factor", text="Fac")
        row.operator("zgswtor.upscale_downscale", text="Upscale").action="UPSCALE"




# Scene Tools sub-panel
class ZGSWTOR_PT_scene_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Scene Tools"

    def draw(self, context):
        layout = self.layout

        # Simplify (copy of existing operators)
        row = layout.row(align=True)
        row.prop(context.scene.render, "use_simplify", text=" Simplify")
        in_row = row.row()  # for setting a non-50% contiguous row region
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