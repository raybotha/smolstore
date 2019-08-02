# -*- coding: utf-8 -*-
import pytest
from smolstore.document import Document


@pytest.fixture
def new_dict():
    return {"key": "value"}


@pytest.fixture
def new_doc(new_dict):
    return Document(new_dict)


def test_well_behaved_repr(new_doc):
    assert eval(repr(new_doc)) == new_doc


def test_equivalence(new_dict, new_doc):
    assert new_dict == new_doc


def test_update(new_doc):
    new_doc.update({"key": "new_value"})
    assert new_doc == {"key": "new_value"}


def test_add_item(new_doc):
    new_doc["key2"] = "value2"
    assert new_doc == {"key": "value", "key2": "value2"}


def test_remove_item():
    doc = Document({"key1": "value1", "key2": "value2"})
    del doc["key2"]
    assert doc == {"key1": "value1"}


def test_iterate(new_doc):
    loops = 0
    for key, value in new_doc.items():
        loops += 1
        assert key == "key"
        assert value == "value"
        assert loops == 1


def test_length(new_doc):
    assert len(new_doc) == 1
    doc2 = Document({1: 1, 2: 2})
    assert len(doc2) == 2


def test_pop(new_doc):
    assert new_doc.pop("key") == "value"
    assert len(new_doc) == 0
    assert new_doc == {}


def test_str(new_doc):
    assert str(new_doc) == "{'key': 'value'}"
