#!/usr/bin/env python

import itertools
import os
import setuptools
import shutil
import sys
import time


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

INSTALL_DIR = os.path.join(sys.prefix, 'share', 'noVNC')
TOPDIR = os.path.abspath(os.path.dirname(__file__))
VFILE  = os.path.join(TOPDIR, 'version.py')

args = filter(lambda x: x[0] != '-', sys.argv)
command = args[1] if len(args) > 1 else ''

if command == 'sdist':
    PISTON_VERSION = os.environ['PISTON_VERSION']
    with file(VFILE, 'w') as f:
        f.write('''#!/usr/bin/env python\nVERSION = '%s'\n''' % PISTON_VERSION)
elif command == 'develop':
    PISTON_VERSION = time.strftime('9999.0.%Y%m%d%H%M%S', time.localtime())
    with file(VFILE, 'w') as f:
        f.write('''#!/usr/bin/env python\nVERSION = '%s'\n''' % PISTON_VERSION)
elif command is None:
    PISTON_VERSION = '9999999999-You_did_not_set_a_version'
else:
    assert os.path.exists(VFILE), 'version.py does not exist, please set PISTON_VERSION (or run make_version.py for dev purposes)'
    import version as pistonversion
    PISTON_VERSION = pistonversion.VERSION

# Workaround for https://github.com/pypa/pip/issues/288
def snap_symlink(path):
    if not os.path.islink(path):
        return path
    real = os.path.realpath(os.path.normpath(path))
    os.unlink(path)
    shutil.copy(real, path)
    return path

data_files = {}
for p in itertools.chain.from_iterable([setuptools.findall(x) for x in 'images', 'include', 'utils']):
    d, _ = os.path.split(p)
    full = os.path.join(INSTALL_DIR, d)
    data_files[full] = data_files.get(full, [])
    data_files[full].append(snap_symlink(p))

data_files[INSTALL_DIR] = map(snap_symlink, ['vnc.html', 'vnc_auto.html', 'favicon.ico'])

setuptools.setup(name='noVNC',
    zip_safe = False,
    version=PISTON_VERSION,
    description='noVNC is a HTML5 VNC client that runs well in any modern browser including mobile browsers',
    data_files = data_files.items(),
    author='',
    author_email='',
    maintainer='',
    maintainer_email='',
    url = 'http://github.com/piston/noVNC.git',
    platforms=["any"],
)
