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

import logging
import sys

import click
import pendulum
from duniterpy.api import bma
from duniterpy.documents import BlockID, Membership, get_block_id
from tabulate import tabulate

from silkaj import auth, tui, wot
from silkaj.blockchain_tools import BlockchainParams, HeadBlock
from silkaj.constants import DATE, SUCCESS_EXIT_STATUS
from silkaj.license import license_approval
from silkaj.network_tools import ClientInstance, send_document


@click.command(
    "membership",
    help="Send and sign membership document: \n\
for first emission and for renewal",
)
@click.pass_context
def send_membership(ctx):
    dry_run = ctx.obj["DRY_RUN"]

    # Authentication
    key = auth.auth_method()

    # Get the identity information
    head_block = HeadBlock().head_block
    membership_block_id = BlockID(head_block["number"], head_block["hash"])
    identity = (wot.choose_identity(key.pubkey))[0]
    identity_uid = identity["uid"]
    identity_block_id = get_block_id(identity["meta"]["timestamp"])

    # Display license and ask for confirmation
    currency = head_block["currency"]
    if not dry_run:
        license_approval(currency)

    # Confirmation
    client = ClientInstance().client
    display_confirmation_table(identity_uid, key.pubkey, identity_block_id)
    if not dry_run and not ctx.obj["DISPLAY_DOCUMENT"]:
        tui.send_doc_confirmation("membership document for this identity")

    # Create and sign membership document
    membership = generate_membership_document(
        key.pubkey,
        membership_block_id,
        identity_uid,
        identity_block_id,
        currency,
        key,
    )

    logging.debug(membership.signed_raw())

    if dry_run:
        click.echo(membership.signed_raw())
        sys.exit(SUCCESS_EXIT_STATUS)

    if ctx.obj["DISPLAY_DOCUMENT"]:
        click.echo(membership.signed_raw())
        tui.send_doc_confirmation("membership document for this identity")

    # Send the membership signed raw document to the node
    send_document(bma.blockchain.membership, membership)


def display_confirmation_table(identity_uid, pubkey, identity_block_id):
    """
    Check whether there is pending memberships already in the mempool
    Display their expiration date

    Actually, it works sending a membership document even if the time
    between two renewals is not awaited as for the certification
    """

    client = ClientInstance().client

    identities_requirements = client(bma.wot.requirements, pubkey)
    for identity_requirements in identities_requirements["identities"]:
        if identity_requirements["uid"] == identity_uid:
            membership_expires = identity_requirements["membershipExpiresIn"]
            pending_expires = identity_requirements["membershipPendingExpiresIn"]
            pending_memberships = identity_requirements["pendingMemberships"]
            break

    table = list()
    if membership_expires:
        expires = pendulum.now().add(seconds=membership_expires).diff_for_humans()
        table.append(["Expiration date of current membership", expires])

    if pending_memberships:
        line = [
            "Number of pending membership(s) in the mempool",
            len(pending_memberships),
        ]
        table.append(line)

        expiration = pendulum.now().add(seconds=pending_expires).diff_for_humans()
        table.append(["Pending membership documents will expire", expiration])

    table.append(["User Identifier (UID)", identity_uid])
    table.append(["Public Key", tui.display_pubkey_and_checksum(pubkey)])

    table.append(["Block Identity", str(identity_block_id)[:45] + "…"])

    block = client(bma.blockchain.block, identity_block_id.number)
    date_idty_pub = pendulum.from_timestamp(block["time"], tz="local").format(DATE)
    table.append(["Identity published", date_idty_pub])

    params = BlockchainParams().params
    membership_validity = (
        pendulum.now().add(seconds=params["msValidity"]).diff_for_humans()
    )
    table.append(["Expiration date of new membership", membership_validity])

    membership_mempool = (
        pendulum.now().add(seconds=params["msPeriod"]).diff_for_humans()
    )
    table.append(
        ["Expiration date of new membership from the mempool", membership_mempool]
    )

    click.echo(tabulate(table, tablefmt="fancy_grid"))


def generate_membership_document(
    pubkey,
    membership_block_id,
    identity_uid,
    identity_block_id,
    currency,
    key=None,
):
    return Membership(
        issuer=pubkey,
        membership_block_id=membership_block_id,
        uid=identity_uid,
        identity_block_id=identity_block_id,
        currency=currency,
        signing_key=key,
    )
