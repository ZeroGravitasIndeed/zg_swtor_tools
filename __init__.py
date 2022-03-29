import sys
import importlib

# Add-on Metadata

bl_info = {
    "name": "ZG SWTOR Tools",
    "author": "ZeroGravitas",
    "version": (1, 0),
    "blender": (2, 83, 0),
    "category": "SWTOR",
    "location": "Operator Search",
    "description": "Diverse SWTOR asset-handling tools",
    "warning": "This Add-on's Uber Material Processor tool requires the SWTOR Legacy Uber Shader. Please read its tooltip before use",
    "doc_url": "",
    "tracker_url": "",
}

# Add-on modules loader:
# Simplifies coding the loading of the modules to keeping a list of their names
# (See https://b3d.interplanety.org/en/creating-multifile-add-on-for-blender/ )

modulesNames = [
    'ui',
    'preferences',
    'process_uber_mats',
    'remove_doubles',
    'deduplicate_nodegroups'
    ]
  
modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":
    register()