#!/usr/bin/env python

from setuptools import setup
import distutils.command.build as _build
import distutils.command.build_clib as _build_clib
import setuptools.command.install as _install

import sys
import os
import os.path as op
import distutils.spawn as ds
import distutils.dir_util as dd

root_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))


class build_clib(_build_clib.build_clib):
    def run(self):
        if ds.find_executable('cmake') is None:
            print("CMake  is required to build SimX")
            print("Please install cmake version >= 2.6 and re-run setup")
            sys.exit(-1)

        print("Configuring edlib build with CMake.... ")
        dd.mkpath(op.join(root_dir, 'build'))
        try:
            cwd = os.getcwd()
            os.chdir(op.join(root_dir, 'build'))
            ds.spawn(['cmake', op.join(root_dir, 'edlib')])
            ds.spawn(['make'])
            os.chdir(cwd)
        except ds.DistutilsExecError:
            print("Error while running cmake")
            print("run 'setup.py build --help' for build options")
            print("You may also try editing the settings in CMakeLists.txt file and re-running setup")
            sys.exit(-1)
        super().run()

setup(
    name="edlib",
    version='0.1',
    description='edlib bindings',
    # requires = ["greenlet"],
    # install_requires = ["greenlet"],
    include_package_data=True,
    # url = 'http://simx.lanl.gov',
    # author='Sunil Thulasidasan, Lukas Kroc and others',
    # author_email = 'simx-dev@lanl.gov',
    license="MIT",
    # platforms = ['GNU/Linux', 'Unix', 'Mac OS-X'],

    # ext_modules is not present here. This will be generated through CMake via the
    # build or install commands
    cmdclass={'build_clib': build_clib},
    # zip_safe=False,
    # packages=['simx', 'simx.core', 'simx.os'],
)
