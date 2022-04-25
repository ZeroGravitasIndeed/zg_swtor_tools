from email.policy import default
import bpy

class ZGSWTOR_OT_quickscale(bpy.types.Operator):
    bl_idname = "zgswtor.quickscale"
    bl_label = "SWTOR Tools"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Quickscaler:\nResizes objects preserving their relative distances to facilitate\noperations that require real life-like sizes (e.g., auto-weight painting).\n\n• Requires a selection of objects.\n• Affects Dimension data instead of scale"

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
            ],
        options={'HIDDEN'}
        )

    quickscale_factor : bpy.props.FloatProperty(
        name = "Quickscaling Factor",
        description = 'Upscaling/Downscaling factor for temporarily or permanently upsizing\nSWTOR models and others to "real life" dimensions that Blender handles better\nin certain calculations (e.g., auto-weight painting, physics, etc.)',
        min = 1.0,
        max = 100.0,
        soft_min = 7.0,
        soft_max = 10.0,
        step = 5,
        precision = 2,
        default = -1.0,
        options={'HIDDEN'}
        )


    # METHODS

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


    
    
    def execute(self, context):

        # Select only objects that aren't parented to avoid double-scaling.
        # Scales both sizes and positions in respect to the origin so that
        # the whole scene's object spacing is correctly preserved.

        quickscale_factor_pref = bpy.context.preferences.addons[__package__].preferences.swtor_quickscale_factor

        if self.quickscale_factor == -1.0:  # Get the upscaling factor from the add-on's preferences.
            self.quickscale_factor = quickscale_factor_pref

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
    bpy.types.Scene.zgswtor_quickscale_factor = bpy.props.FloatProperty(
        name="",
        description="Scaling Factor. Recommended values are:\n\n- 10 for simplicity (characters look superhero-like tall, over 2 m.).\n\n- Around 8 for accuracy (characters show more realistic heights)",
        default=bpy.context.preferences.addons[__package__].preferences.swtor_quickscale_factor
    )
    bpy.utils.register_class(ZGSWTOR_OT_quickscale)

def unregister():
    del bpy.types.Scene.zgswtor_quickscale_factor
    bpy.utils.unregister_class(ZGSWTOR_OT_quickscale)


if __name__ == "__main__":
    register()