from distutils.core import setup
import requests.certs
import py2exe


setup(
    name='hogge',
    version='1.0.1',
    url='https://github.com/igortg/ir_clubchamps',
    license='LGPL v3.0',
    author='Igor T. Ghisi',
    description='',
    console=[{
        "dest_base": "ir_clubchamps",
        "script": "main.py",
    }],
    zipfile = None,
    data_files = [(".", [requests.certs.where()])],
    options={
        "py2exe": {
            "compressed": True,
            "dll_excludes": ["msvcr100.dll"],
            "excludes": ["Tkinter"],
            "bundle_files": 1,
            "dist_dir": "ir_clubchamps"
        }
    },
)


