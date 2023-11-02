import io
from io import StringIO

from ..libs import WADFile
from ..libs import WriteableLump
from ..libs import write_lumps_to_pwad
from ..libs import load_udmf_map
from ..libs import write_udmf_map
import bpy


class MinimalUDMFPWAD:
    def __init__(self, codename, udmf_map_text):
        self.udmf_map_text = udmf_map_text
        self.codename = codename

    def get_lumps(self):
        lumps = [
            WriteableLump(self.codename, b""),
            WriteableLump("TEXTMAP", self.udmf_map_text),
            WriteableLump("ENDMAP", b""),
        ]
        return lumps


def load_map_from_pwad(pwad_filename):
    wad_file = WADFile(pwad_filename)
    map_bytes = wad_file.read_lump("TEXTMAP")
    io = StringIO(map_bytes.decode("utf-8"))
    return load_udmf_map(io)


def embed_udmf_map(udmf_map):
    with io.StringIO() as f:
        write_udmf_map(udmf_map, f)
        data = f.getvalue()

    # Check if the text block already exists
    udmf_text_block = bpy.data.texts.get("EmbeddedUDMF")

    # If it exists, clear its content
    if udmf_text_block:
        udmf_text_block.clear()
    else:  # If it doesn't exist, create a new one
        udmf_text_block = bpy.data.texts.new(name="EmbeddedUDMF")

    # Assign the new content to the text block
    udmf_text_block.from_string(data)


def export_map_to_pwad(pwad_filename, udmf_map):
    # Create a buffer to write the UDMF map to
    buffer = io.StringIO()
    write_udmf_map(udmf_map, buffer)

    # Get the contents of the buffer
    udmf_text = buffer.getvalue()
    pwad = MinimalUDMFPWAD("E1M1", udmf_text.encode("utf-8"))
    write_lumps_to_pwad(pwad.get_lumps(), pwad_filename)

    buffer.close()
    embed_udmf_map(udmf_map)
