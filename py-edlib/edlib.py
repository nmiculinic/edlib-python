import ctypes as c
import os


class AligmentResult:
    def __init__(self, edit_distance, start_locations, end_locations, alignment, alphabet_size):
        self.edit_distance = edit_distance
        self.start_locations = start_locations
        self.end_locations = end_locations
        self.alignment = alignment
        self.alphabet_size = alphabet_size


class Edlib:
    """
    Edlib class
    TODO: Docs

    Edit operations.
    EDLIB_EDOP_MATCH 0    //!< Match.
    EDLIB_EDOP_INSERT 1   //!< Insertion to target = deletion from query.
    EDLIB_EDOP_DELETE 2   //!< Deletion from target = insertion to query.
    EDLIB_EDOP_MISMATCH 3 //!< Mismatch.
    """

    '''
    Global method. This is the standard method.
    Useful when you want to find out how similar is first sequence to second sequence.
    '''
    EDLIB_MODE_NW = 0

    '''
    Prefix method. Similar to global method, but with a small twist - gap at query end is not penalized.
    What that means is that deleting elements from the end of second sequence is "free"!
    For example, if we had "AACT" and "AACTGGC", edit distance would be 0, because removing "GGC" from the end
    of second sequence is "free" and does not count into total edit distance. This method is appropriate
    when you want to find out how well first sequence fits at the beginning of second sequence.
    '''
    EDLIB_MODE_SHW = 1

    '''
    Infix method. Similar as prefix method, but with one more twist - gaps at query end and start are
    not penalized. What that means is that deleting elements from the start and end of second sequence is "free"!
    For example, if we had ACT and CGACTGAC, edit distance would be 0, because removing CG from the start
    and GAC from the end of second sequence is "free" and does not count into total edit distance.
    This method is appropriate when you want to find out how well first sequence fits at any part of
    second sequence.
    For example, if your second sequence was a long text and your first sequence was a sentence from that text,
    but slightly scrambled, you could use this method to discover how scrambled it is and where it fits in
    that text. In bioinformatics, this method is appropriate for aligning read to a sequence.
    '''
    EDLIB_MODE_HW = 2

    ''' Find edit distance and end locations.'''
    EDLIB_TASK_DISTANCE = 0

    '''Find edit distance, end locations and start locations.'''
    EDLIB_TASK_LOC = 1

    ''' Find edit distance, end locations and start locations and alignment path.'''
    EDLIB_TASK_PATH = 2

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
        path = os.path.join(root_dir, 'lib', 'libedlib.so')
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

        free_result_prototype = c.CFUNCTYPE(
            None,
            Edlib._EdlibAlignResult,
        )

        self._free_result = free_result_prototype(('edlibFreeAlignResult', self._libedlib))

    @staticmethod
    def _wrap_results(edlib_result):
        starts = [edlib_result.startLocations[i] for i in range(edlib_result.numLocations)]
        ends = [edlib_result.endLocations[i] for i in range(edlib_result.numLocations)]

        return AligmentResult(
            edlib_result.editDistance,
            starts,
            ends,
            [ord(edlib_result.alignment[i]) for i in range(edlib_result.alignmentLength)],
            edlib_result.alphabetLength
        )

    def align(self, query, target, align_mode=EDLIB_MODE_NW, align_task=EDLIB_TASK_PATH, max_distance=-1):
        """
        :param query:
            query sequence
        :param target:
            target sequence
        :param align_mode:
            alignment method
        :param align_task:
            required alignment data
        :param max_distance:
            set to non-negative value to tell edlib that edit distance is not larger than k,
            k to negative value and edlib will internally auto-adjust k until score is found
        :return:
        """
        conf = Edlib._EdlibAlignConfig(max_distance, align_mode, align_task)

        query_c_arr = c.c_char_p(query.encode())
        target_c_arr = c.c_char_p(target.encode())

        query_len = c.c_int(len(query))
        target_len = c.c_int(len(target))

        edlib_result = self._align_f(query_c_arr, query_len, target_c_arr, target_len, conf)
        py_result = self._wrap_results(edlib_result)
        self._free_result(edlib_result)
        return py_result


def demo():
    edlib = Edlib()
    result = edlib.align("aaa", "tttttaaattttt")
    print(result.edit_distance)
    print(result.alignment)
    print(result.alphabet_size)


if __name__ == "__main__":
    demo()
