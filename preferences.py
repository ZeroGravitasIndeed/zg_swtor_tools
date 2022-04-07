import bpy

class addonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
 
    swtor_resources_path: bpy.props.StringProperty(
        name = "SWTOR Resources",
        description = 'Path to the "resources" folder produced by a SWTOR assets extraction',
        subtype = "DIR_PATH",
        default = "Choose or type the folder's path",
        maxlen=1024
    )
 
    def draw(self, context):
        layout = self.layout
        col=layout.column()
        col.scale_y = 0.7
        col.label(text="Path to the 'resources' folder created by a SWTOR assets extraction")
        col.label(text="produced by the Slicers GUI app, EasyMYP, or any similar tool.")
        layout.prop(self, 'swtor_resources_path', expand=True)
 

# Registrations

def register():
    bpy.utils.register_class(addonPreferences)


def unregister():
    bpy.utils.unregister_class(addonPreferences)

if __name__ == "__main__":
    register()