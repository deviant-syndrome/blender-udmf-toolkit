from .popup import register as popup_register
from .preferences import register as preferences_register

if __name__ == "__main__":
    preferences_register()
    popup.register()