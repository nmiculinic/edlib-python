import os
from ctypes import *


class EdlibAlignConfig(Structure):
    _fields_ = [("k", c_int),
                ("align_mode", c_int),
                ("align_task", c_int)]


class EdlibAlignResult(Structure):
    _fields_ = [("editDistance", c_int),
                ("endLocations", c_void_p),
                ("startLocations", c_void_p),
                ("numLocations", c_int),
                ("alignment", c_char_p),
                ("alignmentLength", c_int),
                ("alphabetLength", c_int)]


class Edlib:
    def __init__(self):
        # temp hardcoded load path,
        root_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        path = os.path.join(root_dir, '..', 'lib', 'libedlib.so')
        self.libedlib = cdll.LoadLibrary(path)

        align_prototype = CFUNCTYPE(
            EdlibAlignResult,
            c_char_p,
            c_int,
            c_char_p,
            c_int
        )
        self.align_f = align_prototype(('edlibAlign', self.libedlib))

        default_conf_prototype = CFUNCTYPE(EdlibAlignConfig)
        self.default_conf_f = default_conf_prototype(
            ('edlibDefaultAlignConfig', self.libedlib))

    def align(self, query, target):
        default_conf = self.default_conf_f()

        query_c_arr = c_char_p(query.encode())
        target_c_arr = c_char_p(target.encode())

        query_len = c_int(len(query))
        target_len = c_int(len(target))

        return self.align_f(query_c_arr, query_len, target_c_arr, target_len, default_conf)


def demo():
    edlib = Edlib()
    result = edlib.align("aaa", "bbb")
    print(result.editDistance)

if __name__=="__main__":
    demo()
