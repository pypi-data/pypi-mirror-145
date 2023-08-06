# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlean']

package_data = \
{'': ['*'], 'sqlean': ['grammar/*']}

install_requires = \
['black>=21.4b',
 'lark>=1.1.0',
 'pydantic>=1.8.2',
 'rich>=10.0',
 'tomli>=1.0.0',
 'typer>=0.4.0']

entry_points = \
{'console_scripts': ['sqlean = sqlean.main:app']}

setup_kwargs = {
    'name': 'sqlean',
    'version': '0.0.2',
    'description': 'Clean your SQL queries',
    'long_description': '## Why\n\n* rise of SQL\n* dbt\n* formatter like black to reduce arguments. In return for consistency, sometimes\n  it\'s less readable\n\n\n## Contributing\n\n`sqlean` will need a community effort to be capable of parsing all valid SQL\nqueries. We\'ve setup the testing to make it easier to add to the grammar so that\nmore and more elements of valid SQL can be parsed.\n\n## Installing\n\n## Usage\n\n### Configuration\n\n### Snapshot tests\n\n\n#### Snapshot files\n\nEach snapshot file is divided into 3 parts, with each part separated by a line\nwith three dashes:\n\n```text\n---\n```\n\nThe first part is minimal working example (MWE) for the SQL query. This is the\nonly part that needs to be human-written.\n\n#### Conventions\n\nThe snapshots are located in the `sqlean/tests/snapshots` directory, under\ndifferent sub-directories. The sub-directories are grouped by grammar elements.\nWithin each sub-directory, the files are prefixed by a three digit integer...\n\nThe snapshot files have extension `.snapshot`. You can set up your editor to\nrecognise the `.snapshot` file as an `R` file so that you get syntax\nhighlighting of the parse tree.\n\n### Adding to the parser\n\nIf you run `sqlean` on a file that you contains a valid SQL/dbt query but\n`sqlean` marks it as "unparsable", this indicates that there is an element of\nyour file that is not in `sqlean`\'s grammar. You can contribute to the grammar\nso that the element and the file can be parsed and styled.\n\n1. TODO: there should be an easy command line way to figure out what element\n   cannot be parsed.\n1. Once the unparsable element has been identified, write a minimal working\n   example (MWE) of an SQL query that contains the element.\n1. Identify the sub-directory in the `sqlean/tests/snapshots` directory where\n   the element should go, or if there needs to be a new sub-directory.\n1. Within the sub-directories, create a new file named according to the\n   [conventions](#conventions) and put your MWE in the file.\n1. Run the snapshot test for this file:\n\n   ```bash\n   make snapshot L=tests/snapshots/{sub_dir}/{new_file}\n   ```\n\n   This will fail with an error printed in the snapshot file which can guide\n   you on modifying the grammar so that the file can be parsed.\n\n   If there are a number of different new files, you can use the `M` (match)\n   argument instead of the `L` (location) argument to match a string within the\n   file names. For example,\n\n   ```bash\n   make snapshot M=dbt\n   ```\n\n    will run the snapshot tests on all snapshot files that contain "dbt" in the\n    file name.\n1. As you modify the grammar in the `.lark` file, you can check the output of\n   the parser by running the snapshot test and checking what is printed in the\n   third section of the snapshot file. Errors will appear in the third section\n   if there is a problem with the grammar.\n1. Once you\'re happy with the parse tree, you can move on to styling the output.\n   Similar to the grammar, as you modify the styling, you can check the output\n   of the styler by running the same snapshot test and checking what is printed\n   in the second section of the snapshot file. Errors will appear in the second\n   section if there is a problem with the styler.\n1. Once you\'re happy with the styling, you should run the tests on all existing\n   snapshot files with:\n\n   ```bash\n   make snapshot\n   ```\n\n   If your parsing or styling changed other files, it will show up here. These\n   file changes will show up in git so it will be easy to see for the author\n   and in code review whether the change was intentional or not.\n\n\n\n\n### Design principles\n\nThe identity of a tree should be sufficient to know how to inspect the children.\nFor example, suppose there were a `bool_operation` rule/tree that could be both\na binary or unary operation. This would break this principle since you wouldn\'t\nknow if the boolean operator is the 0th child (eg `NOT`) or the 1st child (eg\n`AND` or `OR`).\n\nAll children of a tree should have the same indentation level.\n\nAs much as possible, parsing should follow BQ syntax. However, the BQ docs do\nnot provide a complete grammar.\n\nYou should be able to determine from a node itself what the indentation level\nshould be. In other words, you shouldn\'t need to look to the parent. This means\nthat anything that should be printed in full on it\'s own line needs to be a tree\nand not a token.\n\n#### CLI options vs configuration file\n\nCLI options are for options that can change from one run of `sqlean` to another.\nProject level configuration will not change from one run to another, and must be\nset in `pyproject.toml`.\n[`pyproject.toml`](https://snarky.ca/what-the-heck-is-pyproject-toml/) is\nbecoming the standard configuration for Python tooling, and no other\nconfiguration files will be accepted by `sqlean`.\n\nThe `target` directory or file can be both a project level setting and also change\nfrom one run to another, so it can appear in both `pyproject.toml` or as a CLI\nargument. If it is in `pyproject.toml` and it is supplied as a CLI argument, then\nCLI argument will be used. If it applies in neither, then the current directory\nis used as a default.\n\n### Constraints\n\n* Transformers are leaf to root, so cannot determine indent levels\n* Visitors are leaf to root by default, but can be run root to leaf (visit_topdown)\n',
    'author': 'Oliver Chen',
    'author_email': 'oliverxchen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oliverxchen/sqlean',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
