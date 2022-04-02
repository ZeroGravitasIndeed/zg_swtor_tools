import bpy
import pathlib
import xml.etree.ElementTree as ET
import addon_utils



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
                            mat_tree = ET.parse(mat_tree_filepath)
                        except:
                            continue  # disregard and go for the next material
                        mat_root = mat_tree.getroot()

                        mat_Derived = mat_root.find("Derived").text

                        if mat_Derived == "Uber":

                            # ----------------------------------------------
                            # Decide whether to empty the material for processing or disregard it
                            mat_nodes = mat.node_tree.nodes
                            if self.use_overwrite_bool == True:
                                for node in mat_nodes:
                                    mat_nodes.remove(node)
                            elif "Principled BSDF" in mat_nodes and not (("Uber Shader" in mat_nodes) or ("ShaderNodeHeroEngine" in mat_nodes)):
                                for node in mat_nodes:
                                    mat_nodes.remove(node)
                            else:
                                continue  # Entirely disregard material and go for the next one


                            # ----------------------------------------------
                            # Basic material settings
                            # mat.use_nodes = True  # Redundant?
                            mat.use_fake_user = False

                            # Read and set some basic material attributes
                            mat_AlphaMode = mat_root.find("AlphaMode").text
                            mat_AlphaTestValue = mat_root.find("AlphaTestValue").text
                            mat_IsTwoSided = mat_root.find("IsTwoSided").text

                            # Adjust transparency and shadows
                            mat.alpha_threshold = float(mat_AlphaTestValue)
                            if mat_AlphaMode == 'Test':
                                mat.blend_method = 'CLIP'
                                mat.shadow_method = 'CLIP'
                            elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                                mat.blend_method = 'BLEND'
                                mat.shadow_method = 'HASHED'
                            else:
                                mat.blend_method = 'OPAQUE'
                                mat.shadow_method = 'NONE'

                            # Set Backface Culling
                            mat.use_backface_culling = (mat_IsTwoSided == "False" and self.use_IsTwoSided_bool == True)
                        

                            # Add Output node to emptied material
                            # (why can't I do output_node = mat_node.new('ShaderNodeOutputMaterial') instead?)
                            output_node = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')


                            # ----------------------------------------------
                            # Gather texture maps

                            DiffuseMap_image = None
                            RotationMap_image = None
                            GlossMap_image = None

                            texturemap_image = None

                            mat_inputs = mat_root.findall("input")
                            for mat_input in mat_inputs:
                                mat_semantic = mat_input.find("semantic").text
                                mat_type = mat_input.find("type").text
                                mat_value = mat_input.find("value").text

                                # Parsing and loading texture maps

                                if mat_type == "texture":
                                    mat_value = mat_value.replace("\\", "/")
                                    texturemap_path = swtor_resources_path + "/" + mat_value + ".dds"
                                    try:
                                        texturemap_image = bpy.data.images.load(texturemap_path, check_existing=True)
                                        texturemap_image.colorspace_settings.name = 'Raw'
                                    except:
                                        pass
                                    if mat_semantic == "DiffuseMap":
                                        DiffuseMap_image = texturemap_image
                                    elif mat_semantic == "RotationMap1":
                                        RotationMap_image = texturemap_image
                                    elif mat_semantic == "GlossMap":
                                        GlossMap_image = texturemap_image


                            # ----------------------------------------------
                            # Add Uber Shader and connect texturemaps

                            if gr2_addon_legacy:
                                # For Legacy version of the shader

                                # Add Uber Shader and link it to Output node
                                if not "Uber Shader" in mat_nodes:
                                    uber_nodegroup = mat_nodes.new(type="ShaderNodeGroup")
                                    uber_nodegroup.node_tree = bpy.data.node_groups["Uber Shader"]
                                else:
                                    uber_nodegroup = mat_nodes["Uber Shader"]
                                
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
                                _d.image = DiffuseMap_image


                                # Add Rotation node and link it to Uber shader
                                if not "_n RotationMap" in mat_nodes:
                                    _n = mat_nodes.new(type='ShaderNodeTexImage')
                                    _n.name = _n.label = "_n RotationMap"
                                else:
                                    _n = mat_nodes["_n RotationMap"]
                                _n.location = (-464, 0)
                                _n.width = _n.width_hidden = 300
                                links.new(uber_nodegroup.inputs[1],_n.outputs[0])
                                links.new(uber_nodegroup.inputs[2],_n.outputs[1])
                                _n.image = RotationMap_image


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
                                _s.image = GlossMap_image

                            else:
                                # For current version of the shader

                                # Add Uber Shader and link it to Output node
                                if not "ShaderNodeHeroEngine" in mat_nodes:
                                    uber_nodegroup = mat_nodes.new('ShaderNodeHeroEngine')
                                else:
                                    uber_nodegroup = mat_nodes["Uber Shader"]

                                uber_nodegroup.derived = 'UBER'

                                uber_nodegroup.location = [-200, 100]

                                uber_nodegroup.location = 0, 0
                                uber_nodegroup.width = 300
                                uber_nodegroup.width_hidden = 300
                                uber_nodegroup.name = "SWTOR"
                                uber_nodegroup.label = ""

                                output_node.location = 400, 0

                                links = mat.node_tree.links

                                links.new(output_node.inputs[0],uber_nodegroup.outputs[0])


                                # Link the two nodes
                                links.new(output_node.inputs['Surface'],uber_nodegroup.outputs['Shader'])

                                # Set shader's texturemap nodes

                                if 'Uber Shader' in mat_nodes:
                                    underlying_uber_nodegroup = uber_nodegroup.node_tree
                                    underlying_uber_nodegroup["diffuseMap"] = DiffuseMap_image
                                    underlying_uber_nodegroup["glossMap"] = GlosseMap_image
                                    underlying_uber_nodegroup["rotationMap"] = RotationMap_image
                                else:
                                    print("No underlying nodegroup found.")


                        elif mat_Derived == "EmissiveOnly":
                            pass

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