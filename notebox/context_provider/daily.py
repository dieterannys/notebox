#!/usr/bin/env python3

from datetime import datetime

from notebox.context_provider.base import ContextProvider, ContextProviderItem


class ContextProviderDaily(ContextProvider):

    def get_items(self, filters):
        return [ContextProviderItem(
            title=datetime.now().strftime("%Y-%m-%d"),
            uid=datetime.now().strftime("%Y-%m-%d"),
        )]

