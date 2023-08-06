# nbasenumber

## Usage

This package is using for complex fractions' calculation.

## How to use it

import it by: `from complex_fraction import Fraction`. No any additional modules or packages will be installed.

## Extensibility

```python3
>>> # Convert an instance to Fraction
>>> class Foo(object) :
...    def __Fraction__(self) :
...        return Fraction(1)
...
>>> Fraction(Foo())
Fraction(1)
```
