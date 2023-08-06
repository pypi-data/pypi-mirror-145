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

import urllib
from collections import OrderedDict

import click
from duniterpy.api.bma import blockchain, wot
from duniterpy.api.errors import DuniterError
from pendulum import from_timestamp, now
from tabulate import tabulate

from silkaj import wot_tools as wt
from silkaj.blockchain_tools import BlockchainParams
from silkaj.constants import DATE
from silkaj.crypto_tools import is_pubkey_and_check
from silkaj.network_tools import ClientInstance, exit_on_http_error
from silkaj.tools import message_exit
from silkaj.tui import display_pubkey_and_checksum


def get_sent_certifications(signed, time_first_block, params):
    sent = list()
    expire = list()
    if signed:
        for cert in signed:
            sent.append(cert["uid"])
            expire.append(
                expiration_date_from_block_id(
                    cert["cert_time"]["block"], time_first_block, params
                )
            )
    return sent, expire


@click.command(
    "wot",
    help="Check received and sent certifications and consult the membership status of any given identity",
)
@click.argument("uid_pubkey")
def received_sent_certifications(uid_pubkey):
    """
    get searched id
    get id of received and sent certifications
    display in a table the result with the numbers
    """
    client = ClientInstance().client
    first_block = client(blockchain.block, 1)
    time_first_block = first_block["time"]

    checked_pubkey = is_pubkey_and_check(uid_pubkey)
    if checked_pubkey:
        uid_pubkey = checked_pubkey

    identity, pubkey, signed = choose_identity(uid_pubkey)
    certifications = OrderedDict()
    params = BlockchainParams().params
    requirements = client(wot.requirements, pubkey)
    for req in requirements["identities"]:
        if req["pubkey"] == pubkey:
            break
    certifications["received_expire"] = list()
    certifications["received"] = list()
    for cert in identity["others"]:
        certifications["received_expire"].append(
            expiration_date_from_block_id(
                cert["meta"]["block_number"], time_first_block, params
            )
        )
        certifications["received"].append(
            cert_written_in_the_blockchain(req["certifications"], cert)
        )
        (
            certifications["sent"],
            certifications["sent_expire"],
        ) = get_sent_certifications(signed, time_first_block, params)
    nbr_sent_certs = len(certifications["sent"]) if "sent" in certifications else 0
    table = tabulate(
        certifications, headers="keys", tablefmt="orgtbl", stralign="right"
    )
    txt = f'{identity["uid"]} ({display_pubkey_and_checksum(pubkey, True)}) \
from block #{identity["meta"]["timestamp"][:15]}…\n\
received {len(certifications["received"])} and sent {nbr_sent_certs}/{params["sigStock"]} certifications:\n\
{table}\n\
✔: Certification available to be written or already written into the blockchain\n'
    print(txt)
    membership_status(certifications, pubkey, req)


def cert_written_in_the_blockchain(written_certs, certifieur):
    for cert in written_certs:
        if cert["from"] == certifieur["pubkey"]:
            return certifieur["uids"][0] + " ✔"
    return certifieur["uids"][0]


def membership_status(certifications, pubkey, req):
    params = BlockchainParams().params
    if len(certifications["received"]) >= params["sigQty"]:
        date = certifications["received_expire"][
            len(certifications["received"]) - params["sigQty"]
        ]
        print(f"Membership expiration due to certification expirations: {date}")
    member = wt.is_member(pubkey)
    if member:
        member = True
    print("member:", member)
    if req["revoked"]:
        revoke_date = from_timestamp(req["revoked_on"], tz="local").format(DATE)
        print(f"revoked: {req['revoked']}\nrevoked on: {revoke_date}")
    if not member and req["wasMember"]:
        print("expired:", req["expired"], "\nwasMember:", req["wasMember"])
    elif member:
        expiration_date = now().add(seconds=req["membershipExpiresIn"]).format(DATE)
        print(f"Membership document expiration: {expiration_date}")
        print("Sentry:", req["isSentry"])
    print("outdistanced:", req["outdistanced"])


def expiration_date_from_block_id(block_id, time_first_block, params):
    expir_timestamp = (
        date_approximation(block_id, time_first_block, params["avgGenTime"])
        + params["sigValidity"]
    )
    return from_timestamp(expir_timestamp, tz="local").format(DATE)


def date_approximation(block_id, time_first_block, avgentime):
    return time_first_block + block_id * avgentime


@click.command("lookup", help="User identifier and public key lookup")
@click.argument("uid_pubkey")
def id_pubkey_correspondence(uid_pubkey):
    checked_pubkey = is_pubkey_and_check(uid_pubkey)
    if checked_pubkey:
        uid_pubkey = checked_pubkey

    try:
        lookups = wt.wot_lookup(uid_pubkey)
    except urllib.error.HTTPError as e:
        exit_on_http_error(e, 404, f"No identity found for {uid_pubkey}")

    content = f"Public keys or user id found matching '{uid_pubkey}':\n"
    for lookup in lookups:
        for identity in lookup["uids"]:
            pubkey_checksum = display_pubkey_and_checksum(lookup["pubkey"])
            content += f'\n→ {pubkey_checksum} ↔ {identity["uid"]}'
    click.echo(content)


def choose_identity(pubkey_uid):
    """
    Get lookup from a pubkey or an uid
    Loop over the double lists: pubkeys, then uids
    If there is one uid, returns it
    If there is multiple uids, prompt a selector
    """

    try:
        lookups = wt.wot_lookup(pubkey_uid)
    except urllib.error.HTTPError as e:
        exit_on_http_error(e, 404, f"No identity found for {pubkey_uid}")

    # Generate table containing the choices
    identities_choices = {"id": [], "uid": [], "pubkey": [], "timestamp": []}
    for pubkey_index, lookup in enumerate(lookups):
        for uid_index, identity in enumerate(lookup["uids"]):
            identities_choices["id"].append(str(pubkey_index) + str(uid_index))
            identities_choices["pubkey"].append(
                display_pubkey_and_checksum(lookup["pubkey"])
            )
            identities_choices["uid"].append(identity["uid"])
            identities_choices["timestamp"].append(
                identity["meta"]["timestamp"][:20] + "…"
            )

    identities = len(identities_choices["uid"])
    if identities == 1:
        pubkey_index = 0
        uid_index = 0
    elif identities > 1:
        table = tabulate(identities_choices, headers="keys", tablefmt="orgtbl")
        click.echo(table)

        # Loop till the passed value is in identities_choices
        message = "Which identity would you like to select (id)?"
        selected_id = None
        while selected_id not in identities_choices["id"]:
            selected_id = click.prompt(message)

        pubkey_index = int(selected_id[:-1])
        uid_index = int(selected_id[-1:])

    return (
        lookups[pubkey_index]["uids"][uid_index],
        lookups[pubkey_index]["pubkey"],
        lookups[pubkey_index]["signed"],
    )
