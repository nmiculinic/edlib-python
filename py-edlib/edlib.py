import os
import ctypes as c


class AligmentResult:

    def __init__(self, edit_distance, start_locations, end_locations, alignment, alphabet_size):
        self.edit_distance = edit_distance
        self.start_locations = start_locations
        self.end_locations = end_locations
        self.alignment = alignment
        self.alphabet_size = alphabet_size


class Edlib:

    class _EdlibAlignConfig(c.Structure):
        _fields_ = [("k", c.c_int),
                    ("align_mode", c.c_int),
                    ("align_task", c.c_int)]

    class _EdlibAlignResult(c.Structure):
        _fields_ = [("editDistance", c.c_int),
                    ("endLocations", c.POINTER(c.c_int)),
                    ("startLocations", c.POINTER(c.c_int)),
                    ("numLocations", c.c_int),
                    ("alignment", c.POINTER(c.c_char)),
                    ("alignmentLength", c.c_int),
                    ("alphabetLength", c.c_int)]

    def __init__(self):
        # temp hardcoded load path,
        root_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        path = os.path.join(root_dir, '..', 'lib', 'libedlib.so')
        self._libedlib = c.cdll.LoadLibrary(path)
        self._initialize_functions()

    def _initialize_functions(self):
        align_prototype = c.CFUNCTYPE(
            Edlib._EdlibAlignResult,
            c.c_char_p,
            c.c_int,
            c.c_char_p,
            c.c_int
        )
        self._align_f = align_prototype(('edlibAlign', self._libedlib))

        default_conf_prototype = c.CFUNCTYPE(Edlib._EdlibAlignConfig)
        self._default_conf_f = default_conf_prototype(
            ('edlibDefaultAlignConfig', self._libedlib))

    @staticmethod
    def _wrap_results(edlib_result):
        starts, ends = [], []

        for i in range(edlib_result.numLocations):
            starts.append(edlib_result.startLocations[i])
            ends.append(edlib_result.endLocations[i])

        return AligmentResult(
            edlib_result.editDistance,
            starts,
            ends,
            [edlib_result.alignment[i] for i in range(edlib_result.alignmentLength)],
            edlib_result.alphabetLength
        )

    def align(self, query, target):
        default_conf = Edlib._EdlibAlignConfig(-1, 0, 2)

        query_c_arr = c.c_char_p(query.encode())
        target_c_arr = c.c_char_p(target.encode())

        query_len = c.c_int(len(query))
        target_len = c.c_int(len(target))

        res = self._align_f(query_c_arr, query_len, target_c_arr, target_len, default_conf)
        return self._wrap_results(res)


def demo():
    edlib = Edlib()
    result = edlib.align("aaa", "tttttaaattttt")
    print(result)

if __name__=="__main__":
    demo()
