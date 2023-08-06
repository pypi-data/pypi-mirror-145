# Python runtime loader (pyrulo)
Python library to import classes from script files at runtime.

# Installation
`pip install pyrulo`

# Usage

Lets say we have the following scripts
```python
# base.py script

class Base:
  pass
```

```python
# a.py script
from base import Base

class A(Base):
  pass
```

```python
# b.py script
from base import Base

class B(Base):
  pass
```

```python
# c.py script
from base import Base

class C(Base):
  pass
```
We can use pyrulo to retrieve all classes that inherits from `Base` in a given script path or folder
```python
from base import Base
from pyrulo import class_imports

script_path = "a.py"
folder_path = "."

script_classes = class_imports.import_classes_in_file(script_path, Base)  # returns [A]
folder_classes = class_imports.import_classes_in_dir(folder_path, Base)  # returns [A, B, C]
```
