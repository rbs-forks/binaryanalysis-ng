import os
from . import ico

class IcoParser:
    def __init__(self):
        self.unpacked_size = 0
        self.unpack_results = {}
    def parse(self, fileresult, scan_environment, offset):
        self.infile.seek(offset)
        self.data = ico.Ico.from_io(self.infile)
        self.unpacked_size = self.infile.tell() - offset
        for i in self.data.images:
            self.unpacked_size = max(self.unpacked_size, i.ofs_img + i.len_img)
    def parse_and_unpack(self, fileresult, scan_environment, offset, unpack_dir):
        try:
            filename_full = scan_environment.unpack_path(fileresult.filename)
            with filename_full.open('rb') as self.infile:
                self.parse(fileresult, scan_environment, offset)
                self.unpack_results = {
                        'status': True,
                        'length': self.unpacked_size
                    }
                self.set_metadata_and_labels(self.data)
                files_and_labels = self.unpack(fileresult, scan_environment, offset, unpack_dir)
                self.unpack_results['filesandlabels'] = files_and_labels
                return self.unpack_results
        except Exception as e:
            # raise ParserException(*e.args)
            unpacking_error = {
                    'offset': offset + self.unpacked_size,
                    'fatal' : False,
                    'reason' : "{}: {}".format(e.__class__.__name__,str(e))
                }
            return { 'status' : False, 'error': unpacking_error }
    def unpack(self, fileresult, scan_environment, offset, unpack_dir):
        """extract any files from the input file"""
        if offset != 0 or self.unpacked_size != fileresult.filesize:
            outfile_rel = os.path.join(unpack_dir, "unpacked.ico")
            outfile_full = scan_environment.unpack_path(outfile_rel)
            os.makedirs(outfile_full.parent, exist_ok=True)
            outfile = open(outfile_full, 'wb')
            os.sendfile(outfile.fileno(), self.infile.fileno(), offset, self.unpacked_size)
            outfile.close()
            outlabels = self.unpack_results['labels'] + ['unpacked']
            return [ (outfile_rel, outlabels) ]
        else:
            return []
    def set_metadata_and_labels(self, metadata):
        """sets metadata and labels for the unpackresults"""
        self.unpack_results['labels'] = ['graphics','ico','resource']
        self.unpack_results['metadata'] = {}


