# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['immute']
setup_kwargs = {
    'name': 'immute',
    'version': '0.3.3',
    'description': 'Create immutable python classes',
    'long_description': '# Immute\n\nCreate "immutable" classes in python.\n\nI created a simple python object that, when inherited in another class, will prevent assignment operations outside the `__init__()` or `__new__()` methods.\n\n**Note: DOES NOT CREATE TRUELY IMMUTABLE REFERENCES.**\n\nClasses inheriting from `Immutable` are not immutable references, only immutable from assignments, reassignment and deletion operations.\n\nClasses inheriting from `Immutable` are still mutable reference types, and not truly immutable like python\'s built-in types (int, float, bool, str, tuples).\n\n## Example\n\n```python\nfrom immute import Immutable\n\nclass Singleton(Immutable):\n    _instance = None # Class fields allowed during class definition\n\n    # __new__() and __init__() methods are allowed to modify class state.\n    # After instantiation, setattr and delattr are effectively \'\'disabled\'\n    def __new__(cls, *args, **kwargs) -> Singleton:\n        if cls._instance is None:\n            cls._instance = super().__new__(cls, *args, **kwargs)\n        return cls._instance\n\n    def __init__(self) -> None:\n        self.num = 42\n        self.title = "My Super Cool App!"\n\nconfig = Singleton()\nprint(config.title)\n\nconfig.num = 21\n\n# ^^^^^^ This will raise a TypeError exception\n#\n# Attempting to assign class level attributes will throw an error\nSingleton.name = "thing 1"\n# ^^^^^^^^ This will raise a TypeError exception\n```\n\n## To Install\n\nTo install this package, enter on of the following\n\n`pip install immute`\n\nor\n\n`poetry add immute`\n',
    'author': 'fitzypop',
    'author_email': 'fitzypop@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fitzypop/immute',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
