EightID: A (really) short id, that fits in 8 bytes.
===============

[![Build Status](https://github.com/barrachri/gid/workflows/Test/badge.svg)](https://github.com/barrachri/eightid/actions)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/eightid.svg)](https://pypi.python.org/pypi/eightid)

```EightID``` is a short ID that fits in 8 bytes. 4 bytes are dedicated to the timestamp (second resolution) and the other are 4 random bytes.

It's only 8 bytes and as such it fits in a BigInt column.

Installation
------------

Installation using pip:

    pip install eightid

Quick intro
-------------

```python
>>> from eightid import EightID
>>> short_id = EightID()

# Displays as base64 by default
>>> short_id
<EightID 'AH4jTMKtwrXCr8OQ'>
>>> print(short_id)
AH4jTMKtwrXCr8OQ
>>> short_id.integer
35504659304394704

# Access when the id was created
>>> short_id.datetime
datetime.datetime(2022, 4, 6, 17, 16, 12)

# Access with str() and .string
>>> str(short_id)
'AH4jTMKtwrXCr8OQ'
>>> short_id.string
'AH4jTMKtwrXCr8OQ'

# Recreate the EightID from a string
>>> EightID.from_string(short_id.string)
<EightID 'AH4jTMKtwrXCr8OQ'>

# Or from
>>> EightID.from_int(short_id.integer)
<EightID 'AH4jTMKtwrXCr8OQ'>
```

Django integration
-------------

```python
from eightid import django


class AppModel(models.Model):
    id = django.EightIDField(primary_key=True)
```

License
-------

EightID is licensed under the MIT license (see the ```LICENSE``` file for details).
