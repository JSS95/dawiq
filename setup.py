from itertools import chain
import os
from setuptools import setup, find_packages  # type: ignore[import]


VERSION_FILE = "dawiq/version.py"


def get_version():
    with open(VERSION_FILE, "r") as f:
        exec(compile(f.read(), VERSION_FILE, "exec"))
    return locals()["__version__"]


def read_readme():
    with open("README.md", encoding="utf-8") as f:
        content = f.read()
    return content


def get_package_data():
    pkgname = "dawiq"
    pkg_datapaths = [
        "py.typed",
    ]

    ret = []
    for path in pkg_datapaths:
        fullpath = os.path.join(pkgname, path)
        if os.path.isfile(fullpath):
            ret.append(path)
        else:
            for root, dirs, files in os.walk(fullpath):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    ret.append(os.path.join(*filepath.split(os.sep)[1:]))

    return {pkgname: ret}


def read_requirements(path):
    with open(path, "r") as f:
        ret = f.read().splitlines()
    return ret


def get_extras_require():
    ret = {}
    ret["test"] = read_requirements("requirements/test.txt")
    ret["test-ci"] = read_requirements("requirements/test.txt") + read_requirements(
        "requirements/test-ci.txt"
    )
    ret["doc"] = read_requirements("requirements/doc.txt")
    ret["full"] = list(set(chain(*ret.values())))
    return ret


setup(
    name="dawiq",
    version=get_version(),
    python_requires=">=3.9",
    description="Package to construct Qt widgets from dataclasses",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        (
            "License :: OSI Approved :: "
            "GNU Library or Lesser General Public License (LGPL)"
        ),
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Widget Sets",
    ],
    author="Jisoo Song",
    author_email="jeesoo9595@snu.ac.kr",
    maintainer="Jisoo Song",
    maintainer_email="jeesoo9595@snu.ac.kr",
    url="https://github.com/JSS95/dawiq",
    license="LGPL",
    packages=find_packages(),
    package_data=get_package_data(),
    install_requires=read_requirements("requirements/install.txt"),
    extras_require=get_extras_require(),
)
