# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vyxal']

package_data = \
{'': ['*']}

install_requires = \
['num2words>=0.5.10,<0.6.0', 'sympy>=1.9,<2.0']

entry_points = \
{'console_scripts': ['vyxal = vyxal.main:cli']}

setup_kwargs = {
    'name': 'vyxal',
    'version': '2.10.1',
    'description': 'A golfing language that has aspects of traditional programming languages.',
    'long_description': '# Vyxal\n\n![Vyxal Logo](./documents/logo/vylogo.png)\n\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Vyxal/Vyxal.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Vyxal/Vyxal/context:python) ![Test status](https://github.com/Vyxal/Vyxal/actions/workflows/run-tests.yaml/badge.svg)\n\n**Vyxal** is a golfing language that takes the idea that conciseness comes at the cost of practicality and throws it out the window. That\'s right - where other golflangs throw you into the deep-end of keyboard mashing, Vyxal eases you into the concept of elegantly crafting built-ins into a functioning program.\n\nAnd yes, this design goal really _does_ warrant adding another golfing language into the already densely populated mix of golflangs. If you go and take a look at the current state of the art of golfing languages, you\'ll find that 99% of languages are either a) powerful and concise, but not easy to pick up or b) easy to learn, but not that useful for anything non-trivial (I say this as someone who\'s made and contributed to both kinds of languages). Vyxal aims to bridge the gap between simplicity and "golfability".\n\n## Fun Vyxal Features\n\n- Comments!\n\n```\n1 1+ # This is a comment\n     # This is a comment too, but it\'s longer\n     # Btw the expression evaluates to 2\n```\n\n[Try it Online!](https://vyxal.pythonanywhere.com/#WyIiLCIiLCIxIDErICMgVGhpcyBpcyBhIGNvbW1lbnRcbiAgICAgIyBUaGlzIGlzIGEgY29tbWVudCB0b28sIGJ1dCBpdCdzIGxvbmdlclxuICAgICAjIEJ0dyB0aGUgZXhwcmVzc2lvbiBldmFsdWF0ZXMgdG8gMiIsIiIsIiJd)\n\n- Variables!\n\n```\n`Joe` →first_name # The variable "first_name" now has the value "Joe"\n69 →age # The variable "age" now has the value 69 (nice)\n←first_name ` is ` ←age ` years old` +++ # "Joe is 69 years old"\n```\n\n[Try it Online!](https://vyxal.pythonanywhere.com/#WyIiLCIiLCJgSm9lYCDihpJmaXJzdF9uYW1lICMgVGhlIHZhcmlhYmxlIFwiZmlyc3RfbmFtZVwiIG5vdyBoYXMgdGhlIHZhbHVlIFwiSm9lXCJcbjY5IOKGkmFnZSAjIFRoZSB2YXJpYWJsZSBcImFnZVwiIG5vdyBoYXMgdGhlIHZhbHVlIDY5IChuaWNlKVxu4oaQZmlyc3RfbmFtZSBgIGlzIGAg4oaQYWdlIGAgeWVhcnMgb2xkYCArKysgIyBcIkpvZSBpcyA2OSB5ZWFycyBvbGRcIiIsIiIsIiJd)\n\n- Named Functions!\n\n```\n@fibonacii:N|                # def fibonacii(N):\n  ←N 0 = [ 0 |               #   if N == 0: return 0\n    ←N 1 = [ 1 |             #   elif N == 1: return 1\n      ←N 2 - @fibonacii;     #   else: return fibonacii(N - 2) + fibonacii(N - 1)\n      ←N 1 - @fibonacii; +\n    ]\n  ]\n;\n\n6 @fibonacii;\n```\n\n[Try it Online!](https://vyxal.pythonanywhere.com/#WyIiLCIiLCJAZmlib25hY2lpOk58ICAgICAgICAgICAgICAgICMgZGVmIGZpYm9uYWNpaShOKTpcbiAg4oaQTiAwID0gWyAwIHwgICAgICAgICAgICAgICAjICAgaWYgTiA9PSAwOiByZXR1cm4gMFxuICAgIOKGkE4gMSA9IFsgMSB8ICAgICAgICAgICAgICMgICBlbGlmIE4gPT0gMTogcmV0dXJuIDFcbiAgICAgIOKGkE4gMiAtIEBmaWJvbmFjaWk7ICAgICAjICAgZWxzZTogcmV0dXJuIGZpYm9uYWNpaShOIC0gMikgKyBmaWJvbmFjaWkoTiAtIDEpXG4gICAgICDihpBOIDEgLSBAZmlib25hY2lpOyArXG4gICAgXVxuICBdXG47XG5cbjYgQGZpYm9uYWNpaTsiLCIiLCIiXQ==)\n\n- And Nice Syntax Choices!\n\nIn conclusion, if you\'re coming from a traditional programming language, Vyxal is the right golfing language for you - you\'ll appreciate the familiar control structures! If you\'re coming from another golfing language, Vyxal is also the right golfing language for you - you\'ll be able to jump right into complex problem solving!\n\n_(Btw we also have cookies - the tasty kind, not the track your info kind)_\n\n## Installation\n\nYou can also use the [online interpreter](https://vyxal.pythonanywhere.com) with no need to install!\n\nIf you only want to run Vyxal, all you need to run is this:\n\n```\npip install vyxal\n```\n\nIf you are working on Vyxal, install [Poetry](https://python-poetry.org), and then you can clone this repo and run:\n\n```\npoetry install\n```\n\n## Usage\n\nTo run using the script:\n\n```\nvyxal <file> <flags (single string of flags)> <input(s)>\n```\n\nIf you\'re using Poetry:\n\n```\npoetry run vyxal <file> <flags (single string of flags)> <input(s)>\n```\n\n## Links\n\n- [Repository](https://github.com/Vyxal/Vyxal)\n- [Online Interpreter](http://vyxal.pythonanywhere.com)\n<!-- TODO: fix broken links\n- [Tutorial](https://github.com/Vyxal/Vyxal/blob/master/docs/Tutorial.md)\n- [Codepage](https://github.com/Vyxal/Vyxal/blob/master/docs/codepage.txt)\n  -->\n- [Main Chat Room (SE Chat)](https://chat.stackexchange.com/rooms/106764/vyxal)\n- [Vycord (Discord)](https://discord.gg/hER4Avd6fz)\n- [Elements](https://github.com/Vyxal/Vyxal/blob/v2.6.0/documents/knowledge/elements.md)\n- [Vyxapedia](https://vyxapedia.hyper-neutrino.xyz/)\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://vyxal.pythonanywhere.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
