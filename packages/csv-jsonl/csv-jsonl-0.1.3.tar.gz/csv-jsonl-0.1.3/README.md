# csv-jsonlines

A convenient module for writing a list of dictionaries to a [`.jsonl`-formatted](https://jsonlines.org/) text file, suitable for ingestion by [BigQuery](https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-json) and other services.

`csv-jsonlines` is built on top of Python's built-in `csv` module. It allows you to specify a `fieldnames` list to add a bit of assurance. Otherwise, no schema-handling is offered.

# Why not Just Use `csv` Files?

If you are here asking that question, I'm guessing you have not spent exciting times attempting to clean up poorly-formatted csv files (I'm looking at you, Excel).


# Installation

`pip install csv-jsonl`

# Usage

```python
>>> from csv_jsonl import JSONLinesDictWriter
>>> l = [{"foo": "bar", "bat": 1}, {"foo": "bar", "bat": 2}]
>>> with open("foo.jsonl", "w", encoding="utf-8") as _fh:
...     writer = JSONLinesDictWriter(_fh)
...     writer.writerows(l)
...
>>> d = {"foo": "bar", "bat": 1}
>>> with open("bar.jsonl", "w", encoding="utf-8") as _fh:
...     writer = JSONLinesDictWriter(_fh)
...     writer.writerow(d)
...
>>> from collections import OrderedDict
>>> od = OrderedDict([('foo', 'bar'), ('bat', 1)])
>>> with open("qux.jsonl", "w", encoding="utf-8") as _fh:
...     writer = JSONLinesDictWriter(_fh)
...     writer.writerow(od)
...
>>> fieldnames = ["foo", "bar"] # keys = ["foo", "bat"] expect fail
>>> with open("baz.jsonl", "w", encoding="utf-8") as _fh:
...     writer = JSONLinesDictWriter(_fh, fieldnames=fieldnames)
...     writer.writerows(l)
...
Expect ValueError
```

[![pipeline status](https://gitlab.com/doug.shawhan/csv-jsonl/badges/main/pipeline.svg)](https://gitlab.com/doug.shawhan/csv-jsonl/-/commits/main)
[![coverage report](https://gitlab.com/doug.shawhan/csv-jsonl/badges/main/coverage.svg)](https://gitlab.com/doug.shawhan/csv-jsonl/-/commits/main)
[![Latest Release](https://gitlab.com/doug.shawhan/csv-jsonl/-/badges/release.svg)](https://gitlab.com/doug.shawhan/csv-jsonl/-/releases)
