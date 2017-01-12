#!/usr/bin/env python

from setuptools import setup

from setuptools.command import install
from distutils.command.build import build

import sys
import os
import os.path as op
import distutils.spawn as ds
import distutils.dir_util as dd
import distutils.file_util as df

root_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
build_root = root_dir


def build_me():
    if ds.find_executable('cmake') is None:
        print("CMake  is required to build edlib")
        print("Please install cmake version >= 2.6 and re-run setup")
        sys.exit(-1)

    print("Configuring edlib build with CMake.... ")
    dd.mkpath(op.join(build_root, 'build'))
    dd.mkpath(op.join(build_root, 'lib'))
    try:
        cwd = os.getcwd()
        os.chdir(op.join(build_root, 'build'))
        ds.spawn(['cmake', op.join(root_dir, 'edlib')])
        ds.spawn(['make'])
        df.move_file(
            op.join(build_root, 'build', 'lib', 'libedlib.so'),
            op.join(build_root, 'lib')
        )
        os.chdir(cwd)
    except ds.DistutilsExecError:
        print("Error while running cmake")
        print("run 'setup.py build --help' for build options")
        print("You may also try editing the settings in CMakeLists.txt file and re-running setup")
        sys.exit(-1)


class build(build):
    def run(self):
        build_me()
        super().run()


class install(install.install):
    def run(self):
        build_me()
        super().run()


setup(
    name="edlib",
    version='0.1',
    description='edlib bindings',
    url='https://github.com/nmiculinic/edlib-python',
    license="MIT",
    packages=['edlib'],
    cmdclass={'build': build, 'install': install},
    data_files=[('lib', ['lib/libedlib.so'])],
    package_dir={'edlib': 'py-edlib'},
    requires=[],
    zip_safe=False,
)
