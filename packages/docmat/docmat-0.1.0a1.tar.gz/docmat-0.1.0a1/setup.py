# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docmat', 'docmat.docstring_formats.google', 'docmat.docstring_formats.shared']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['docmat = docmat.__main__:main']}

setup_kwargs = {
    'name': 'docmat',
    'version': '0.1.0a1',
    'description': 'Python docstring formatter',
    'long_description': '<!-- omit in TOC -->\n# docmat\n\nPython docstring formatter.\n\n- [Main Functionalities](#main-functionalities)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Supported docstring formats](#supported-docstring-formats)\n- [Examples](#examples)\n- [Integration with VSCode](#integration-with-vscode)\n- [Roadmap](#roadmap)\n\n## Main Functionalities\n\n- Adjusts indentation and spacing.\n- Wraps all docstring text.\n\n## Installation\n\n```bash\npip install docmat\n```\n\n## Usage\n\nIn order to format the docstring of a file, run in a terminal shell:\n\n```bash\ndocmat <filename>|<folder>|<glob>\n```\n\nExamples:\n\n```bash\ndocmat to_format.py\n```\n\n```bash\ndocmat to_format.py other_file_to_format.py\n```\n\n```bash\ndocmat to_format.py --line-length 79\n```\n\n```bash\ndocmat directory\n```\n\n```bash\ndocmat directory/*\n```\n\n## Supported docstring formats\n\n- Google\n\nAdding support for other docstring formats is in the Roadmap.\n\n## Examples\n\nBefore:\n\n```python\ndef func():\n    """\n    This fits in one line.\n    """\n```\n\nAfter:\n\n```python\ndef func():\n    """This fits in one line."""\n```\n\n---\nBefore:\n\n```python\ndef func():\n    """start with lower letter, dot missing"""\n```\n\nAfter:\n\n```python\ndef func():\n    """Start with lower letter, dot missing."""\n```\n\n---\nBefore:\n\n```python\ndef func():\n    """\n    In this docstring a newline after the summary is missing.\n    Summary and description should be separated by a newline.\n    """\n```\n\nAfter:\n\n```python\ndef func():\n    """\n    In this docstring a newline after the summary is missing.\n\n    Summary and description should be separated by a newline.\n    """\n```\n\n---\nBefore:\n\n```python\ndef func():\n    """\n    Summary.\n\n    The length of the function description in this specific function exceeds the maximum line length, that in this case is left to the default value `88`. This block of text should be wrapped.\n    """\n```\n\nAfter:\n\n```python\ndef func():\n    """Summary.\n\n    The length of the function description in this specific function exceeds the maximum\n    line length, that in this case is left to the default value `88`. This block of text\n    should be wrapped.\n    """\n```\n\n---\nAdding the parameter `--wrap-summary`\n\nBefore:\n\n```python\ndef func():\n    """By default, the summary line is not wrapped even if it exceeds the maximum line length.\n\n    This behavior can be overriden by adding the `--wrap-summary` command line parameter\n    """\n```\n\nAfter:\n\n```python\ndef func():\n    """By default, the summary line is not wrapped even if it exceeds the maximum line\n    length.\n\n    This behavior can be overriden by adding the `--wrap-summary` command line\n    parameter.\n    """\n```\n\n---\nBefore:\n\n```python\ndef func(arg1, arg2):\n    """Summary.\n\n    args:\n    arg1(type): The indentation level of this argument is not correct.\n    arg2(type): In this case, the description of this argument exceeds the maximum line length and it needs to be wrapped.\n    """\n```\n\nAfter:\n\n```python\ndef func(arg1, arg2):\n    """Summary.\n\n    Args:\n        arg1(type): The indentation level of this argument is not correct.\n        arg2(type): In this case, the description of this argument exceeds the maximum\n            line length and it needs to be wrapped.\n    """\n```\n\n## Integration with VSCode\n\n`docmat` will be integrated with `VSCode` using a dedicated extension (see also [roadmap](#roadmap)).\n\nIn the meantime, `docmat` can be used from `VSCode` with a keyboard shortcut. Here are the steps to make it work:\n\n1. Install `docmat` in the python environment used by VSCode following the [installation steps](#installation)\n2. Open the Keyboard Shortcuts configuration file in VSCode `Preferences > Keyboard Shortcuts > Open Keyboard Shortcuts (JSON) [icon in the top-right]` this will open the `keybindings.json` file containing the keyboard shortcuts.\n3. Associate the docmat command to a key-binding by adding the following entry to the keybindings list:\n\n    ```json\n    [\n        {\n            "key": "shift+alt+d",\n            "command": "workbench.action.terminal.sendSequence",\n            "args": {\n                "text": "docmat \'${file}\'\\u000D"\n            }\n        }\n    ]\n    ```\n\n    The suggested key-binding is `shift`+`alt`+`D`, but you can change it to whatever you like.\n\n4. Save the file.\n\nNow, every time you are working on a python file you can hit `shift`+`alt`+`D` and the `docmat` command will be executed in the VSCode terminal on the file that you have currently opened. Eventual errors or log messages will be shown there. Please note that the environment where `docmat` is installed should be active in the VSCode integrated terminal prior to using the shortcut.\n\n## Roadmap\n\n- Add support for a no-format comment token.\n- Add support for bullet lists.\n- Add support for other docstring formats:\n  - Numpydoc\n  - reST\n  - Epytext\n- Integrate with pre-commit.\n- Create VSCode extension.\n- Add support for code examples in docstring.\n',
    'author': 'Claudio Salvatore Arcidiacono',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
