#!/usr/bin/env python3
"""Import the data from Beancount book."""

from beancount import loader
from beancount.core.data import Entries


def import_data(file_path) -> Entries:
    """Import data from a path."""
    entries, errors, options = loader.load_file(file_path)
    return entries
