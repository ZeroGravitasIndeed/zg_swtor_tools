import bpy

class addonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
 
    swtor_resources_path: bpy.props.StringProperty(
        name = 'swtor_resources_path',
        description = 'Path to "resources" folder produced by a SWTOR assets extraction',
        subtype = "DIR_PATH",
        default = "resources",
        maxlen=1024
    )
 
    def draw(self, context):
        layout = self.layout
        layout.label(text='Enter the path to the "resources" folder created by a SWTOR assets extraction')
        row = layout.row()
        row.prop(self, 'swtor_resources_path', expand=True)
 

# Registrations

def register():
    bpy.utils.register_class(addonPreferences)


def unregister():
    bpy.utils.unregister_class(addonPreferences)
