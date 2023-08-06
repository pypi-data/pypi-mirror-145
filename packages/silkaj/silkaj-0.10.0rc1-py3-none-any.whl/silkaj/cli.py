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

from click import group, help_option, option, pass_context, version_option
from duniterpy.api.endpoint import endpoint

from silkaj import revocation
from silkaj.auth import generate_auth_file
from silkaj.blocks import verify_blocks_signatures
from silkaj.cert import send_certification
from silkaj.checksum import checksum_command
from silkaj.commands import argos_info, currency_info, difficulties, list_blocks
from silkaj.constants import (
    G1_DEFAULT_ENDPOINT,
    G1_TEST_DEFAULT_ENDPOINT,
    SILKAJ_VERSION,
)
from silkaj.license import license_command
from silkaj.membership import send_membership
from silkaj.money import cmd_amount
from silkaj.tx import send_transaction
from silkaj.tx_history import transaction_history
from silkaj.wot import id_pubkey_correspondence, received_sent_certifications


@group()
@help_option("-h", "--help")
@version_option(SILKAJ_VERSION, "-v", "--version")
@option(
    "--endpoint",
    "-ep",
    help=f"Default endpoint to reach Ğ1 currency by its official node {endpoint(G1_DEFAULT_ENDPOINT).host}\
 This option allows to specify a custom endpoint as follow: <host>:<port>.\
 In case no port is specified, it defaults to 443.",
)
@option(
    "--gtest",
    "-gt",
    is_flag=True,
    help=f"Default endpoint to reach ĞTest currency by its official node: {endpoint(G1_TEST_DEFAULT_ENDPOINT).host}",
)
@option(
    "--auth-scrypt",
    "--scrypt",
    is_flag=True,
    help="Scrypt authentication: default method",
)
@option("--nrp", help='Scrypt parameters: defaults N,r,p: "4096,16,1"')
@option(
    "--auth-file",
    "-af",
    is_flag=True,
    help="Authentication file. Defaults to: './authfile'",
)
@option(
    "--file",
    default="authfile",
    show_default=True,
    help="Path file specification with '--auth-file'",
)
@option("--auth-seed", "--seed", is_flag=True, help="Seed hexadecimal authentication")
@option("--auth-wif", "--wif", is_flag=True, help="WIF and EWIF authentication methods")
@option(
    "--display",
    "-d",
    is_flag=True,
    help="Display the generated document before sending it",
)
@option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="By-pass licence, confirmation. \
Do not send the document, but display it instead",
)
@pass_context
def cli(
    ctx,
    endpoint,
    gtest,
    auth_scrypt,
    nrp,
    auth_file,
    file,
    auth_seed,
    auth_wif,
    display,
    dry_run,
):
    if display and dry_run:
        sys.exit("ERROR: display and dry-run options can not be used together")

    ctx.obj = dict()
    ctx.ensure_object(dict)
    ctx.obj["ENDPOINT"] = endpoint
    ctx.obj["GTEST"] = gtest
    ctx.obj["AUTH_SCRYPT"] = auth_scrypt
    ctx.obj["AUTH_SCRYPT_PARAMS"] = nrp
    ctx.obj["AUTH_FILE"] = auth_file
    ctx.obj["AUTH_FILE_PATH"] = file
    ctx.obj["AUTH_SEED"] = auth_seed
    ctx.obj["AUTH_WIF"] = auth_wif
    ctx.obj["DISPLAY_DOCUMENT"] = display
    ctx.obj["DRY_RUN"] = dry_run


cli.add_command(argos_info)
cli.add_command(generate_auth_file)
cli.add_command(cmd_amount)
cli.add_command(list_blocks)
cli.add_command(send_certification)
cli.add_command(checksum_command)
cli.add_command(difficulties)
cli.add_command(transaction_history)
cli.add_command(id_pubkey_correspondence)
cli.add_command(currency_info)
cli.add_command(license_command)
cli.add_command(send_membership)
cli.add_command(send_transaction)
cli.add_command(verify_blocks_signatures)
cli.add_command(received_sent_certifications)


@cli.group(
    "revocation",
    help="Create, save, verify or publish revocation document.\n\
Subcommands optionally take the path to the revocation document.",
)
@help_option("-h", "--help")
def revocation_group():
    pass


revocation_group.add_command(revocation.save)
revocation_group.add_command(revocation.verify)
revocation_group.add_command(revocation.publish)
revocation_group.add_command(revocation.revoke_now)


@cli.command("about", help="Display program information")
def about():
    print(
        "\
\n             @@@@@@@@@@@@@\
\n         @@@     @         @@@\
\n      @@@   @@       @@@@@@   @@.            Silkaj",
        SILKAJ_VERSION,
        "\
\n     @@  @@@       @@@@@@@@@@@  @@,\
\n   @@  @@@       &@@@@@@@@@@@@@  @@@         Powerfull and lightweight command line client\
\n  @@  @@@       @@@@@@@@@#   @@@@ @@(\
\n  @@ @@@@      @@@@@@@@@      @@@  @@        Built in Python for Duniter’s currencies: Ğ1 and Ğ1-Test\
\n @@  @@@      @@@@@@@@ @       @@@  @@\
\n @@  @@@      @@@@@@ @@@@       @@  @@       Authors: see AUTHORS.md file\
\n @@  @@@@      @@@ @@@@@@@      @@  @@\
\n  @@ @@@@*       @@@@@@@@@      @# @@        Website: https://silkaj.duniter.org\
\n  @@  @@@@@    @@@@@@@@@@       @ ,@@\
\n   @@  @@@@@ @@@@@@@@@@        @ ,@@         Repository: https://git.duniter.org/clients/python/silkaj\
\n    @@@  @@@@@@@@@@@@        @  @@*\
\n      @@@  @@@@@@@@        @  @@@            License: GNU AGPLv3\
\n        @@@@   @@          @@@,\
\n            @@@@@@@@@@@@@@@\n",
    )
