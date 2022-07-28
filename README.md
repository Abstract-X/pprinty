# pprinty

[![PyPI version](https://badge.fury.io/py/pprinty.svg)](https://badge.fury.io/py/pprinty)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org)
[![GitHub license](https://img.shields.io/github/license/Abstract-X/pprinty)](https://github.com/Abstract-X/pprinty/blob/main/LICENSE)

`pprinty` is a Python package for beautiful printing of objects. 

---

### Installation

```commandline
pip install pprinty
```

---

### Usage
```python3
>>> from pprinty import pprint
>>>
>>> pprint({"a": {"d": "e"}, "b": "f", "c": ["I read the letter.", "Stood up.", "Sat down.", "Pondered for a minute."]})
{
    'a': {
        'd': 'e'
    },
    'b': 'f',
    'c': [
        'I read the letter.',
        'Stood up.',
        'Sat down.',
        'Pondered for a minute.'
    ]
}
```
