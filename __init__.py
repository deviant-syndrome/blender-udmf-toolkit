from .operators import import_udmf
from .ui import popup, preferences

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
    preferences.register()

    # ... other registration code ...


def unregister():
    popup.unregister()
    import_udmf.unregister()
    preferences.unregister()
    # ... other unregistration code ...


if __name__ == "__main__":
    register()
