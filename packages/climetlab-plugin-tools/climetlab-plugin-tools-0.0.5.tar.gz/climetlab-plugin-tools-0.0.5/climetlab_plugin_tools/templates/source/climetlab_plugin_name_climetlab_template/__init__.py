#!/usr/bin/env python3
# license_header_climetlab_template
import os

import pandas as pd
from climetlab import Source


def get_version():
    version_file = os.path.join(os.path.dirname(__file__), "version")
    with open(version_file, "r") as f:
        version = f.readlines()
        version = version[0]
        version = version.strip()
    return version


__version__ = get_version()


class SourceNameClimetlabTemplate(Source):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def to_pandas(self, **kwargs):
        options = {}
        options.update(self.kwargs)
        options.update(kwargs)

        # TODO: implement the code to get data
        # from the new source of data
        data = [["a", "b", "c"], ["AA", "BB", "CC"]]

        df = pd.DataFrame(
            data,
            columns=["col_A", "col_B", "col_C"],
        )
        return df
