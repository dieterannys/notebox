#!/usr/bin/env python3

from dataclasses import dataclass, field
from typing import Dict, Any
from enum import Enum


class ContextProviderItemType(Enum):
    EVENT = 1
    TASK = 2
    DAILY = 3


@dataclass
class ContextProviderItem:
    title: str
    uid: str
    item_type: ContextProviderItemType
    collection: str = None
    account: str = None
    service: str = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


class ContextProvider:

    def __init__(self, params):
        pass
    
    def get_items(self, collection: str):
        raise NotImplementedError

