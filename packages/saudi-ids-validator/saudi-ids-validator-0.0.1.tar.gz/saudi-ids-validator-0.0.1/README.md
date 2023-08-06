# saudi-id-validator
A tiny package that helps you validate Saudi national or iqama ids. Inspired by the original repo [Saudi-ID-Validator](https://github.com/alhazmy13/Saudi-ID-Validator) so special thanks to them!


## Features
Accepts number or string <br/>
Accepts both eastern and western Arabic numbers <br/>


## Installation
To install the package run:
```bash
pip install saudi-id-validator
```


## Usage
Here's a basic example on how you can use the package:

```python
from saudi_id_validator import is_valid_saudi_id

print(is_valid_saudi_id("1000000008"))   # => true if this's your id please don't sue me :)
print(is_valid_saudi_id(1000000008))     # => true
print(is_valid_saudi_id("١٠٠٠٠٠٠٠٠٨"))   # => true
print(is_valid_saudi_id("1000000000"))   # => false
print(is_valid_saudi_id("100000000"))    # => false
print(is_valid_saudi_id("not a number")) # => false
```
