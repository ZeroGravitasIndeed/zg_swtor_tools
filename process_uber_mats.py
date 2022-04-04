# This code is horrible. it just happens to work. Mostly.
# PEP-8 what's that. Read my Indent Rollercoaster Model manifest!
# So, without further ado…

import bpy
import pathlib
import xml.etree.ElementTree as ET
import addon_utils
import timeit


class ZGSWTOR_OT_process_uber_mats(bpy.types.Operator):

    bl_label = "SWTOR Tools"
    bl_idname = "zgswtor.process_uber_mats"
    bl_description = "Checks for Uber materials in selected objects and replaces\nany default generic Principled Shader in them with Uber ones\nand associated textures\n\nRequires a selection of objects to oeprate on\nand the presence of Legacy SWTOR Shaders in the .blend file"
    bl_options = {'REGISTER', 'UNDO'}

    # ------------------------------------------------------------------
    # Check that there is a selection of objects (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False

    # ------------------------------------------------------------------
    #Define some checkbox-type properties

    use_IsTwoSided_bool: bpy.props.BoolProperty(
        name="Use 'IsTwoSided' data",
        description="Activates Backface Culling if the .mat file's 'IsTwoSided' element contains a 'False'.\nUseful when processing locations such as player ships or buildings' interiors, as their inner floors, walls and ceilings become see-through from outside, facilitating characters and props placement",
        default = False
        )
    
    use_overwrite_bool: bpy.props.BoolProperty(
        name="Overwrite Uber materials",
        description='Processes the selected objects Uber materials even if they have an Uber shader already, effectively "regenerating" those ones',
        default = False )

    # ------------------------------------------------------------------
    def execute(self, context):

        selected_objects = bpy.context.selected_objects
        if not selected_objects:
            return {"CANCELLED"}

        # --------------------------------------------------------------
        # Get the extracted SWTOR assets' "resources" folder from the add-on's preferences. 
        swtor_resources_path = bpy.context.preferences.addons[__package__].preferences.swtor_resources_path
        swtor_shaders_path = swtor_resources_path + "/art/shaders/materials"

        # Test the existence of the shaders subfolder to validate the SWTOR "resources" folder
        if pathlib.Path(swtor_shaders_path).exists() == False:
            self.report({"WARNING"}, "Unable to find the SWTOR Materials subfolder. Please check this add-on's preferences: either the path to the extracted assets 'resources' folder is incorrect or the resources > art > shaders > materials subfolder is missing.")
            return {"CANCELLED"}

        # --------------------------------------------------------------
        # Check which version of the SWTOR shaders are available
        if addon_utils.check("io_scene_gr2_legacy")[1]:
            gr2_addon_legacy = True
        elif addon_utils.check("io_scene_gr2")[1]:
            gr2_addon_legacy = False
        else:
            self.report({"WARNING"}, "No version of the 'io_scene_gr2' add-on is enabled.")
            return {"CANCELLED"}


        # Main loop
        for ob in selected_objects:
            if ob.type == "MESH":

                for mat_slot in ob.material_slots:

                    mat = mat_slot.material

                    if (r"Template: " not in mat.name) and (r"default" not in mat.name) and mat.users:

                        # By looking for the material in the shaders folder we'll inherently
                        # filter out recolorable materials such as skin, eyes or armor already,
                        # finding only the Uber and a few Creature ones.
                        mat_tree_filepath = swtor_shaders_path + "/" + mat.name + ".mat"
                        try:
                            matxml_tree = ET.parse(mat_tree_filepath)
                        except:
                            continue  # disregard and go for the next material
                        matxml_root = matxml_tree.getroot()

                        matxml_derived = matxml_root.find("Derived").text

                        if matxml_derived == "Uber" or matxml_derived == "EmissiveOnly":

                            if self.use_overwrite_bool == True or ( "Principled BSDF" in mat_nodes and not ( ("Uber Shader" in mat_nodes) or ("ShaderNodeHeroEngine" in mat_nodes) ) ):
                                mat.node_tree.nodes(clear)
                            else:
                                continue  # Entirely disregard material and go for the next one

                            # ----------------------------------------------
                            # Basic material settings

                            mat.use_nodes = True  # Redundant?
                            mat.use_fake_user = False

                            mat_nodes = mat.node_tree.nodes

                            # Read and set some basic material attributes
                            mat_AlphaMode = matxml_root.find("AlphaMode").text
                            mat_AlphaTestValue = matxml_root.find("AlphaTestValue").text
                            mat_IsTwoSided = matxml_root.find("IsTwoSided").text                        

                            # Add Output node to emptied material
                            # (why can't I do output_node = mat_node.new('ShaderNodeOutputMaterial') instead?)
                            output_node = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')


                            # ----------------------------------------------
                            # Gather texture maps

                            diffusemap_image = None
                            rotationmap_image = None
                            glossmap_image = None

                            temp_image = None
                            temp_imagepath = None

                            matxml_inputs = matxml_root.findall("input")
                            for matxml_input in matxml_inputs:
                                matxml_semantic = matxml_input.find("semantic").text
                                matxml_type = matxml_input.find("type").text
                                matxml_value = matxml_input.find("value").text

                                # Parsing and loading texture maps

                                if matxml_type == "texture":
                                    matxml_value = matxml_value.replace("\\", "/")
                                    temp_imagepath = swtor_resources_path + "/" + matxml_value + ".dds"
                                    try:
                                        temp_image = bpy.data.images.load(temp_imagepath, check_existing=True)
                                        temp_image.colorspace_settings.name = 'Raw'
                                    except:
                                        pass
                                    if matxml_semantic == "DiffuseMap":
                                        diffusemap_image = temp_image
                                    elif matxml_semantic == "RotationMap1":
                                        rotationmap_image = temp_image
                                    elif matxml_semantic == "GlossMap":
                                        glossmap_image = temp_image


                            # ----------------------------------------------
                            # Add Uber Shader and connect texturemaps

                            if gr2_addon_legacy:
                                # ------------------------------------------
                                # For Legacy version of the shader

                                # Adjust transparency and shadows
                                mat.alpha_threshold = float(mat_AlphaTestValue)

                                if mat_AlphaMode == 'Test':
                                    mat.blend_method = 'CLIP'
                                    mat.shadow_method = 'CLIP'
                                elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                                    mat_AlphaMode == 'Blend'
                                    mat.blend_method = 'BLEND'
                                    mat.shadow_method = 'HASHED'
                                else:
                                    mat_AlphaMode == 'None'
                                    mat.blend_method = 'OPAQUE'
                                    mat.shadow_method = 'NONE'

                                # Set Backface Culling
                                mat.use_backface_culling = (mat_IsTwoSided == "False" and self.use_IsTwoSided_bool == True)


                                # Add Uber Shader and link it to Output node
                                uber_nodegroup = mat_nodes.new(type="ShaderNodeGroup")
                                uber_nodegroup.node_tree = bpy.data.node_groups["Uber Shader"]
                                
                                uber_nodegroup.location = 0, 0
                                uber_nodegroup.width = 300
                                uber_nodegroup.width_hidden = 300
                                uber_nodegroup.name = "Uber Shader"
                                uber_nodegroup.label = "Uber Shader"

                                output_node.location = 400, 0

                                links = mat.node_tree.links

                                links.new(output_node.inputs[0],uber_nodegroup.outputs[0])


                                # Add Diffuse node and link it to Uber shader
                                if not "_d DiffuseMap" in mat_nodes:
                                    _d = mat_nodes.new(type='ShaderNodeTexImage')
                                    _d.name = _d.label = "_d DiffuseMap"
                                else:
                                    _d = mat_nodes["_d DiffuseMap"]
                                _d.location = (-464, 300)
                                _d.width = _d.width_hidden = 300
                                links.new(uber_nodegroup.inputs[0],_d.outputs[0])
                                _d.image = diffusemap_image


                                # Add Rotation node and link it to Uber shader
                                if matxml_derived != "EmissiveOnly"
                                    if not "_n RotationMap" in mat_nodes:
                                        _n = mat_nodes.new(type='ShaderNodeTexImage')
                                        _n.name = _n.label = "_n RotationMap"
                                    else:
                                        _n = mat_nodes["_n RotationMap"]
                                    _n.location = (-464, 0)
                                    _n.width = _n.width_hidden = 300
                                    links.new(uber_nodegroup.inputs[1],_n.outputs[0])
                                    links.new(uber_nodegroup.inputs[2],_n.outputs[1])
                                    _n.image = rotationmap_image
                                else:
                                    uber_nodegroup.inputs[1] = [0, 0.5, 0, 1]
                                    uber_nodegroup.inputs[2] = 0.5


                                # Add Gloss node and link it to Uber shader
                                if not "_s GlossMap" in mat_nodes:
                                    _s = mat_nodes.new(type='ShaderNodeTexImage')
                                    _s.name = _s.label = "_s GlossMap"
                                else:
                                    _s = mat_nodes["_s GlossMap"]
                                _s.location = (-464, -300)
                                _s.width = _s.width_hidden = 300
                                links.new(uber_nodegroup.inputs[3],_s.outputs[0])
                                links.new(uber_nodegroup.inputs[4],_s.outputs[1])
                                _s.image = glossmap_image

                            else:
                                # ------------------------------------------
                                # For modern version of the shader

                                # Add Uber Shader and link it to Output node
                                uber_nodegroup = mat_nodes.new(type="ShaderNodeHeroEngine")
                                uber_nodegroup.derived = 'UBER'
                                
                                # Adjust transparency and shadows
                                if mat_AlphaMode == 'Test':
                                    uber_nodegroup.alpha_mode = 'CLIP'
                                    try:
                                        mat.shadow_method = 'CLIP'
                                    except:
                                        pass
                                    uber_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                                    try:
                                        mat.shadow_method = 'BLEND'
                                    except:
                                        pass
                                    mat.shadow_method = 'HASHED'
                                    uber_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                else:
                                    try:
                                        mat.shadow_method = 'OPAQUE'
                                    except:
                                        pass
                                    mat.shadow_method = 'NONE'

                                # Set Backface Culling
                                uber_nodegroup.show_transparent_back = (mat_IsTwoSided == "False" and self.use_IsTwoSided_bool == True)
                                
                                uber_nodegroup.location = 0, 0
                                uber_nodegroup.width = 350  # I like to be able to see the names of the textures
                                uber_nodegroup.width_hidden = 300

                                output_node.location = 400, 0

                                # Link the two nodes
                                links = mat.node_tree.links
                                links.new(output_node.inputs[0],uber_nodegroup.outputs[0])

                                # Set shader's texturemap nodes
                                uber_nodegroup.diffuseMap = diffusemap_image
                                uber_nodegroup.glossMap = glossmap_image
                                uber_nodegroup.rotationMap = rotationmap_image

        print("Time spent = ", timeit.timeit() )
        return {"FINISHED"}


# UI is set in ui.py


# ------------------------------------------------------------------
# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_process_uber_mats)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_process_uber_mats)

if __name__ == "__main__":
    register()