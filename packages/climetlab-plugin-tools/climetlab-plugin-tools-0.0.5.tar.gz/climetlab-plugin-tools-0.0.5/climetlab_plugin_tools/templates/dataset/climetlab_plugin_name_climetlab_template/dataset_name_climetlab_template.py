#!/usr/bin/env python3
# license_header_climetlab_template
from __future__ import annotations

import climetlab as cml
from climetlab import Dataset
from climetlab.decorators import normalize

__version__ = "0.1.0"

URL = "https://storage.ecmwf.europeanweather.cloud"

PATTERN = (
    "{url}/climetlab/test-data/0.5/fixtures/"
    "plugin_create_dataset_example_{year}_{parameter}.grib"
)


class DatasetNameClimetlabTemplate(Dataset):
    name = None
    home_page = "-"
    # The licence is the licence of the data (not the licence of the plugin)
    licence = "-"
    documentation = "-"
    citation = "-"

    # These are the terms of use of the data (not the licence of the plugin)
    terms_of_use = (
        "By downloading data from this dataset, "
        "you agree to the terms and conditions defined at "
        "https://github.com/github_username_climetlab_template/"
        "climetlab-plugin-name-climetlab-template/"
        "blob/main/LICENSE. "
        "If you do not agree with such terms, do not download the data. "
    )

    dataset = None

    @normalize("parameter", ["tp", "t2m"])
    def __init__(self, year, parameter):
        request = dict(parameter=parameter, url=URL, year=year)
        self.source = cml.load_source("url-pattern", PATTERN, request)
