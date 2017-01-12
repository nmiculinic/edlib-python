import os
import ctypes as c


class Edlib:

    def __init__(self):
        # temp hardcoded load path,
        self.libedlib = c.cdll.LoadLibrary('./lib/libedlib.so')

    def align(self, query, target):
        pass

