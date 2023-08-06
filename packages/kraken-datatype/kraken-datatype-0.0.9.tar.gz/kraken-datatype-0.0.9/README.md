# kraken datatype

## Overview
Library to extract, validate and normalize datatypes. 

datatypes:
- email
- url
- date
- country
- address
- telephone
- bool
- currency
- domain


## functions:
- validate: returns True false if validate
- normalize: returns normalized value or None
- guess: return best guess or None of datatype



## How to use:

```
import kraken_datatype as dt 

result = dt.validate('email', 'name@test.com')
print(result)

result = dt.normalize('email', 'name@test.com')
print(result)

result = dt.guess('name@test.com')
print(result)
```
