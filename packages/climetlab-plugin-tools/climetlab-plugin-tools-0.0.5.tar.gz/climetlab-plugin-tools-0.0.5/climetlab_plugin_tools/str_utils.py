# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#
import re


def Title(s):
    if not s:
        return ""
    return s[0].upper() + s[1:]


def CamelCase(k):
    """Transform to CamelCase:
    >>> CamelCase("class-name")
    'ClassName'
    >>> CamelCase("class_name")
    'ClassName'
    >>> CamelCase("Class_name_longer")
    'ClassNameLonger'
    >>> CamelCase("")
    ''
    >>> CamelCase("a")
    'A'
    """
    if not k:
        return ""
    if len(k) == 1:
        return k.upper()
    k = k.replace("-", "_")
    lst = k.split("_")
    lst = [Title(s) for s in lst]
    return "".join(lst)


def camelCase(k):
    """Transform to camelCase:
    >>> camelCase("class-name")
    'className'
    >>> camelCase("class_name")
    'className'
    >>> camelCase("Class_name_longer")
    'classNameLonger'
    >>> camelCase("")
    ''
    >>> camelCase("a")
    'a'
    """
    if not k:
        return ""
    k = CamelCase(k)
    if len(k) == 1:
        return k.lower()
    return k[0].lower() + k[1:]


def dashes(k):
    """Transform to dashes:
    >>> dashes("class-name")
    'class-name'
    >>> dashes("class_name")
    'class-name'
    >>> dashes("Class_name_longer")
    'class-name-longer'
    >>> dashes("")
    ''
    >>> dashes("a")
    'a'
    >>> dashes("A")
    'a'
    """
    return k.lower().replace("_", "-")


def underscores(k):
    return dashes(k).replace("-", "_")


def dots(k):
    return dashes(k).replace("-", ".")


def alphanum(k):
    return re.sub("[^0-9a-zA-Z\\-]+", "-", k)
