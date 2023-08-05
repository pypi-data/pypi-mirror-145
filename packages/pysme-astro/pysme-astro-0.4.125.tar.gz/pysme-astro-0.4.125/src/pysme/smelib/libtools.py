# -*- coding: utf-8 -*-
"""
These libtools are used to locate, download, and install the SME C/Fortran
library.
"""

import ctypes as ct
import logging
import os
import platform
import subprocess
import sys
import zipfile
from os.path import dirname, exists, join

import wget

logger = logging.getLogger(__name__)


def download_libsme(loc=None):
    """
    Download the SME library and the necessary datafiles

    Parameters
    ----------
    loc : str, optional
        the path to the location the files should be placed,
        by default they are placed so that PySME can find and use them

    Raises
    ------
    KeyError
        If no existing library is found for this system
    """
    if loc is None:
        loc = dirname(dirname(get_full_libfile()))
    # Download compiled library from github releases
    print("Downloading and installing the latest libsme version for this system")
    aliases = {
        "Linux": "manylinux2014_x86_64",
        "Windows": "windows",
        "Darwin": "macos",
    }
    system = platform.system()

    try:
        system = aliases[system]
    except KeyError:
        raise KeyError(
            f"Could not find the associated compiled library for this system {system}."
            " Either compile it yourself and place it in src/pysme/ or open an"
            " issue on Github. Supported systems are: Linux, MacOS, Windows."
        )

    github_releases_url = "https://github.com/AWehrhahn/SMElib/releases/latest/download"
    github_releases_fname = "{system}-gfortran.zip".format(system=system)
    url = github_releases_url + "/" + github_releases_fname
    fname = join(loc, github_releases_fname)

    if exists(fname):
        os.remove(fname)

    print("Downloading file %s" % url)
    os.makedirs(loc, exist_ok=True)
    wget.download(url, out=loc)

    zipfile.ZipFile(fname).extractall(loc)

    os.remove(fname)


def compile_interface():
    """
    Compiles the Python Module Interface to the SME library. This needs to be
    called once, before trying to import _smelib.

    Since the module uses the setup.py method to be compiled,
    it is somewhat hacked together to make it work.
    """
    libdir = join(dirname(__file__))
    executable = sys.executable
    if executable is None:
        # If python is unable to identify the path to its own executable use python3
        # This is unlikely to happen for us though
        executable = "python3"
    cwd = os.getcwd()
    # We need to swith to the correct directory and back, for setup.py to work
    os.chdir(libdir)
    subprocess.run([executable, "setup.py", "build_ext", "--inplace"])
    os.chdir(cwd)


def get_lib_name():
    """Get the name of the SME C library"""
    system = platform.system().lower()

    if system == "windows":
        return "libsme-5.dll"

    arch = platform.machine()
    bits = 64  # platform.architecture()[0][:-3]

    return "sme_synth.so.{system}.{arch}.{bits}".format(
        system=system, arch=arch, bits=bits
    )


def get_lib_directory():
    """
    Get the directory name of the library. I.e. 'lib' on all systems
    execpt windows, and 'bin' on windows
    """
    if platform.system() in ["Windows"]:
        dirpath = "bin"
    else:
        # For Linux/MacOS
        dirpath = "lib"
    return dirpath


def get_full_libfile():
    """Get the full path to the sme C library"""
    localdir = dirname(dirname(__file__))
    libfile = get_lib_name()
    dirpath = get_lib_directory()
    libfile = join(localdir, dirpath, libfile)
    return libfile


def load_library(libfile=None):
    """
    Load the SME library using cytpes.CDLL

    This is useful and necessary for the pymodule interface to find the
    library.

    Parameters
    ----------
    libfile : str, optional
        filename of the library to load, by default use the SME library in
        this package

    Returns
    -------
    lib : CDLL
        library object of the SME library
    """
    if libfile is None:
        libfile = get_full_libfile()
    try:
        os.add_dll_directory(dirname(libfile))
    except AttributeError:
        newpath = dirname(libfile)
        if "PATH" in os.environ:
            newpath += os.pathsep + os.environ["PATH"]
        os.environ["PATH"] = newpath
    return ct.CDLL(str(libfile))


def get_full_datadir():
    """
    Get the filepath to the datafiles of the SME library
    """
    localdir = dirname(dirname(__file__))
    datadir = join(localdir, "share/libsme/")
    return datadir
