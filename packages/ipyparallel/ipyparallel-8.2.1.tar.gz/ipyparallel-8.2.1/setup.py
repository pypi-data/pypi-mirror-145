#!/usr/bin/env python
# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.
import glob
import os
import sys

import setuptools
from setuptools.command.bdist_egg import bdist_egg


class bdist_egg_disabled(bdist_egg):
    """Disabled version of bdist_egg

    Prevents setup.py install performing setuptools' default easy_install,
    which it should never ever do.
    """

    def run(self):
        sys.exit(
            "Aborting implicit building of eggs. Use `pip install .` to install from source."
        )


# the name of the project
name = 'ipyparallel'

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))
pkg_root = pjoin(here, name)
lab_path = pjoin(pkg_root, 'labextension')

package_data_spec = {'ipyparallel.nbextension': [pjoin('static', '*')]}

data_files_spec = [
    # all extension-enabling config files
    (
        'etc/jupyter',
        'etc/jupyter',
        '**',
    ),
    # nbclassic extension
    (
        'share/jupyter/nbextensions/ipyparallel',
        'ipyparallel/nbextension/static',
        '*',
    ),
    # lab extension
    ('share/jupyter/labextensions/ipyparallel-labextension', here, 'install.json'),
    ('share/jupyter/labextensions/ipyparallel-labextension', lab_path, '**'),
]

version_ns = {}
with open(pjoin(here, name, '_version.py')) as f:
    exec(f.read(), {}, version_ns)

with open(pjoin(here, "README.md")) as f:
    readme = f.read()

# import setupbase from jupyter_packaging (0.10.4)
if '' not in sys.path:
    sys.path.insert(0, '')
from setupbase import wrap_installers, npm_builder, get_data_files

builder = npm_builder(build_cmd="build:prod", npm="jlpm")

cmdclass = {}
if os.environ.get("IPP_DISABLE_JS") == "1":
    print("Skipping js installation")
else:
    # this tells us if labextension is built at all, not if it's up-to-date
    labextension_built = glob.glob(os.path.join(lab_path, "*"))
    if not labextension_built:
        # jupyter-packaging doesn't update data_files or package_data correctly
        # after running builds
        # run build first if we know it's needed
        builder()
        # don't need to run it again
        needs_js = False

    needs_js = True
    if not os.path.isdir(os.path.join(here, ".git")):
        print("Installing from a dist, not a repo")
        # not in a repo, probably installing from sdist
        # could be git-archive, though!
        # skip rebuilding js if it's already present
        if labextension_built:
            print(f"Not regenerating labextension in {lab_path}")
            needs_js = False

    if needs_js:
        cmdclass = wrap_installers(pre_develop=builder, pre_dist=builder)


if "bdist_egg" not in sys.argv:
    cmdclass["bdist_egg"] = bdist_egg_disabled

setup_args = dict(
    name=name,
    version=version_ns["__version__"],
    packages=setuptools.find_packages(),
    description="Interactive Parallel Computing with IPython",
    data_files=get_data_files(data_files_spec),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="IPython Development Team",
    author_email="ipython-dev@scipy.org",
    url="https://ipython.org",
    license="BSD",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Interactive", "Interpreter", "Shell", "Parallel"],
    classifiers=[
        "Framework :: Jupyter",
        "Framework :: Jupyter :: JupyterLab",
        "Framework :: Jupyter :: JupyterLab :: 3",
        "Framework :: Jupyter :: JupyterLab :: Extensions",
        "Framework :: Jupyter :: JupyterLab :: Extensions :: Prebuilt",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    cmdclass=cmdclass,
    include_package_data=True,
    install_requires=[
        "entrypoints",
        "decorator",
        "pyzmq>=18",
        "traitlets>=4.3",
        "ipython>=4",
        "jupyter_client",
        "ipykernel>=4.4",
        "tornado>=5.1",
        "psutil",
        "python-dateutil>=2.1",
        "tqdm",
    ],
    python_requires=">=3.6",
    extras_require={
        "nbext": ["notebook", "jupyter_server"],
        "serverextension": ["jupyter_server"],
        "labextension": ["jupyter_server", "jupyterlab>=3"],
        "retroextension": ["jupyter_server", "retrolab"],
        "benchmark": ["asv"],
        "test": [
            "pytest",
            "pytest-cov",
            "pytest-asyncio",
            "pytest-tornado",
            "ipython[test]",
            "testpath",
        ],
    },
    entry_points={
        'ipyparallel.controller_launchers': [
            'batch = ipyparallel.cluster.launcher:BatchControllerLauncher',
            'htcondor = ipyparallel.cluster.launcher:HTCondorControllerLauncher',
            'local = ipyparallel.cluster.launcher:LocalControllerLauncher',
            'lsf = ipyparallel.cluster.launcher:LSFControllerLauncher',
            'mpi = ipyparallel.cluster.launcher:MPIControllerLauncher',
            'pbs = ipyparallel.cluster.launcher:PBSControllerLauncher',
            'sge = ipyparallel.cluster.launcher:SGEControllerLauncher',
            'ssh = ipyparallel.cluster.launcher:SSHControllerLauncher',
            'slurm = ipyparallel.cluster.launcher:SlurmControllerLauncher',
            'winhpc = ipyparallel.cluster.launcher:WindowsHPCControllerLauncher',
        ],
        'ipyparallel.engine_launchers': [
            'batch = ipyparallel.cluster.launcher:BatchEngineSetLauncher',
            'htcondor = ipyparallel.cluster.launcher:HTCondorEngineSetLauncher',
            'local = ipyparallel.cluster.launcher:LocalEngineSetLauncher',
            'lsf = ipyparallel.cluster.launcher:LSFEngineSetLauncher',
            'mpi = ipyparallel.cluster.launcher:MPIEngineSetLauncher',
            'pbs = ipyparallel.cluster.launcher:PBSEngineSetLauncher',
            'sge = ipyparallel.cluster.launcher:SGEEngineSetLauncher',
            'slurm = ipyparallel.cluster.launcher:SlurmEngineSetLauncher',
            'ssh = ipyparallel.cluster.launcher:SSHEngineSetLauncher',
            'sshproxy = ipyparallel.cluster.launcher:SSHProxyEngineSetLauncher',
            'winhpc = ipyparallel.cluster.launcher:WindowsHPCEngineSetLauncher',
        ],
        "console_scripts": [
            "ipcluster = ipyparallel.cluster.app:main",
            "ipcontroller = ipyparallel.controller.app:main",
            "ipengine = ipyparallel.engine.app:main",
        ],
    },
    zip_safe=False,
)


if __name__ == "__main__":
    setuptools.setup(**setup_args)
