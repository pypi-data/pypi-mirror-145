# colassigner

[![Documentation Status](https://readthedocs.org/projects/colassigner/badge/?version=latest)](https://colassigner.readthedocs.io/en/latest)
[![codeclimate](https://img.shields.io/codeclimate/maintainability/endremborza/colassigner.svg)](https://codeclimate.com/github/endremborza/colassigner)
[![codecov](https://img.shields.io/codecov/c/github/endremborza/colassigner)](https://codecov.io/gh/endremborza/colassigner)
[![pypi](https://img.shields.io/pypi/v/colassigner.svg)](https://pypi.org/project/colassigner/)


fitting somewhat complex, nested data structures into tables, and removing the need to remember the name and construction logic of any column, if you can rely on static analysis

things to think about:
- draw a reliance dag based on calls
- pivot table: data content based columns
  - enum type support
- changing record entity type
- partial inheritance / composite types
