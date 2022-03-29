import bpy


class ZGSWTOR_PT_materials_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Materials Tools"

    def draw(self, context):

        self.layout.operator("zgswtor.process_uber_mats", text="Process Uber materials")

        self.layout.operator("zgswtor.deduplicate_nodegroups", text="Deduplicate Nodegroups")


class ZGSWTOR_PT_objects_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "Object Tools"

    def draw(self, context):
        
        self.layout.operator("zgswtor.remove_doubles", text="Merge Double Vertices")






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