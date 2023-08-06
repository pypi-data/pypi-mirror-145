#!/usr/bin/env python
# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


import io
import os

import setuptools


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return io.open(file_path, encoding="utf-8").read()


version = None
lines = read("climetlab_plugin_tools/version").split("\n")
if lines:
    version = lines[0]


assert version


setuptools.setup(
    name="climetlab-plugin-tools",
    version=version,
    description="Example climetlab external dataset plugin",
    long_description=read("README.md"),
    author="European Centre for Medium-Range Weather Forecasts (ECMWF)",
    author_email="software.support@ecmwf.int",
    license="Apache License Version 2.0",
    url="https://github.com/ecmwf-lab/climetlab-plugin-tools",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["climetlab>=0.10.0"],
    zip_safe=True,
    entry_points={
        "climetlab.scripts": [
            "climetlab_plugin_tools_1 = climetlab_plugin_tools.create_plugin_cmd:CreateDatasetPluginCmd",
            "climetlab_plugin_tools_2 = climetlab_plugin_tools.create_plugin_cmd:CreateSourcePluginCmd",
        ],
        "console_scripts": [
            "climetlab-plugin-create-dataset=climetlab_plugin_tools:CreateDatasetPluginStandAlone",
            "climetlab-plugin-create-source=climetlab_plugin_tools:CreateSourcePluginStandAlone",
        ],
    },
    keywords="meteorology",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
)
