#!/usr/bin/env python3

from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum


@dataclass
class ContextProviderItem:
    title: str
    uid: str
    collection: str = None
    account: str = None
    service: str = None
    tags: List[str] = field(default_factory=list)
    created_time: datetime = None
    start_time: datetime = None
    end_time: datetime = None
    raw: Any = None


class ContextProvider:

    def __init__(self, params = dict()):
        pass
    
    def get_items(self, filters: Dict[str, Any]):
        raise NotImplementedError

