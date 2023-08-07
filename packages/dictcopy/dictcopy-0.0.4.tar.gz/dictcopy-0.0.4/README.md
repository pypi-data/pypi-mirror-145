# dict-copy

Extension methods for copying dictionaries

## Installation

Use pip to install the package:

```bash
pip install dict-copy
```

## Usage

This package provides some functions to copy a dict


### Simple clone

```python
from dictcopy import dictcopy


obj = {
    "name": "Jeff",
    "lastname": "Aguilar",
    "age": 28,
    "email": "jeff.aguilar.06@gmail.com"
}

obj1 = dictcopy.clone(obj)
```

### Copy some values

If you want to clone the dictionary, but only with some values, you can specify them.

```python
obj1 = dictcopy.clone(obj, {
    "name",
    "lastname",
    "email"
})
```

### Strict mode

By default, when you specify fields that do not exist in the source dictionary, they will simply be skipped.

But, you could change this behavior by changing the `strict_mode` property to True. You will get a `KeyError`


```python
obj1 = dictcopy.clone(obj, {
    "name",
    "lastname",
    "email",
    "ocupation"
}, strict_mode=True)
```


### Extract values

If you want to remove some values, extract might help. will return a new dictionary with the fields removed from the source dictionary

```python
obj1 = dictcopy.extract(obj, {
    "age",
    "email"
})
```

You can also apply strict mode to validate that each field exists in the source dictionary. You will get a `KeyError`

```python
obj1 = dictcopy.extract(obj, {
    "age",
    "email"
}, strict_mode=True)
```