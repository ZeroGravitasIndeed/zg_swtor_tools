import bpy
import pathlib
import re
import xml.etree.ElementTree as ET
import addon_utils


def detect_gr2_addon_version():
    # for future compatibility with new shaders
    if addon_utils.check("io_scene_gr2_legacy")[1]:
        return("legacy")
    if addon_utils.check("io_scene_gr2")[1]:
        return("current")

    

class ZGSWTOR_OT_process_uber_mats(bpy.types.Operator):

    bl_label = "SWTOR Tools"
    bl_idname = "zgswtor.process_uber_mats"
    bl_description = "Checks for Uber materials in selected objects and replaces\ntheir default generic Principled Shaders with Uber ones\nand associated textures\n\nREQUIRES A SELECTION OF OBJECTS AND THE PRESENCE\nOF LEGACY SWTOR SHADERS IN THE .BLEND FILE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        selected_objects = bpy.context.selected_objects
        if not selected_objects:
            return {"CANCELLED"}

        # Get the extracted SWTOR assets' "resources" folder from the add-on preferences. 
        swtor_resources_path = bpy.context.preferences.addons[__package__].preferences.swtor_resources_path
        swtor_shaders_path = swtor_resources_path + "/art/shaders/materials"

        # Test the existence of the shaders subfolder to validate the SWTOR "resources" folder
        if pathlib.Path(swtor_shaders_path).exists() == False:
            self.report({"WARNING"}, "Can't find the SWTOR Materials subfolder. Please check this add-on's preferences: either the path to the extracted assets 'resources' folder is incorrect or the resources > art > shaders > materials subfolder is missing.")
            return {"CANCELLED"}

        mats = []
        for obj in selected_objects:
            for mat_slot in obj.material_slots:
                mats.append(bpy.data.materials[mat_slot.material.name])

        print(mats)


        for mat in mats:

            # print(mat.name)

            if (r"Template: " not in mat.name) and (r"default" not in mat.name) and mat.users:

                mat_tree_filepath = swtor_shaders_path + "/" + mat.name + ".mat"

                # By looking for the material in the shaders folder we'll inherently
                # filter out recolorable materials such as skin, eyes or armor already.

                try:
                    mat_tree = ET.parse(mat_tree_filepath)
                except:
                    print("     Not processed")
                    continue

                
                mat_root = mat_tree.getroot()

                mat_Derived = mat_root.find("Derived").text  # Shader Type
                mat_Visibility = mat_root.find("Visibility").text
                mat_AlphaMode = mat_root.find("AlphaMode").text
                mat_AlphaTestValue = mat_root.find("AlphaTestValue").text
                mat_IsTwoSided = mat_root.find("IsTwoSided").text



                # Parse inputs, detect which ones are textures and load them

                mat_inputs = mat_root.findall("input")
                for mat_input in mat_inputs:
                    mat_semantic = mat_input.find("semantic").text
                    mat_type = mat_input.find("type").text
                    mat_value = mat_input.find("value").text
                    mat_variable = mat_input.find("variable").text


                    if mat_type == "texture":
                        mat_value = mat_value.replace("\\", "/")

                    if mat_semantic == "DiffuseMap":
                        try:
                            DiffuseMap_image = bpy.data.images.load(swtor_resources_path + "/" + mat_value + ".dds", check_existing=True)
                            DiffuseMap_image.colorspace_settings.name = 'Raw'
                        except:
                            DiffuseMap_image = None
                        
                    if mat_semantic == "RotationMap1":
                        try:
                            RotationMap_image = bpy.data.images.load(swtor_resources_path + "/" + mat_value + ".dds", check_existing=True)
                            RotationMap_image.colorspace_settings.name = 'Raw'
                        except:
                            RotationMap_image = None

                    if mat_semantic == "GlossMap":
                        try:
                            GlossMap_image = bpy.data.images.load(swtor_resources_path + "/" + mat_value + ".dds", check_existing=True)
                            GlossMap_image.colorspace_settings.name = 'Raw'
                        except:
                            GlossMap_image = None

                if "Uber" in mat_Derived:

                    mat.blend_method = 'CLIP'
                    mat.shadow_method = 'CLIP'
                    mat.alpha_threshold = 0.5
                    mat.use_nodes = True
                    mat.use_fake_user = True


                    nodes = mat.node_tree.nodes

                    # Remove Principled shader
                    for node in nodes:
                        if node.name == "Principled BSDF":
                            nodes.remove(node)


                    # Add Uber Shader and link it to Output node
                    if not "Uber Shader" in nodes:
                        uber_nodegroup = nodes.new(type="ShaderNodeGroup")
                        uber_nodegroup.node_tree = bpy.data.node_groups["Uber Shader"]
                    else:
                        uber_nodegroup = nodes["Uber Shader"]
                    
                    uber_nodegroup.location = 0, 0
                    uber_nodegroup.width = 300
                    uber_nodegroup.width_hidden = 300
                    uber_nodegroup.name = "Uber Shader"
                    uber_nodegroup.label = "Uber Shader"

                    nodes["Material Output"].location = 400, 0

                    links = mat.node_tree.links

                    links.new(nodes["Material Output"].inputs[0],uber_nodegroup.outputs[0])



                    # Add Diffuse node and link it to Uber shader
                    if not "_d DiffuseMap" in nodes:
                        _d = nodes.new(type='ShaderNodeTexImage')
                        _d.name = _d.label = "_d DiffuseMap"
                    else:
                        _d = nodes["_d DiffuseMap"]
                    _d.location = (-464, 300)
                    _d.width = _d.width_hidden = 300
                    links.new(uber_nodegroup.inputs[0],_d.outputs[0])
                    _d.image = DiffuseMap_image


                    # Add Rotation node and link it to Uber shader
                    if not "_n RotationMap" in nodes:
                        _n = nodes.new(type='ShaderNodeTexImage')
                        _n.name = _n.label = "_n RotationMap"
                    else:
                        _n = nodes["_n RotationMap"]
                    _n.location = (-464, 0)
                    _n.width = _n.width_hidden = 300
                    links.new(uber_nodegroup.inputs[1],_n.outputs[0])
                    links.new(uber_nodegroup.inputs[2],_n.outputs[1])
                    _n.image = RotationMap_image


                    # Add Gloss node and link it to Uber shader
                    if not "_s GlossMap" in nodes:
                        _s = nodes.new(type='ShaderNodeTexImage')
                        _s.name = _s.label = "_s GlossMap"
                    else:
                        _s = nodes["_s GlossMap"]
                    _s.location = (-464, -300)
                    _s.width = _s.width_hidden = 300
                    links.new(uber_nodegroup.inputs[3],_s.outputs[0])
                    links.new(uber_nodegroup.inputs[4],_s.outputs[1])
                    _s.image = GlossMap_image

        return {"FINISHED"}


# UI is set in ui.py



# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_process_uber_mats)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_process_uber_mats)