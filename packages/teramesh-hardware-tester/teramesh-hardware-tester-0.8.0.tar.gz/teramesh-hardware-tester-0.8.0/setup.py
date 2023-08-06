#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = "teramesh-hardware-tester"
DESCRIPTION = "Scripts to test Teramesh hardware."
URL = "https://gitea.cluster.teramesh.cn/i-DRC/teramesh-hardware-tester"
EMAIL = "michael.sayapin@i-drc.com"
AUTHOR = "Michael Sayapin"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.8.0"

install_requires = [
    "pyserial>=3,<4",
    "esptool>=3.2,<4",
    "click>=8.0,<9",
    "asciimatics>=1.13,<2",
    "uModbus>=1,<2",
]

extras_require = {
    "rpi": [
        "RPi.GPIO ~= 0.7",
    ],
    "dev": [
        "ipython",
        "ipdb",
        "zest.releaser[recommended]",
    ],
    "ui": [
        "fastapi==0.70.1",
        "uvicorn==0.16.0",
        "jinja2==3.0.3",
    ],
}
extras_require["all"] = [v for s in extras_require.values() for v in s]

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload -r pypi dist/*")
        os.system("twine upload -r idrc dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "teramesh-hardware-test=teramesh_hardware_tester.tester:run_tester",
            "teramesh-modbus-test=teramesh_hardware_tester.modbuser:run_modbuser",
            "teramesh-configure=teramesh_hardware_tester.configurer:run_configurer",
            "teramesh-dump-config=teramesh_hardware_tester.dumper:run_dumper",
            "teramesh-modbus-server=teramesh_hardware_tester.modbus_server:run_modbus_server",
            "teramesh-burn-efuses=teramesh_hardware_tester.efuser:run_efuser",
            "tht-ui=teramesh_hardware_tester.server:main",
        ],
    },
    install_requires=install_requires,
    extras_require=extras_require,
    include_package_data=True,
    license="Proprietary",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: System :: Hardware",
    ],
    cmdclass={
        "upload": UploadCommand,
    },
)
