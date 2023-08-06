# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import configparser
import datetime
import logging
import os
import pathlib

from climetlab.scripts.tools import parse_args

from .str_utils import CamelCase, alphanum, camelCase, dashes, underscores

LOG = logging.getLogger(__name__)
# import climetlab.debug


APACHE_LICENCE = """This software is licensed under the terms of the Apache Licence Version 2.0
which can be obtained at http://www.apache.org/licenses/LICENSE-2.0."""

PREFIX_ECMWF_LICENCE = (
    """(C) Copyright {year} European Centre for Medium-Range Weather Forecasts."""
)

POSTFIX_ECMWF_LICENCE = """In applying this licence, ECMWF does not waive the privileges and immunities
granted to it by virtue of its status as an intergovernmental organisation
nor does it submit to any jurisdiction."""


class PluginContext:
    def __init__(self, kind, **kwargs):
        self.kind = kind
        self._transformers = {}
        self.kwargs = kwargs

    def fill_form(self):
        for t in TRANSFORMERS_CLASSES[self.kind]:
            t(self)

    @property
    def template_dir(self):
        here = os.path.dirname(__file__)
        return os.path.realpath(os.path.join(here, "templates", self.kind))

    @property
    def output_dir(self):
        return self("climetlab-plugin-name-climetlab-template")

    def check_output_dir(self):
        if os.path.exists(self.output_dir):
            raise Exception(
                f"Folder {self.output_dir} already exists. Not overwriting it."
            )

    def create_plugin(self):
        self.check_output_dir()
        for path in self.template_files_list():
            template = os.path.join(self.template_dir, path)
            output = os.path.join(self.output_dir, path)
            output = self(output)
            LOG.info(f"Creating {output}")
            with open(template, "r") as f:
                txt = f.read()
            txt = self(txt)
            os.makedirs(os.path.dirname(output), exist_ok=True)
            with open(output, "w") as f:
                f.write(txt)
        print(f"Plugin built in {self.output_dir}")
        print(self.final_help())

    def template_files_list(self):
        cwd = os.getcwd()
        os.chdir(self.template_dir)
        lst = [str(f) for f in pathlib.Path(".").glob("**/*") if os.path.isfile(str(f))]
        # TODO: find a nicer way to avoid __path__ folders.
        lst = [f for f in lst if "__pycache__" not in f]
        os.chdir(cwd)
        return lst

    def __call__(self, txt):
        if txt is None:
            return None
        assert isinstance(txt, str), txt
        original = txt
        for k, transformer in self._transformers.items():
            txt = transformer(txt)
        if txt != original:
            txt = self(txt)
        return txt

    def get_default_email(self):
        try:
            return self._gitconfig("email")
        except:  # noqa:E722
            return f'{self._transformers["full_name"].value.replace(" ", ".").lower()}@example.com'

    def get_default_full_name(self):
        try:
            return self._gitconfig("name")
        except:  # noqa:E722
            return "Joe Developer"

    def _gitconfig(self, key):
        if os.environ.get("CLIMETLAB_PLUGIN_TOOLS_NO_GUESS"):
            raise Exception("CLIMETLAB_PLUGIN_TOOLS_NO_GUESS is set.")
        config = configparser.ConfigParser()
        gitconfig = os.path.expanduser("~/.gitconfig")
        config.read(gitconfig)
        value = config["user"][key]
        LOG.info(f"Found {key} in gitconfig {value}")
        return value

    def final_help(self):
        txt = """
--------------------------------------------------------------------
Climetlab plugin generated successfully. Next steps:
  1. Create a repository on github at http://github.com/repo_url_climetlab_template.

  2. Push to the repository as instructed by github:
    cd climetlab-plugin-name-climetlab-template
    git init
    git add .
    git commit -m'first commit'
    git branch -M main
    git remote add origin http://github.com/repo_url_climetlab_template
    git push --set-upstream origin main

  [Optional: See tests running http://github.com/repo_url_climetlab_template/actions]

  3 - Publish to pipy (pip) manually:
      python -m pip install --upgrade pip
      pip install setuptools wheel twine
      twine upload dist/*
      # Need pipy login/password (create an account at https://pypi.org)

  Others can now do `pip install climetlab-plugin-name-climetlab-template`.

  4. Publish automatically from Github to pypi. [Optional]
     Edit climetlab-plugin-name-climetlab-template/.github/workflows/check-and-publish to point to pypi instead of test.pypi.
     Create a token from pypi at https://pypi.org/manage/account/token/
     Add the token as a Gihtub secret on the name PYPI_API_TOKEN at https://github.com/repo_url_climetlab_template/settings/secrets/actions/new

  You are all set! Push the github repository and release from http://github.com/repo_url_climetlab_template/releases/new.
"""  # noqa: E501
        return self(txt)


class Transformer:
    _help = ""
    glob = None

    def __init__(
        self,
        context,
        key,
        default=None,
        pattern=None,
        value=None,
        force_prefix="",
    ):
        LOG.debug(f"New Transformer({key})")

        self._context = context
        self.key = key

        self.default = self._context(default)
        self.force_prefix = self._context(force_prefix)
        self.pattern = pattern
        self.value = value
        self.help = self._context(self._help)

        self.fill()
        LOG.debug(f"Transformer({key}) created")

    def __repr__(self) -> str:
        return f"Transformer({self.key}, pattern={self.pattern}, value={self.value})"

    def fill(self):
        if self.pattern is None:
            self.pattern = self.key

        if not self.glob:
            self.adapts = [lambda x: x]
        elif self.glob is True:
            self.adapts = [underscores, dashes, CamelCase, camelCase]
        else:
            self.adapts = self.glob

        self.read_value()

        self.pattern = self.pattern + "_climetlab_template"
        self._context._transformers[self.key] = self

    def prompt(self):
        return f"Please enter {self.desc} ('?' for help)"

    def default_prompt(self):
        if self.default:
            return f"Hit 'return' to use the default value '{self.force_prefix}{self.default}'"
        return ""

    def try_reading_from_context(self):
        if self._context.kwargs.get(self.key, None):
            self.value = self._context.kwargs[self.key]
            assert isinstance(self.value, str)
            assert isinstance(self.force_prefix, str)
            print(f"\n--> Using {self.force_prefix + self.value} (from command line)")
            return True

    def try_reading_from_user(self):
        print()
        value = input(">>>> " + self.force_prefix)
        if value == "h" or value == "?":
            print(f"?\n  {self.help}")
            if self.default is not None:
                print(f"  Default value: {self.force_prefix}{self.default}")
            return self.try_reading_from_user()
        if value:
            self.value = value
            print(f"\n--> Using {self.force_prefix + self.value}")
            return True

    def try_reading_from_default(self):
        if self.default is not None:
            print(f"\n--> Using {self.force_prefix + self.default} (default)")
            self.value = self.default
            return True

    def read_value(self):
        print()
        print(self.prompt())
        print(self.default_prompt())
        if self.try_reading_from_context():
            return
        if self.try_reading_from_user():
            return
        if self.try_reading_from_default():
            return
        return self.read_value()

    def __call__(self, txt):
        for adapt in self.adapts:
            p = adapt(self.pattern)
            v = adapt(self.value)
            if p in txt:
                LOG.debug(f'Replacing "{p}" by "{v}"')
                LOG.debug(f"  k={self.key}")
                LOG.debug(f"  p: {self.pattern} -> {p}")
                LOG.debug(f"  v: {self.value} -> {v}")
            txt = txt.replace(p, v)
        return txt


class NoPromptTransformer(Transformer):
    def read_value(self):
        LOG.debug(f"{self.key}: not prompt using {self.value}.")


class GlobNoPromptTransformer(NoPromptTransformer):
    glob = True


class SourceNameTransformer(GlobNoPromptTransformer):
    def __init__(self, context):
        name = context._transformers["plugin_name"].value
        if name.endswith("-source"):
            name = name[:-7]
        super().__init__(context, "source_name", value=name)


class DatasetNameTransformer(Transformer):
    desc = "the dataset name"
    _help = """The dataset name is used as follow:
  A climetlab dataset plugin package can provides one or more
  datasets. This scripts creates a plugin with one dataset.
  The dataset name will be used by the end users to access
  the data through CliMetLab with:
  cml.load_dataset("dataset-name", ...)
  The convention is to make the dataset name start with
  "plugin-name-climetlab-template".
  The dataset name can easily be modified afterwards, without
  regenerating a new plugin, simply by editing the setup.py."""
    glob = True

    def __init__(self, context):
        super().__init__(
            context,
            "dataset_name",
            default="",
            force_prefix="plugin-name-climetlab-template",
        )

    def fill(self):
        super().fill()
        self.value = dashes(self.value).lower()
        self.value = alphanum(self.value)
        if self.value:
            while self.value.startswith("-"):
                self.value = self.value[1:]
            name = "plugin-name-climetlab-template" + "-" + self.value
        else:
            self.value = "main"
            name = "plugin-name-climetlab-template"
        name = self._context(name)
        GlobNoPromptTransformer(self._context, "dataset_full_name", value=name)


class PluginNameTransformer(Transformer):
    desc = "the plugin name"
    _help = """The plugin name is used to define:
     - The python package name `import climetlab_{plugin_name} `
     - The pip package name `pip install climetlab-{plugin-name}`.
  It will also be used to suggest and appropriate URL on github.
  The plugin_name can be the name of the project you are working on,
  but notice that it should be specific enough as only one plugin with
  a given name can be installed. Highly generic names (such as "meteo",
  "domain", "copernicus", "country-name" are not recommended.
  The plugin name cannot be easily modified afterwards.
  You would need to regenerate a new one and copy existing code."""
    glob = True

    def __init__(self, context):
        super().__init__(
            context,
            "plugin_name",
            default="my_plugin",
        )
        context.check_output_dir()


class EmailTransformer(Transformer):
    desc = "your email"
    _help = """The email is used in setup.py to define the email maintainer of the pip package."""

    def __init__(self, context):
        super().__init__(
            context,
            "email",
            default=context.get_default_email(),
        )


class GithubUsernameTransformer(Transformer):
    desc = "your Github user name"
    _help = """The github username (or github space name) is used
  to suggest a github repository url.
  The username (ecmwf-lab) should be used if you wish to host your
  repository on the github space "https://github.com/ecmwf-lab/").
  Else, please provide your own github user name."""

    def __init__(self, context):
        super().__init__(
            context,
            "github_username",
            default="ecmwf-lab",
        )


class FullNameTransformer(Transformer):
    desc = "your full name"
    _help = """The full name is used in setup.py to define the maintainer of the pip package."""

    def __init__(self, context):
        super().__init__(
            context,
            "full_name",
            default=context.get_default_full_name(),
        )


class RepoUrlTransformer(Transformer):
    desc = "the repository url"
    _help = """The repository url name is used to define:
      - The package url in the setup.py, i.e. the url published in Pypi for pip.
      - The links in the README file.
  If your do not want to host you repository on github,
  please edit manually the generated setup.py afterwards."""

    def __init__(self, context):
        super().__init__(
            context,
            "repo_url",
            default="github_username_climetlab_template/climetlab-plugin-name-climetlab-template",
            force_prefix="https://github.com/",
        )


class LicenceTransformer(Transformer):
    _help = """The APACHE 2.0 licence is used for the plugin code.
  Most users should answer "n" to use the standard APACHE 2.0 licence.
  ECMWF users should answer "y" to add the appropriate addition to the licence.
  The licence is added in the plugin code:
      - In the header of each python file.
      - In the LICENSE file.
      - In the README.
  If you choose another licence, please modify these files manually afterwards."""
    desc = "Use the modified APACHE licence with ECMWF additions?"

    def __init__(self, context):
        super().__init__(context, "licence")

    def prompt(self):
        return f"{self.desc} ('y' or 'n', '?' for help)"

    def fill(self):
        self.read_value()
        self.value = dict(y=True, n=False)[self.value.lower()]

        self.year = str(datetime.datetime.now().year)
        licence = APACHE_LICENCE
        if self.value:
            licence = "\n".join([PREFIX_ECMWF_LICENCE, licence, POSTFIX_ECMWF_LICENCE])
        licence = licence.format(year=self.year)

        print(f"   Using this licence:\n{licence}\n")

        NoPromptTransformer(self._context, "year_licence", value=str(self.year))

        NoPromptTransformer(self._context, "licence_txt", value=licence)
        NoPromptTransformer(self._context, "license_txt", value=licence)

        licence_with_sharp = "\n".join(["# " + line for line in licence.split("\n")])
        NoPromptTransformer(
            self._context,
            "licence_header",
            pattern="# licence_header",
            value=licence_with_sharp,
        )
        NoPromptTransformer(
            self._context,
            "license_header",
            pattern="# license_header",
            value=licence_with_sharp,
        )


TRANSFORMERS_CLASSES = {
    "dataset": [
        PluginNameTransformer,
        DatasetNameTransformer,
        FullNameTransformer,
        EmailTransformer,
        GithubUsernameTransformer,
        RepoUrlTransformer,
        LicenceTransformer,
    ],
    "source": [
        PluginNameTransformer,
        SourceNameTransformer,
        FullNameTransformer,
        EmailTransformer,
        GithubUsernameTransformer,
        RepoUrlTransformer,
        LicenceTransformer,
    ],
}


class CreateDatasetPluginCmd:
    @parse_args(
        name=dict(help="Plugin name"),
        dataset=dict(help="Dataset name"),
    )
    def do_plugin_create_dataset(self, args):
        context = PluginContext(
            "dataset", plugin_name=args.name, dataset_name=args.dataset
        )
        context.fill_form()
        context.create_plugin()


class CreateSourcePluginCmd:
    @parse_args(name=dict(help="Plugin name"))
    def do_plugin_create_source(self, args):
        context = PluginContext("source", plugin_name=args.name)
        context.fill_form()
        context.create_plugin()
