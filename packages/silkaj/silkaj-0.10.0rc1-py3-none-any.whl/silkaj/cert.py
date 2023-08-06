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

import click
from duniterpy.api import bma
from duniterpy.documents import BlockID, Certification, Identity, get_block_id
from pendulum import from_timestamp, now
from tabulate import tabulate

from silkaj import tui, wot
from silkaj import wot_tools as wt
from silkaj.auth import auth_method
from silkaj.blockchain_tools import BlockchainParams, HeadBlock
from silkaj.constants import ALL, DATE, SUCCESS_EXIT_STATUS
from silkaj.crypto_tools import is_pubkey_and_check
from silkaj.license import license_approval
from silkaj.network_tools import ClientInstance, send_document


@click.command("cert", help="Send certification")
@click.argument("uid_pubkey_to_certify")
@click.pass_context
def send_certification(ctx, uid_pubkey_to_certify):
    client = ClientInstance().client

    checked_pubkey = is_pubkey_and_check(uid_pubkey_to_certify)
    if checked_pubkey:
        uid_pubkey_to_certify = checked_pubkey

    idty_to_certify, pubkey_to_certify, send_certs = wot.choose_identity(
        uid_pubkey_to_certify
    )

    # Authentication
    key = auth_method()

    issuer_pubkey = key.pubkey
    issuer = pre_checks(client, issuer_pubkey, pubkey_to_certify)

    # Display license and ask for confirmation
    head = HeadBlock().head_block
    currency = head["currency"]
    license_approval(currency)

    # Certification confirmation
    certification_confirmation(
        ctx, issuer, issuer_pubkey, pubkey_to_certify, idty_to_certify
    )

    # Create and sign certification document
    certification = docs_generation(
        currency,
        pubkey_to_certify,
        idty_to_certify,
        issuer_pubkey,
        head,
        key,
    )

    if ctx.obj["DISPLAY_DOCUMENT"]:
        click.echo(certification.signed_raw(), nl=False)
        tui.send_doc_confirmation("certification")

    # Send certification document
    send_document(bma.wot.certify, certification)


def pre_checks(client, issuer_pubkey, pubkey_to_certify):
    # Check whether current user is member
    issuer = wt.is_member(issuer_pubkey)
    if not issuer:
        sys.exit("Current identity is not member.")

    if issuer_pubkey == pubkey_to_certify:
        sys.exit("You can’t certify yourself!")

    # Check if the certification can be renewed
    req = client(bma.wot.requirements, pubkey_to_certify)
    req = req["identities"][0]
    for cert in req["certifications"]:
        if cert["from"] == issuer_pubkey:
            params = BlockchainParams().params
            # Ğ1: 0<–>2y - 2y + 2m
            # ĞT: 0<–>4.8m - 4.8m + 12.5d
            renewable = cert["expiresIn"] - params["sigValidity"] + params["sigReplay"]
            if renewable > 0:
                renewable_date = now().add(seconds=renewable).format(DATE)
                sys.exit(f"Certification renewable from {renewable_date}")

    # Check if the certification is already in the pending certifications
    for pending_cert in req["pendingCerts"]:
        if pending_cert["from"] == issuer_pubkey:
            sys.exit("Certification is currently being processed")
    return issuer


def certification_confirmation(
    ctx, issuer, issuer_pubkey, pubkey_to_certify, idty_to_certify
):
    cert = list()
    cert.append(["Cert", "Issuer", "–>", "Recipient: Published: #block-hash date"])
    client = ClientInstance().client
    idty_timestamp = idty_to_certify["meta"]["timestamp"]
    block_id_idty = get_block_id(idty_timestamp)
    block = client(bma.blockchain.block, block_id_idty.number)
    timestamp_date = from_timestamp(block["time"], tz="local").format(ALL)
    block_id_date = f": #{idty_timestamp[:15]}… {timestamp_date}"
    cert.append(["ID", issuer["uid"], "–>", idty_to_certify["uid"] + block_id_date])
    cert.append(
        [
            "Pubkey",
            tui.display_pubkey_and_checksum(issuer_pubkey),
            "–>",
            tui.display_pubkey_and_checksum(pubkey_to_certify),
        ]
    )
    params = BlockchainParams().params
    cert_begins = now().format(DATE)
    cert_ends = now().add(seconds=params["sigValidity"]).format(DATE)
    cert.append(["Valid", cert_begins, "—>", cert_ends])
    click.echo(tabulate(cert, tablefmt="fancy_grid"))
    if not ctx.obj["DISPLAY_DOCUMENT"]:
        tui.send_doc_confirmation("certification")


def docs_generation(
    currency, pubkey_to_certify, idty_to_certify, issuer_pubkey, head, key
):
    identity = Identity(
        pubkey=pubkey_to_certify,
        uid=idty_to_certify["uid"],
        block_id=get_block_id(idty_to_certify["meta"]["timestamp"]),
        currency=currency,
    )
    identity.signature = idty_to_certify["self"]

    return Certification(
        pubkey_from=issuer_pubkey,
        identity=identity,
        block_id=BlockID(head["number"], head["hash"]),
        signing_key=key,
        currency=currency,
    )
