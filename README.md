# ZeroGravitas's SWTOR Tools
A Blender Add-on with a set of miscellaneous tools to use on **Star Wars: The Old Republic** MMO's assets. It will grow on features as those occur to me.


## Installation

The installation of the Add-on in Blender follows the usual practices:

1. Download the Add-on as a zg_swtors_tool.zip file. Don't unZip it: it's used as such .zip.
2. In Blender, go to Edit menu > Preferences option > Add-ons tab > Install… button.
3. Select the Add-on in the file dialog box and click on the Install Add-on button.
4. The Add-on will appear in the Add-ons list with its checkbox un-ticked. Tick it to enable the Add-on.
5. Twirl the arrow preceding the check-box to reveal some information and, most importantly, **the Add-on's Preferences**. Note that it asks for **the path of a "resources" folder**.

    Some of the Add-on's features depend on looking for information and game assets inside a SWTOR assets extraction (typically produced by apps such as SWTOR Slicers or EasyMYP). In the case of a SWTOR Slicers extraction, the "resources" folder is inside the folder set as that app's Output Folder.
    
    Use the folder icon to produce a file dialog box where to locate the "resources" folder, or type or copy the folder path in the filepath field.

The Add-on's tools will appear in the 3D Viewport's Sidebar ('n' key), in the "ZG SWTOR" tab.

## SWTOR Materials Tools:

### Process Uber Materials:
Processes all the Uber-type materials in a selection of objects, plus any EmissiveOnly-type (glass) ones.

Options:
* **Overwrite Uber Materials** (off by default): overwrite already present Uber and EmissiveOnly objects's materials, which allows to convert Uber materials from Legacy to modern and viceversa. The option appears in the Undo box at the bottom-left side of the 3D Viewport.
* **Collect Collider Objects** (on by default): adds all objects with an "Util_collision_hidden" material in a Collection named "Collider Objects".

**It needs the presence of an enabled SWTOR importer Add-on** ("io_scene_gr2") in Blender, either the latest version or the Legacy one, as it uses their Uber materials, whichever is there. In the case of the Legacy materials, importing any throwaway game object might be needed in order to generate the required material template if none are there.

This tool produces a simplistic glass material, Principled Shader-based, for EmissiveOnly-type materials such as those in spaceship windows, too.

As some sets of objects, such as spaceship interiors, can easily have a hundred materials or more, Blender might look like being unresponsive while processing them. Its progress can be followed in Blender's Console output, which will show the objects and materials being processed. Some error messages are prone to appear, due to some unintended interactions with the modern version of the SWTOR Importer Add-on: those are expected, and don't affect the final result.

### Deduplicate Scene's Nodegroups:
Consolidates all duplicates of a node in the scene ("node.001", "node.002", etc.) so that they become instances of the original instead of independent ones. The copies are marked as "zero users" so that, after saving the project, the next time it is opened they will be discarded (that's how Blender deals with such things).
* It acts on all the nodes of a scene, and doesn't require a selection of objects.

## SWTOR Objects Tools:

### Merge Double Vertices:
Merges "duplicate" vertices (applies a "Merge By Distance" with a tolerance of 0.000001 m.), which usually solves many issues when fusing body parts or applying Subdivision or Multiresolution Modifiers.
* Requires a selection of one or several game objects.
* When selecting multiple objects, the tool acts on each of them separately so as not to merge vertices of different objects by accident.
