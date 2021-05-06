#!/usr/bin/env python3

from datetime import datetime

from notebox.context_provider.base import ContextProvider, ContextProviderItem, ContextProviderItemType


class ContextProviderDaily(ContextProvider):

    def get_items(self, collection: str = "daily"):
        # collection can later be used to return weekly, monthly, etc notes
        return [ContextProviderItem(
            title=datetime.now().strftime("%Y-%m-%d"),
            uid=datetime.now().strftime("%Y-%m-%d"),
            item_type=ContextProviderItemType.DAILY,
        )]

