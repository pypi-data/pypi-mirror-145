#!/usr/bin/env python3
"""Import the data from Woob bank."""

from typing import Dict, List
from collections.abc import Iterator
import datetime as dt

from woob.core import Woob, bcall
from woob.capabilities.bank import CapBank, base
from woob.capabilities.base import NotLoadedType


def _get_tx_list(
    iterable_obj: Iterator[base.Transaction], min_date: dt.datetime
) -> List[base.Transaction]:
    """
    Filter a list of transaction.

    Helper function to consume an iterator of transactions and filter
    it to only keep operations after a given min_date.

    The function manually unsugar the iteration to try and
    catch the backend calls errors.

    iterable_obj is an iterator returned by iter_history() or iter_accounts()
    """
    res = []
    tx_iter = iter(iterable_obj)
    while True:
        try:
            tran = next(tx_iter)
            tx_date = (
                tran.rdate
                if not isinstance(tran.rdate, NotLoadedType)
                else tran.date
            )
            if tx_date < min_date:
                continue
            res.append(tran)
        except StopIteration:
            break
        # We don't care about the ugly errors behind curtains
        # in practice they tend to be unrelated to the current
        # account being processed
        except bcall.CallErrors:
            continue
    return res


def import_data(min_date: dt.datetime) -> Dict[str, Dict[str, List[base.Transaction]]]:
    """Import woob bank data."""
    w = Woob()
    w.load_backends(CapBank)
    res = {}
    account_list = iter(w.iter_accounts())
    # Pattern used to deal with the account iterator raising exceptions
    while True:
        try:
            account = next(account_list)
            print(f"Processing account {account.id}")
            historic = w.iter_history(account)
            coming = w.iter_coming(account)
            res[account.id] = {}
            if historic is not None:
                res[account.id]["history"] = _get_tx_list(historic, min_date)
            if coming is not None:
                res[account.id]["coming"] = _get_tx_list(coming, min_date)
        except StopIteration:
            break
        except bcall.CallErrors as e:
            print(f"Ignoring an account because of {len([1 for it in e])} errors")
            for backend, error, backtrace in e:
                print(f"{error}")
            continue
    return res
