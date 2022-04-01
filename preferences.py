import bpy

class addonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
 
    swtor_resources_path: bpy.props.StringProperty(
        name = "'resources' path",
        description = 'Path to "resources" folder produced by a SWTOR assets extraction',
        subtype = "DIR_PATH",
        default = "resources",
        maxlen=1024
    )
 
    def draw(self, context):
        layout = self.layout
        layout.label(text="Path to the 'resources' folder created by a SWTOR assets extraction")
        layout.prop(self, 'swtor_resources_path', expand=True)
 

# Registrations

def register():
    bpy.utils.register_class(addonPreferences)


def unregister():
    bpy.utils.unregister_class(addonPreferences)

if __name__ == "__main__":
    register()