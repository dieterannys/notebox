#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum


class ContextProviderItemType(Enum):
    EVENT = 1
    TASK = 2


@dataclass
class ContextProviderItem:
    title: str
    uid: str
    collection: str
    account: str
    service: str
    item_type: ContextProviderItemType
    attributes: Dict[str, Any]
    raw: Any = None


class ContextProvider:
    
    def get_items(self, collection: str):
        raise NotImplementedError

