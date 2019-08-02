# -*- coding: utf-8 -*-
from smolstore import SmolStore
from smolstore.table import Table


def test_init_in_memory():
    store = SmolStore()
    assert isinstance(store, SmolStore)


def test_create_named_table():
    store = SmolStore()
    _ = store.table("new_table")
    assert isinstance(store._tables.get("new_table"), Table)


def test_retrieve_table():
    store = SmolStore()
    table1 = store.table("new_table")
    table2 = store.table("new_table")
    assert table1 is table2


def test_rollback():
    store = SmolStore()
    _ = store.table("new_table")
    assert isinstance(store._tables.get("new_table"), Table)

    store.rollback()
    assert store._tables == {}
