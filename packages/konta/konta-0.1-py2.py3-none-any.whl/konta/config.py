#!/usr/bin/env python3
"""
Configuration module of Konta.

The configuration is mostly read from a TOML file located in the relevant XDG folder.

The module exposes all the API to read from the config, and also validates all the
data before it's accessed by the rest of the code.
"""

import dataclasses
import pathlib
import toml
import xdg
from typing import Dict, Optional, List

from beancount.core import data


ACCOUNT_KEY = "Accounts"
ACCOUNT_NAME_KEY = "name"
ACCOUNT_CURR_KEY = "default-currency"

PAYEES_KEY = "Payees"
PAYEES_NAME_KEY = "name"
PAYEES_CAT_KEY = "category"

DEFAULT_KEY = "Default"
DEFAULT_CAT_KEY = "category"

BEANS_KEY = "Beans"
BEANS_I_KEY = "input"


@dataclasses.dataclass
class Account:
    """An account known by id."""

    id: str
    name: data.Account
    default_currency: data.Currency


@dataclasses.dataclass
class Payee:
    """A payee known by label."""

    raw_label: str
    pretty_name: Optional[str]
    category: data.Account

    @property
    def name(self) -> str:
        """Get the name."""
        return self.pretty_name if self.pretty_name is not None else self.raw_label


@dataclasses.dataclass
class Beans:
    """The beans."""

    inputs: Optional[List[pathlib.Path]]


class Config:
    """The main configuration object."""

    def __init__(self, raw: Dict[any, any]):
        """Construct."""
        self._default_cat = raw[DEFAULT_KEY][DEFAULT_CAT_KEY]
        self._accounts = {
            k: Account(k, v[ACCOUNT_NAME_KEY], v[ACCOUNT_CURR_KEY])
            for (k, v) in raw[ACCOUNT_KEY].items()
        }
        self._payees = {
            k: Payee(
                k, v.get(PAYEES_NAME_KEY), v.get(PAYEES_CAT_KEY, self._default_cat)
            )
            for (k, v) in raw[PAYEES_KEY].items()
        }
        self._beans = Beans(raw[BEANS_KEY].get(BEANS_I_KEY))

    def get_account(self, id: str) -> Account:
        """Get the account info for given id."""
        return self._accounts[id]

    def get_payee(self, label: str) -> Payee:
        """Get the payee for given transaction label."""
        return self._payees.get(label, Payee(label, None, self._default_cat))

    def get_exising_input_paths(self) -> Optional[List[pathlib.Path]]:
        """Return the existing paths."""
        return self._beans.inputs

    def from_toml(file_path: Optional[pathlib.Path] = None) -> "Config":
        """
        Return a Config object from a toml file.

        Uses default xdg path if path is not given.
        """
        actual_path = (
            file_path
            if file_path is not None
            else (xdg.xdg_config_home() / "konta" / "config.toml")
        )
        raw_dict = toml.load(actual_path)
        return Config(raw_dict)
