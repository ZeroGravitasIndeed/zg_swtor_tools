import bpy

class addonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # Preferences properties --------------------

    # resources folderpath
    swtor_resources_path: bpy.props.StringProperty(
        name = "SWTOR Resources",
        description = 'Path to the "resources" folder produced by a SWTOR assets extraction',
        subtype = "DIR_PATH",
        default = "/Volumes/RECURSOS/3D SWTOR/extracted_swtor/resources/",
#        default = "Choose or type the folder's path",
        maxlen = 1024
    )

    # quickscale factor
    defaultval=5.0
    swtor_quickscale_factor: bpy.props.FloatProperty(
        name = "SWTOR Quickscale",
        description = 'Upscaling/Downscaling factor for temporarily or permanently upsizing\nSWTOR models and others to "real life" dimensions that Blender handles better\nin certain calculations (e.g., auto-weight painting, physics, etc.)',
        subtype="FACTOR",
        min = 1.0,
        max = 100.0,
        soft_min = 7.0,
        soft_max = 10.0,
        step = 3,
        precision = 2,
        default = defaultval
    )

    # UI ----------------------------------------
    
    def draw(self, context):
        layout = self.layout

        # resources folderpath preferences UI
        pref_box = layout.box()
        col=pref_box.column()
        col.scale_y = 0.7
        col.label(text="Path to the 'resources' folder in a SWTOR assets extraction")
        col.label(text="produced by the Slicers GUI app, EasyMYP, or any similar tool.")
        pref_box.prop(self, 'swtor_resources_path', expand=True)

        # Quickscale factor preferences UI
        pref_box = layout.box()
        row=pref_box.row()
        row.label(text="Quick Upscale / Downscale Factor")
        row.prop(self, 'swtor_quickscale_factor', text='')
        

# Registrations

def register():
    bpy.utils.register_class(addonPreferences)

def unregister():
    bpy.utils.unregister_class(addonPreferences)

if __name__ == "__main__":
    register()