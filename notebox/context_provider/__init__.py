#!/usr/bin/env python3

from notebox.config import ContextProviderConfig
from notebox.context_provider.gcal import ContextProviderGcal
from notebox.context_provider.todoist import ContextProviderTodoist


context_provider_map = dict(
    gcal=ContextProviderGcal,
    todoist=ContextProviderTodoist
)


def context_provider_factory(config: ContextProviderConfig):
    return context_provider_map[config.type](config.params)

