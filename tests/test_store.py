# -*- coding: utf-8 -*-
from smolstore import SmolStore


def test_init_in_memory():
    store = SmolStore()
    assert isinstance(store, SmolStore)
