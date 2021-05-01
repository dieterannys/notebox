#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, List, Any

import yaml


@dataclass
class ContextProviderConfig:
    name: str
    type: str
    params: Dict[str, Any]

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            name=d['name'],
            type=d['type'],
            params=d['params']
        )


@dataclass
class ContextTypeProviderConfig:
    name: str
    collection: str

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            name=d['name'],
            collection=d['collection'],
        )


@dataclass
class ContextTypeConfig:
    name: str
    context_provider: ContextTypeProviderConfig
    title_format: str

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            name=d['name'],
            context_provider=ContextTypeProviderConfig.from_dict(d['context_provider']),
            title_format=d['title_format']
        )


@dataclass
class Config:
    name: str
    path: str
    editor: str
    context_providers: List[ContextProviderConfig]
    context_types: List[ContextTypeConfig]

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            name=d['name'],
            path=d['path'],
            editor=d['editor'].split(' '),
            context_providers=[ContextProviderConfig.from_dict(ds) for ds in d['context_providers']],
            context_types=[ContextTypeConfig.from_dict(ds) for ds in d['context_types']]
        )
    
    @classmethod
    def from_yaml_file(cls, filepath: str):
        with open(filepath) as f:
            raw = yaml.load(f, Loader=yaml.FullLoader)
        return cls.from_dict(raw)

