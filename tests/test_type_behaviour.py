# -*- coding: utf-8 -*-
import pytest

from smolstore import SmolStore
from smolstore.document import Document


@pytest.fixture
def new_dict():
    return {"key": "value"}


@pytest.fixture
def new_doc(new_dict):
    store = SmolStore()
    table = store.table()
    table.insert(new_dict)
    return next(table.get(table.fields.key == "value"))


def test_equivalence(new_dict, new_doc):
    assert new_dict == new_doc


def test_update(new_doc):
    new_doc.update({"key": "new_value"})
    assert new_doc == {"key": "new_value"}


def test_add_item(new_doc):
    new_doc["key2"] = "value2"
    assert new_doc == {"key": "value", "key2": "value2"}


def test_iterate(new_doc):
    loops = 0
    for key, value in new_doc.items():
        loops += 1
        assert key == "key"
        assert value == "value"
        assert loops == 1


def test_length(new_doc):
    assert len(new_doc) == 1
    table = new_doc._document_table
    table.insert({"one": 1, "two": 2})
    doc2 = next(table.get(table.fields.one == 1))
    assert len(doc2) == 2


def test_pop(new_doc):
    assert new_doc.pop("key") == "value"
    assert len(new_doc) == 0
    assert new_doc == {}


def test_str(new_doc):
    assert str(new_doc) == "{'key': 'value'}"
