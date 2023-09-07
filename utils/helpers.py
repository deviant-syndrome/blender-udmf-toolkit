from io import StringIO

from ..libs import WADFile
from ..libs import load_udmf_map


def load_map_from_pwad(pwad_filename):
    wad_file = WADFile(pwad_filename)
    map_bytes = wad_file.read_lump('TEXTMAP')
    io = StringIO(map_bytes.decode('utf-8'))
    return load_udmf_map(io)


#
# class MinimalUDMFPWAD:
#     def __init__(self, codename, udmf_map_text):
#         self.udmf_map_text = udmf_map_text
#         self.codename = codename
#
#     def get_lumps(self):
#         lumps = [WriteableLump(self.codename, b''),
#                  WriteableLump('TEXTMAP', self.udmf_map_text),
#                  WriteableLump('ENDMAP', b'')]
#         return lumps
