from ..libs.udmfio_bundled import Sector


class VisualSector(Sector):
    def __init__(self, original):
        # Copy attributes from the original instance
        super().__init__()
        for attr, value in original.__dict__.items():
            setattr(self, attr, value)

        # Set default values for heightceiling and heightfloor
        if self.heightceiling is None:
            self.heightceiling = 0
        if self.heightfloor is None:
            self.heightfloor = 0