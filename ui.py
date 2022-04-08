import bpy


# Materials Tools sub-panel
class ZGSWTOR_PT_materials_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Materials Tools"

    def draw(self, context):

        # process_uber_mats UI
        self.layout.operator("zgswtor.process_uber_mats", text="Process Uber Materials")

        # deduplicate nodegroups UI
        self.layout.operator("zgswtor.deduplicate_nodegroups", text="Deduplicate Scene's Nodegroups")

        # # Shader Controls UI
        # box = self.layout.box()
        # box.label(text="Scene-wide Shader Controls")
        # box.prop(context.scene, "Normals strength")
        # box.prop(context.scene, "Emissive strength")



# Objects Tools sub-panel
class ZGSWTOR_PT_objects_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Objects Tools"

    def draw(self, context):
        
        # remove_doubles UI
        self.layout.operator("zgswtor.remove_doubles", text="Merge Double Vertices")




# Registrations

classes = [
    ZGSWTOR_PT_materials_tools,
    ZGSWTOR_PT_objects_tools
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()