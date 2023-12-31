from .operators import export_udmf
from .operators import import_udmf
from .ui import popup, preferences, panels
from .scene import init_props, clear_props

bl_info = {
    "name": "UDMF Toolkit",
    "author": "Deviant Syndrome",
    "version": (1, 0),
    "blender": (2, 83, 0),  # Minimum blender version required
    "location": "File > Import",
    "description": "Import UDMF maps from PWADs into Blender",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export",
}


def register():
    popup.register()
    import_udmf.register()
    export_udmf.register()
    preferences.register()
    panels.register()
    init_props()
    # ... other registration code ...


def unregister():
    popup.unregister()
    import_udmf.unregister()
    export_udmf.unregister()
    preferences.unregister()
    panels.unregister()
    clear_props()
    # ... other unregistration code ...


if __name__ == "__main__":
    register()
