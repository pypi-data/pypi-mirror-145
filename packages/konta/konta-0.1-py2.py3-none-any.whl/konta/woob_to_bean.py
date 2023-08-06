#!/usr/bin/env python3
"""Transformer library from woob to beancount."""

import hashlib
from typing import Optional

from woob.capabilities.bank import base
from woob.capabilities.base import NotLoadedType, NotAvailableType
from beancount.core.data import Transaction, Posting, Amount
from beancount.core import flags

from konta.config import Config


UNDEFINED_CAT = "Expenses:Undefined"


def _get_id(tx: base.Transaction) -> str:
    tx_date = tx.rdate if not isinstance(tx.rdate, NotLoadedType) else tx.date
    preimage = f"woob_{tx.id}_{tx_date}_{tx.amount}_{tx.raw}"
    return f"v1-{hashlib.sha3_224(preimage.encode()).hexdigest()[0:12]}"


def woob_to_bean(
    config: Config, src_account: str, tx: base.Transaction
) -> Optional[Transaction]:
    """Transform woob transaction to beancount."""
    # Ignore transactions that don't have an amount
    if isinstance(tx.amount, NotLoadedType) or isinstance(tx.amount, NotAvailableType):
        return None
    acc = config.get_account(src_account)
    payee = config.get_payee(tx.label)
    tx_date = tx.rdate if not isinstance(tx.rdate, NotLoadedType) else tx.date
    my_posting = Posting(
        account=acc.name,
        units=Amount(tx.amount, acc.default_currency),
        meta=None,
        price=None,
        cost=None,
        flag=None,
    )
    sorted_posting = Posting(
        account=payee.category,
        units=Amount(tx.amount * -1, acc.default_currency),
        meta=None,
        price=None,
        cost=None,
        flag=None,
    )
    res = Transaction(
        date=tx_date,
        flag=flags.FLAG_OKAY,
        payee=payee.name,
        narration="",
        tags=set(),
        links=set(),
        meta={"konta_id": _get_id(tx)},
        postings=[my_posting, sorted_posting],
    )
    return res
