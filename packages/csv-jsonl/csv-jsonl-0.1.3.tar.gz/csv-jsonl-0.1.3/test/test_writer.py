from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
import tempfile

import pytest

from csv_jsonl import JSONLinesDictWriter

LOD = [{"foo": "bar", "bat": 1}, {"foo": "bar", "bat": 2}]
LOOD = [OrderedDict([('foo', 'bar'), ('bat', 1)]), OrderedDict([('foo', 'bar'), ('bat', 2)])]

def lood_gen():
    for _ in LOOD:
        yield _

def dataclass_gen():

    @dataclass
    class DCTest:
        foo: str
        bar: int

    for foo, bar in zip(["foo", "bar"], range(2)):
        yield DCTest(foo, bar)

def _writerow(data):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(Path(tempdir, "foo.jsonl"), "w", encoding="utf-8") as _fh:
            writer = JSONLinesDictWriter(_fh)
            writer.writerow(LOD[0])

def _writerows(data):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(Path(tempdir, "foo.jsonl"), "w", encoding="utf-8") as _fh:
            writer = JSONLinesDictWriter(_fh)
            writer.writerows(LOD)

def _writerows_fieldnames(data, fieldnames):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(Path(tempdir, "foo.jsonl"), "w", encoding="utf-8") as _fh:
            writer = JSONLinesDictWriter(_fh, fieldnames=fieldnames)
            writer.writerows(LOD)

def test_writerow():
    assert _writerow(LOD) == None

def test_writerows():
    assert _writerows(LOD) == None

def test_writerows_ordered_dict():
    assert _writerows(LOOD) == None

def test_writerows_fieldnames():
    assert _writerows_fieldnames(LOD, fieldnames = list(LOD[0].keys())) == None

def test_writerows_fieldnames_bad():
    error_string = "dict contains fields not in fieldnames: 'bat'"
    with pytest.raises(ValueError, match = error_string):
        _writerows_fieldnames(LOD, fieldnames = ["foo", "bar",])

def test_writerows_newlines_in_values():
    annoyance = [
        {"foo": "bar", "bat": "qux\nuux"},
        {"foo": "bar", "bat": "qux\r\nquux"},
    ]
    assert _writerow(annoyance) == None

def test_writerows_ordered_dict_from_generator():
    assert _writerows(lood_gen()) == None

def test_writerows_dataclasss_from_generator():
    assert _writerows(dataclass_gen()) == None

def test_non_dict_iterables():
    assert _writerows(range(10)) == None
    assert _writerows("Now, why would you do this?") == None
    assert _writerows(["Now, why would you do that?"]) == None
