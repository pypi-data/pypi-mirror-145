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

from click import argument, command, echo, pass_context
from duniterpy.api.bma import blockchain, tx
from duniterpy.documents.transaction import InputSource
from tabulate import tabulate

from silkaj import wot_tools as wt
from silkaj.auth import auth_method, has_auth_method
from silkaj.blockchain_tools import HeadBlock
from silkaj.crypto_tools import (
    check_pubkey_format,
    is_pubkey_and_check,
    validate_checksum,
)
from silkaj.network_tools import ClientInstance
from silkaj.tools import CurrencySymbol
from silkaj.tui import display_amount, display_pubkey_and_checksum


@command("balance", help="Get wallet balance")
@argument("pubkeys", nargs=-1)
@pass_context
def cmd_amount(ctx, pubkeys):
    if not has_auth_method():

        # check input pubkeys
        if not pubkeys:
            sys.exit("You should specify one or many pubkeys")
        pubkeys_list = list()
        wrong_pubkeys = False
        for inputPubkey in pubkeys:
            pubkey = is_pubkey_and_check(inputPubkey)
            if not pubkey:
                wrong_pubkeys = True
                print(f"ERROR: pubkey {inputPubkey} has a wrong format")
            elif pubkey in pubkeys_list:
                sys.exit(
                    f"ERROR: pubkey {display_pubkey_and_checksum(pubkey)} was specified many times"
                )
            pubkeys_list.append(pubkey)
        if wrong_pubkeys:
            sys.exit("Please check the pubkeys format.")

        total = [0, 0]
        for pubkey in pubkeys_list:
            inputs_balance = get_amount_from_pubkey(pubkey)
            show_amount_from_pubkey(pubkey, inputs_balance)
            total[0] += inputs_balance[0]
            total[1] += inputs_balance[1]
        if len(pubkeys_list) > 1:
            show_amount_from_pubkey("Total", total)
    else:
        key = auth_method()
        pubkey = key.pubkey
        show_amount_from_pubkey(pubkey, get_amount_from_pubkey(pubkey))


def show_amount_from_pubkey(label, inputs_balance):
    """
    Shows the balance of a pubkey.
    `label` can be either a pubkey or "Total".
    """
    totalAmountInput = inputs_balance[0]
    balance = inputs_balance[1]
    currency_symbol = CurrencySymbol().symbol
    ud_value = UDValue().ud_value
    average, monetary_mass = get_average()
    member = False

    # if `pubkey` is a pubkey, get pubkey:checksum and uid
    if label != "Total":
        member = wt.is_member(label)
        label = display_pubkey_and_checksum(label)
    # display balance table
    display = list()
    display.append(["Balance of pubkey", label])

    if member:
        display.append(["User identifier", member["uid"]])

    if totalAmountInput - balance != 0:
        display_amount(display, "Blockchain", balance, ud_value, currency_symbol)
        display_amount(
            display,
            "Pending transaction",
            (totalAmountInput - balance),
            ud_value,
            currency_symbol,
        )
    display_amount(display, "Total amount", totalAmountInput, ud_value, currency_symbol)
    display.append(
        [
            "Total relative to M/N",
            f"{round(totalAmountInput / average, 2)} x M/N",
        ]
    )
    echo(tabulate(display, tablefmt="fancy_grid"))


def get_average():
    head = HeadBlock().head_block
    monetary_mass = head["monetaryMass"]
    members_count = head["membersCount"]
    average = monetary_mass / members_count
    return average, monetary_mass


def get_amount_from_pubkey(pubkey):
    listinput, amount = get_sources(pubkey)

    totalAmountInput = 0
    for input in listinput:
        totalAmountInput += amount_in_current_base(input)
    return totalAmountInput, amount


def get_sources(pubkey):
    client = ClientInstance().client
    # Sources written into the blockchain
    sources = client(tx.sources, pubkey)

    listinput = list()
    amount = 0
    for source in sources["sources"]:
        if source["conditions"] == f"SIG({pubkey})":
            listinput.append(
                InputSource(
                    amount=source["amount"],
                    base=source["base"],
                    source=source["type"],
                    origin_id=source["identifier"],
                    index=source["noffset"],
                )
            )
            amount += amount_in_current_base(listinput[-1])

    # pending source
    history = client(tx.pending, pubkey)
    history = history["history"]
    pendings = history["sending"] + history["receiving"] + history["pending"]

    # add pending output
    pending_sources = list()
    for pending in pendings:
        identifier = pending["hash"]
        for i, output in enumerate(pending["outputs"]):
            outputsplited = output.split(":")
            if outputsplited[2] == f"SIG({pubkey})":
                inputgenerated = InputSource(
                    amount=int(outputsplited[0]),
                    base=int(outputsplited[1]),
                    source="T",
                    origin_id=identifier,
                    index=i,
                )
                if inputgenerated not in listinput:
                    # add pendings before blockchain sources for change txs
                    listinput.insert(0, inputgenerated)

        for input in pending["inputs"]:
            pending_sources.append(InputSource.from_inline(input))

    # remove input already used
    for input in pending_sources:
        if input in listinput:
            listinput.remove(input)

    return listinput, amount


class UDValue:
    __instance = None

    def __new__(cls):
        if UDValue.__instance is None:
            UDValue.__instance = object.__new__(cls)
        return UDValue.__instance

    def __init__(self):
        self.ud_value = self.get_ud_value()

    def get_ud_value(self):
        client = ClientInstance().client
        blockswithud = client(blockchain.ud)
        NBlastUDblock = blockswithud["result"]["blocks"][-1]
        lastUDblock = client(blockchain.block, NBlastUDblock)
        return lastUDblock["dividend"] * 10 ** lastUDblock["unitbase"]


def amount_in_current_base(source):
    """
    Get amount in current base from input or output source
    """
    return source.amount * 10**source.base
