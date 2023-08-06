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

from collections import OrderedDict
from operator import itemgetter
from os import system

import jsonschema
from click import IntRange, argument, command, option
from duniterpy.api import bma
from pendulum import from_timestamp
from tabulate import tabulate
from websocket._exceptions import WebSocketConnectionClosedException

from silkaj.blockchain_tools import HeadBlock
from silkaj.constants import ALL, HOUR
from silkaj.network_tools import ClientInstance, determine_endpoint
from silkaj.tools import CurrencySymbol
from silkaj.wot_tools import identity_of


@command("info", help="Display information about currency")
def currency_info():
    head_block = HeadBlock().head_block
    ep = determine_endpoint()
    current_time = from_timestamp(head_block["time"], tz="local")
    mediantime = from_timestamp(head_block["medianTime"], tz="local")
    print(
        "Connected to node:",
        ep.host,
        ep.port,
        "\nCurrent block number:",
        head_block["number"],
        "\nCurrency name:",
        CurrencySymbol().symbol,
        "\nNumber of members:",
        head_block["membersCount"],
        "\nMinimal Proof-of-Work:",
        head_block["powMin"],
        "\nCurrent time:",
        current_time.format(ALL),
        "\nMedian time:",
        mediantime.format(ALL),
        "\nDifference time:",
        current_time.diff_for_humans(mediantime, True),
    )


def match_pattern(pow, match="", p=1):
    while pow > 0:
        if pow >= 16:
            match += "0"
            pow -= 16
            p *= 16
        else:
            match += f"[0-{hex(15 - pow)[2:].upper()}]"
            p *= pow
            pow = 0
    return f"{match}*", p


def power(nbr, pow=0):
    while nbr >= 10:
        nbr /= 10
        pow += 1
    return f"{nbr:.1f} × 10^{pow}"


@command(
    "diffi",
    help="Display the current Proof of Work difficulty level to generate the next block",
)
def difficulties():
    client = ClientInstance().client
    try:
        ws = client(bma.ws.block)
        while True:
            current = ws.receive_json()
            jsonschema.validate(current, bma.ws.WS_BLOCK_SCHEMA)
            diffi = client(bma.blockchain.difficulties)
            display_diffi(current, diffi)
    except (jsonschema.ValidationError, WebSocketConnectionClosedException) as e:
        print(f"{str(e.__class__.__name__)}: {str(e)}")


def display_diffi(current, diffi):
    levels = [OrderedDict((i, d[i]) for i in ("uid", "level")) for d in diffi["levels"]]
    diffi["levels"] = levels
    issuers = 0
    sorted_diffi = sorted(diffi["levels"], key=itemgetter("level"), reverse=True)
    for d in diffi["levels"]:
        if d["level"] / 2 < current["powMin"]:
            issuers += 1
        d["match"] = match_pattern(d["level"])[0][:20]
        d["Π diffi"] = power(match_pattern(d["level"])[1])
        d["Σ diffi"] = d.pop("level")
    system("cls||clear")
    block_gen = from_timestamp(current["time"], tz="local").format(ALL)
    match = match_pattern(int(current["powMin"]))[0]
    table = tabulate(sorted_diffi, headers="keys", tablefmt="orgtbl", stralign="center")
    content = f'Current block: n°{current["number"]}, generated on {block_gen}\n\
Generation of next block n°{diffi["block"]} possible by at least {issuers}/{len(diffi["levels"])} members\n\
Common Proof-of-Work difficulty level: {current["powMin"]}, hash starting with `{match}`\n{table}'
    print(content)


@command("blocks", help="Display blocks: default: 0 for current window size")
@argument("number", default=0, type=IntRange(0, 5000))
@option(
    "--detailed",
    "-d",
    is_flag=True,
    help="Force detailed view. Compact view happen over 30 blocks",
)
def list_blocks(number, detailed):
    head_block = HeadBlock().head_block
    current_nbr = head_block["number"]
    if number == 0:
        number = head_block["issuersFrame"]
    client = ClientInstance().client
    blocks = client(bma.blockchain.blocks, number, current_nbr - number + 1)
    issuers = list()
    issuers_dict = dict()
    for block in blocks:
        issuer = OrderedDict()
        issuer["pubkey"] = block["issuer"]
        if detailed or number <= 30:
            gentime = from_timestamp(block["time"], tz="local").format(ALL)
            mediantime = from_timestamp(block["medianTime"], tz="local").format(ALL)
            issuer["block"] = block["number"]
            issuer["gentime"] = gentime
            issuer["mediantime"] = mediantime
            issuer["hash"] = block["hash"][:10]
            issuer["powMin"] = block["powMin"]
        issuers_dict[issuer["pubkey"]] = issuer
        issuers.append(issuer)
    for pubkey in issuers_dict.keys():
        issuer = issuers_dict[pubkey]
        idty = identity_of(issuer["pubkey"])
        for issuer2 in issuers:
            if (
                issuer2.get("pubkey") is not None
                and issuer.get("pubkey") is not None
                and issuer2["pubkey"] == issuer["pubkey"]
            ):
                issuer2["uid"] = idty["uid"]
                issuer2.pop("pubkey")
    header = (
        f"Last {number} blocks from n°{current_nbr - number + 1} to n°{current_nbr}"
    )
    print(header, end=" ")
    if detailed or number <= 30:
        sorted_list = sorted(issuers, key=itemgetter("block"), reverse=True)
        table = tabulate(
            sorted_list, headers="keys", tablefmt="orgtbl", stralign="center"
        )
        print(f"\n{table}")
    else:
        list_issued = list()
        for issuer in issuers:
            found = False
            for issued in list_issued:
                if issued.get("uid") is not None and issued["uid"] == issuer["uid"]:
                    issued["blocks"] += 1
                    found = True
                    break
            if not found:
                issued = OrderedDict()
                issued["uid"] = issuer["uid"]
                issued["blocks"] = 1
                list_issued.append(issued)
        for issued in list_issued:
            issued["percent"] = issued["blocks"] / number * 100
        sorted_list = sorted(list_issued, key=itemgetter("blocks"), reverse=True)
        table = tabulate(
            sorted_list,
            headers="keys",
            tablefmt="orgtbl",
            floatfmt=".1f",
            stralign="center",
        )
        print(f"from {len(list_issued)} issuers\n{table}")


@command("argos", help="Display currency information formatted for Argos or BitBar")
def argos_info():
    head_block = HeadBlock().head_block
    currency_symbol = CurrencySymbol().symbol
    print(currency_symbol, "|")
    print("---")
    ep = determine_endpoint()
    if ep.port == 443:
        href = f"href=https://{ep.host}/"
    else:
        href = f"href=http://{ep.host}:{ep.port}/"
    current_time = from_timestamp(head_block["time"], tz="local")
    mediantime = from_timestamp(head_block["medianTime"], tz="local")
    print(
        "Connected to node:",
        ep.host,
        ep.port,
        "|",
        href,
        "\nCurrent block number:",
        head_block["number"],
        "\nCurrency name:",
        currency_symbol,
        "\nNumber of members:",
        head_block["membersCount"],
        "\nMinimal Proof-of-Work:",
        head_block["powMin"],
        "\nCurrent time:",
        current_time.format(ALL),
        "\nMedian time:",
        mediantime.format(ALL),
        "\nDifference time:",
        current_time.diff_for_humans(mediantime, True),
    )
