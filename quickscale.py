import bpy

class ZGSWTOR_OT_quickscale(bpy.types.Operator):
    bl_idname = "zgswtor.quickscale"
    bl_label = "SWTOR Tools"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Scales selected objects of a SWTOR models-based scene\nto facilitate Blender operations that require real life-like sizes\n(e.g., auto-weight painting, physics, etc.)"

    # Check that there is a selection of objects (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False


    # PROPERTIES

    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    
    action: bpy.props.EnumProperty(
        name="Scaling Type",
        items=[
            ("UPSCALE", "Upscale", "Upscale"),
            ("DOWNSCALE", "Downscale", "Downscale")
            ]
        )

    quickscale_factor : bpy.props.FloatProperty(
        name = "Quickscaling Factor",
        description = 'Upscaling/Downscaling factor for temporarily or permanently upsizing\nSWTOR models and others to "real life" dimensions that Blender handles better\nin certain calculations (e.g., auto-weight painting, physics, etc.)',
        default = 1.0,
        min=0.01,
        soft_min=1,
        max=100,
        soft_max=10
        )


    # METHODS

    @staticmethod  # Get the upscaling factor from the add-on's preferences.
    def get_prefs(self,context):
        return bpy.context.preferences.addons[__package__].preferences.quickscale_factor

    # Methods doing the actual scaling    
    @staticmethod
    def upscale(objs, factor):
        for obj in objs:
            obj.scale *= factor
            obj.location *= factor

    @staticmethod
    def downscale(objs, factor):
        for obj in objs:
            obj.scale /= factor
            obj.location /= factor

    
    # EXECUTE METHOD
    
    def execute(self, context):

        # Select only objects that aren't parented to avoid double-scaling.
        # Scales both sizes and positions in respect to the origin so that
        # the whole scene's object spacing is correctly preserved.

        scaling_factor_prefs = self.get_prefs

        if self.quickscale_factor == None:
            self.quickscale_factor = scaling_factor_prefs

        if self.quickscale_factor != context.scene.zgswtor_quickscale_factor:
            self.quickscale_factor = context.scene.zgswtor_quickscale_factor

        selected_objects = [obj for obj in bpy.context.selected_objects if not obj.parent]

        if selected_objects:
            if self.action == "UPSCALE":
                self.upscale(selected_objects, self.quickscale_factor)
            elif self.action == "DOWNSCALE":
                self.downscale(selected_objects, self.quickscale_factor)

        return {"FINISHED"}


# UI is set in ui.py

# Registrations

def register():
    bpy.types.Scene.zgswtor_quickscale_factor = bpy.props.FloatProperty()
    bpy.utils.register_class(ZGSWTOR_OT_quickscale)

def unregister():
    del bpy.types.Scene.zgswtor_quickscale_factor
    bpy.utils.unregister_class(ZGSWTOR_OT_quickscale)


if __name__ == "__main__":
    register()