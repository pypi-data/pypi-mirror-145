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
from pathlib import Path

import click
from duniterpy.api import bma
from duniterpy.documents.block_id import BlockID
from duniterpy.documents.document import MalformedDocumentError
from duniterpy.documents.identity import Identity
from duniterpy.documents.revocation import Revocation
from duniterpy.key.verifying_key import VerifyingKey

from silkaj import auth, idty_tools, tui, wot
from silkaj.blockchain_tools import get_currency
from silkaj.constants import FAILURE_EXIT_STATUS, SUCCESS_EXIT_STATUS
from silkaj.network_tools import send_document

REVOCATION_LOCAL_PATH = "revocation.txt"


@click.command(
    "save",
    help="Create and save a revocation document. Optionnaly takes the document filename.",
)
@click.argument(
    "file",
    default=REVOCATION_LOCAL_PATH,
)
@click.pass_context
def save(ctx: click.core.Context, file: str):
    currency = get_currency()

    key = auth.auth_method()
    pubkey_ck = tui.display_pubkey_and_checksum(key.pubkey)
    id = (wot.choose_identity(key.pubkey))[0]
    rev_doc = create_revocation_doc(id, key.pubkey, currency)
    rev_doc.sign(key)

    if ctx.obj["DRY_RUN"]:
        click.echo(rev_doc.signed_raw())
        return SUCCESS_EXIT_STATUS

    idty_table = idty_tools.display_identity(rev_doc.identity)
    click.echo(idty_table.draw())
    if ctx.obj["DISPLAY_DOCUMENT"]:
        click.echo(rev_doc.signed_raw())

    confirm_message = "Do you want to save the revocation document for this identity?"
    if click.confirm(confirm_message):
        save_doc(file, rev_doc.signed_raw(), key.pubkey)
    else:
        click.echo("Ok, goodbye!")
        return SUCCESS_EXIT_STATUS


@click.command(
    "revoke",
    help="Create and publish revocation document. Will revoke the identity immediately.",
)
@click.pass_context
def revoke_now(ctx: click.core.Context):
    currency = get_currency()

    warn_before_dry_run_or_display(ctx)

    key = auth.auth_method()
    pubkey_ck = tui.display_pubkey_and_checksum(key.pubkey)
    id = (wot.choose_identity(key.pubkey))[0]
    rev_doc = create_revocation_doc(id, key.pubkey, currency)
    rev_doc.sign(key)

    if ctx.obj["DRY_RUN"]:
        click.echo(rev_doc.signed_raw())
        return SUCCESS_EXIT_STATUS

    idty_table = idty_tools.display_identity(rev_doc.identity)
    click.echo(idty_table.draw())
    if ctx.obj["DISPLAY_DOCUMENT"]:
        click.echo(rev_doc.signed_raw())

    warn_before_sending_document()
    send_document(bma.wot.revoke, rev_doc)


@click.command(
    "verify",
    help="Verifies that a revocation document is correctly formatted and matches an existing identity.\n\
Optionnaly takes the document filename.",
)
@click.argument(
    "file",
    default=REVOCATION_LOCAL_PATH,
)
@click.pass_context
def verify(ctx: click.core.Context, file: str):
    currency = get_currency()

    rev_doc = verify_document(file)

    if ctx.obj["DRY_RUN"]:
        click.echo(rev_doc.signed_raw())
        return SUCCESS_EXIT_STATUS

    idty_table = idty_tools.display_identity(rev_doc.identity)
    click.echo(idty_table.draw())
    if ctx.obj["DISPLAY_DOCUMENT"]:
        click.echo(rev_doc.signed_raw())

    click.echo("Revocation document is valid.")
    return SUCCESS_EXIT_STATUS


@click.command(
    "publish",
    help="Publish revocation document. Identity will be revoked immediately.\n\
Optionnaly takes the document filename.",
)
@click.argument(
    "file",
    default=REVOCATION_LOCAL_PATH,
)
@click.pass_context
def publish(ctx: click.core.Context, file: str):
    currency = get_currency()

    warn_before_dry_run_or_display(ctx)

    rev_doc = verify_document(file)
    if ctx.obj["DRY_RUN"]:
        click.echo(rev_doc.signed_raw())
        return SUCCESS_EXIT_STATUS

    idty_table = idty_tools.display_identity(rev_doc.identity)
    click.echo(idty_table.draw())
    if ctx.obj["DISPLAY_DOCUMENT"]:
        click.echo(rev_doc.signed_raw())

    warn_before_sending_document()
    send_document(bma.wot.revoke, rev_doc)


def warn_before_dry_run_or_display(ctx):
    if ctx.obj["DRY_RUN"]:
        click.echo("WARNING: the document will only be displayed and will not be sent.")


def warn_before_sending_document():
    click.secho("/!\\WARNING/!\\", blink=True, fg="red")
    click.echo(
        "This identity will be revoked.\n\
It will cease to be member and to create the Universal Dividend.\n\
All currently sent certifications will remain valid until they expire."
    )
    tui.send_doc_confirmation("revocation document immediately")


def create_revocation_doc(id, pubkey: str, currency: str):
    """
    Creates an unsigned revocation document.
    id is the dict object containing id infos from request wot.requirements
    """
    idty = Identity(
        currency=currency,
        pubkey=pubkey,
        uid=id["uid"],
        block_id=BlockID.from_str(id["meta"]["timestamp"]),
    )
    idty.signature = id["self"]
    return Revocation(
        currency=currency,
        identity=idty,
    )


def save_doc(path: str, content: str, pubkey: str):
    pubkey_cksum = tui.display_pubkey_and_checksum(pubkey)
    rev_path = Path(path)
    # Ask confirmation if the file exists
    if rev_path.is_file():
        if click.confirm(
            f"Would you like to erase existing file `{path}` with the generated revocation document corresponding to {pubkey_cksum} public key?"
        ):
            rev_path.unlink()
        else:
            click.echo("Ok, goodbye!")
            sys.exit(SUCCESS_EXIT_STATUS)
    # write doc
    with open(rev_path, "w") as file:
        file.write(content)
    click.echo(
        f"Revocation document file stored into `{path}` for following public key: {pubkey_cksum}"
    )
    return SUCCESS_EXIT_STATUS


def verify_document(doc: str):
    """
    This checks that:
      - that the revocation signature is valid.
      - if the identity is unique (warns the user)
    It returns the revocation document or exits.
    """
    error_invalid_sign = "Error: the signature of the revocation document is invalid."
    error_invalid_doc = (
        f"Error: {doc} is not a revocation document, or is not correctly formatted."
    )

    if not Path(doc).is_file():
        sys.exit(f"Error: file {doc} does not exist")
    with open(doc) as document:
        original_doc = document.read()

    try:
        rev_doc = Revocation.from_signed_raw(original_doc)
    except (MalformedDocumentError, IndexError):
        sys.exit(error_invalid_doc)

    verif_key = VerifyingKey(rev_doc.pubkey)
    if not verif_key.check_signature(rev_doc.raw(), rev_doc.signature):
        sys.exit(error_invalid_sign)

    many_idtys = idty_tools.check_many_identities(rev_doc)
    if many_idtys:
        return rev_doc
    sys.exit(FAILURE_EXIT_STATUS)
