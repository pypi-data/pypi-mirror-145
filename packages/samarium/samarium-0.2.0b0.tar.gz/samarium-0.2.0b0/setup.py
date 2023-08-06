# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['samarium']

package_data = \
{'': ['*'], 'samarium': ['modules/*']}

entry_points = \
{'console_scripts': ['samarium = samarium.__main__:main',
                     'samarium-debug = samarium.__main__:main_debug']}

setup_kwargs = {
    'name': 'samarium',
    'version': '0.2.0b0',
    'description': 'A dynamic, interpreted language transpiled to Python',
    'long_description': '# Samarium\n\nSamarium is a dynamic interpreted language transpiled to Python.\nSamarium, in its most basic form, doesn\'t use any digits or letters.\n\nHere\'s a `Hello, World!` program written in Samarium:\n\n<span style="display: inline-block" align="left">\n    <img src="docs/images/00helloworld.png" width="50%">\n</span>\n\nNote: Every statement in Samarium must end in a semicolon, and backticks will be ignored.\n\nDocumentation on how to program in Samarium can be found [here](docs/tableofcontents.md).\n\n\n# Installation\n\n## [pip](https://pypi.org/project/pip/)\n\n`pip install samarium`\n\n## [AUR](https://aur.archlinux.org/)\n\n`yay -S samarium`\n\n## Using Samarium\n\nYou can run Samarium programs with `samarium program.sm`.\n`samarium-debug` may be used instead, which will first print out the intermediary Python code that the Samarium program is transpiled into, before executing it.\n\nThe `-c <command>` option can be used to execute Samarium code from the string `command`, directly in the terminal.\n`command` can be one or more statements separated by semicolons as usual.\nNote that the last statement of `command` will be printed if it does not end in a semicolon.\n\nThere is also a VSCode syntax highlighting extension for Samarium, which can be found here [here](https://marketplace.visualstudio.com/items?itemName=Samarium.samarium-language). The source code can be found [here](https://github.com/samarium-lang/vscode-samarium).\n\n\n# Credits\n\nSamarium was inspired by several languages, including [brainfuck](https://esolangs.org/wiki/Brainfuck), [Rust](https://www.rust-lang.org/), [Java](https://www.java.com/) and [Python](https://www.python.org/).\nThanks to [tetraxile](https://github.com/tetraxile) for helping with design choices and writing the docs, [MithicSpirit](https://github.com/MithicSpirit) for making Samarium an AUR package, and [DarviL82](https://github.com/DarviL82) for fixing some issues.\n\nIf you have any questions, or would like to get in touch, join the [Discord server](https://discord.gg/C8QE5tVQEq)!',
    'author': 'trag1c',
    'author_email': 'trag1cdev@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
