import os
import ctypes as c


class Edlib:
    def __init__(self):
        root_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        self.libedlib = c.cdll.LoadLibrary(os.path.join(root_dir, '..', 'lib', 'libedlib.so'))

    def align(self, query, target):
        pass

Edlib()
