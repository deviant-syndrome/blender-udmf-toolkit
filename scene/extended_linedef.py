from ..libs.udmfio_bundled import Sidedef


class ExtendedSidedef(Sidedef):
    def __init__(self, original_sidedef, index):
        # Copy over all attributes from the original Sidedef to the new instance
        super().__init__()
        self.__dict__ = original_sidedef.__dict__.copy()

        # Set the index
        self.index = index
