
import os
from UnpackParser import UnpackParser
from bangmedia import unpack_mapsforge

class MapsforgeUnpackParser(UnpackParser):
    extensions = []
    signatures = [
        (0, b'mapsforge binary OSM')
    ]
    pretty_name = 'mapsforge'

    def parse_and_unpack(self, fileresult, scan_environment, offset, unpack_dir):
        return unpack_mapsforge(fileresult, scan_environment, offset, unpack_dir)

