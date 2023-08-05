# nors

nors is a counting the number of rows and records in a CSV file.

## Install

```sh
pip install nors
```

## Usage

```python
from nors import count

print(count("10_lines_and_records.csv"))
{'lines': 10, 'csv_records': 10}
```
