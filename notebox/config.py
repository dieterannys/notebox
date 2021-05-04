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
    title_format: str
    context_provider: ContextTypeProviderConfig = None

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            name=d['name'],
            title_format=d.get('title_format', "{title}"),
            context_provider=ContextTypeProviderConfig.from_dict(d.get('context_provider')) if d.get('context_provider') is not None else None,
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

