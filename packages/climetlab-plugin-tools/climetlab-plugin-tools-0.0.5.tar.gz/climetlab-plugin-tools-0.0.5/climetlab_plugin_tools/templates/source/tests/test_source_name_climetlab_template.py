#!/usr/bin/env python3
# licence_header_climetlab_template

import climetlab as cml


def test_source():
    ds = cml.load_source(
        "source-name-climetlab-template",
        arg1="1",
        arg2="2",
    )
    df = ds.to_pandas()
    print(df)


if __name__ == "__main__":
    test_source()
