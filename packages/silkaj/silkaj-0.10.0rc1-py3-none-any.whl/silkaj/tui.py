# Copyright  2016-2022 Maël Azimi <m.a@moul.re>
#
# Silkaj is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Silkaj is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Silkaj. If not, see <https://www.gnu.org/licenses/>.

import sys
from datetime import datetime

import click

from silkaj import constants
from silkaj import crypto_tools as ct
from silkaj import wot_tools


def display_amount(tx, message, amount, ud_value, currency_symbol):
    """
    Displays an amount in unit and relative reference.
    """
    UD_amount = str(round((amount / ud_value), 2))
    unit_amount = str(amount / 100)
    tx.append(
        [
            f"{message} (unit|relative)",
            f"{unit_amount} {currency_symbol} | {UD_amount} UD {currency_symbol}",
        ]
    )


def display_pubkey(tx, message, pubkey):
    """
    Displays a pubkey and the eventually associated id.
    """
    tx.append([f"{message} (pubkey:checksum)", display_pubkey_and_checksum(pubkey)])
    id = wot_tools.is_member(pubkey)
    if id:
        tx.append([f"{message} (id)", id["uid"]])


def display_pubkey_and_checksum(
    pubkey, short=False, length=constants.SHORT_PUBKEY_SIZE
):
    """
    Returns "<pubkey>:<checksum>" in full form.
    returns `length` first chars of pubkey and checksum in short form.
    `length` defaults to SHORT_PUBKEY_SIZE.
    """
    short_pubkey = f"{pubkey[:length]}…" if short else pubkey
    return f"{short_pubkey}:{ct.gen_checksum(pubkey)}"


def send_doc_confirmation(document_name):
    if not click.confirm(f"Do you confirm sending this {document_name}?"):
        sys.exit(constants.SUCCESS_EXIT_STATUS)
