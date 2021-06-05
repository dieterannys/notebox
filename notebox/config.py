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
            params=d.get('params', dict())
        )


@dataclass
class ContextFolderConfig:
    provider: str
    title_format: str
    filter: Dict[str, Any]

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            provider=d['provider'],
            title_format=d.get('title_format', "{title}"),
            filter=d.get('filter', dict())
        )


@dataclass
class DomainConfig:
    name: str
    event: ContextFolderConfig
    project: ContextFolderConfig

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            name=d['name'],
            event=ContextFolderConfig.from_dict(d.get('event')) if d.get('event') is not None else None,
            project=ContextFolderConfig.from_dict(d.get('project')) if d.get('project') is not None else None,
        )


@dataclass
class Config:
    path: str
    editor: str
    context_providers: List[ContextProviderConfig]
    source: ContextFolderConfig
    domains: List[DomainConfig]

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            path=d['path'],
            editor=d['editor'].split(' '),
            context_providers=[ContextProviderConfig.from_dict(ds) for ds in d['context_providers']],
            source=ContextFolderConfig.from_dict(d['source']),
            domains=[DomainConfig.from_dict(ds) for ds in d['domains']],
        )
    
    @classmethod
    def from_yaml_file(cls, filepath: str):
        with open(filepath) as f:
            raw = yaml.load(f, Loader=yaml.FullLoader)
        return cls.from_dict(raw)

