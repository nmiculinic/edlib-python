import os
import ctypes





class Edlib:

    class _EdlibAlignConfig(ctypes.Structure):
        _fields_ = [("k", ctypes.c_int),
                    ("align_mode", ctypes.c_int),
                    ("align_task", ctypes.c_int)]

    class _EdlibAlignResult(ctypes.Structure):
        _fields_ = [("editDistance", ctypes.c_int),
                    ("endLocations", ctypes.c_void_p),
                    ("startLocations", ctypes.c_void_p),
                    ("numLocations", ctypes.c_int),
                    ("alignment", ctypes.c_char_p),
                    ("alignmentLength", ctypes.c_int),
                    ("alphabetLength", ctypes.c_int)]

    def __init__(self):
        # temp hardcoded load path,
        root_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        path = os.path.join(root_dir, '..', 'lib', 'libedlib.so')
        self._libedlib = ctypes.cdll.LoadLibrary(path)

        align_prototype = ctypes.CFUNCTYPE(
            Edlib._EdlibAlignResult,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int
        )
        self._align_f = align_prototype(('edlibAlign', self.libedlib))

        default_conf_prototype = ctypes.CFUNCTYPE(Edlib._EdlibAlignConfig)
        self._default_conf_f = default_conf_prototype(
            ('edlibDefaultAlignConfig', self.libedlib))

    def align(self, query, target):
        default_conf = self.default_conf_f()

        query_c_arr = ctypes.c_char_p(query.encode())
        target_c_arr = ctypes.c_char_p(target.encode())

        query_len = ctypes.c_int(len(query))
        target_len = ctypes.c_int(len(target))

        return self._align_f(query_c_arr, query_len, target_c_arr, target_len, default_conf)


def demo():
    edlib = Edlib()
    result = edlib.align("aaa", "bbb")
    print(result.editDistance)

if __name__=="__main__":
    demo()
