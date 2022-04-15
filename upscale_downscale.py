import bpy

class ZGSWTOR_OT_upscale_downscale(bpy.types.Operator):
    bl_idname = "zgswtor.upscale_downscale"
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

    # Scaling factor property
    manual_scaling_factor: bpy.props.FloatProperty(
        name = "Manual Scaling Factor",
        description = 'Upscaling/Downscaling factor for temporarily or permanently upsizing\nSWTOR models and others to "real life" dimensions that Blender handles better',
        default = 10.0
    )


    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    #
    action: bpy.props.EnumProperty(
        name="SWTOR Scene scaling",
        items=[
            ("UPSCALE", "Upscale", "Upscale"),
            ("DOWNSCALE", "Downscale", "Downscale")
            ]
        )

    # Methods doing the actual setting of Backface Culling    
    @staticmethod
    def upscale(objs, upscaling_factor):
        for obj in objs:
            obj.scale *= upscaling_factor
            obj.location *= upscaling_factor

    @staticmethod
    def downscale(objs, upscaling_factor):
        for obj in objs:
            obj.scale /= upscaling_factor
            obj.location /= upscaling_factor


    
    def execute(self, context):

        # Get the upscaling factor from the add-on's preferences.
        upscaling_factor = bpy.context.preferences.addons[__package__].preferences.upscaling_factor

        # Select only objects that aren't parented, to avoid double-scaling.
        # See: https://blender.stackexchange.com/questions/82678/how-can-i-scale-all-objects-in-the-scene-about-the-origin-using-python
        selected_objects = [obj for obj in bpy.context.selected_objects if not obj.parent]
        
        if selected_objects:

            if self.action == "UPSCALE":
                self.upscale(selected_objects, upscaling_factor)
            elif self.action == "DOWNSCALE":
                self.downscale(selected_objects,upscaling_factor)

        return {"FINISHED"}


# UI is set in ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_upscale_downscale)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_upscale_downscale)

if __name__ == "__main__":
    register()