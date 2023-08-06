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

from click import INT, argument, command, progressbar
from duniterpy.api import bma
from duniterpy.api.client import Client
from duniterpy.api.errors import DuniterError
from duniterpy.documents import Block
from duniterpy.key.verifying_key import VerifyingKey

from silkaj.constants import BMA_MAX_BLOCKS_CHUNK_SIZE
from silkaj.network_tools import determine_endpoint
from silkaj.tools import message_exit


@command(
    "verify",
    help="Verify blocks’ signatures. \
If only FROM_BLOCK is specified, it verifies from this block to the last block. \
If nothing specified, the whole blockchain gets verified.",
)
@argument("from_block", default=0, type=INT)
@argument("to_block", default=0, type=INT)
def verify_blocks_signatures(from_block, to_block):
    client = Client(determine_endpoint())
    to_block = check_passed_blocks_range(client, from_block, to_block)
    invalid_blocks_signatures = list()
    chunks_from = range(from_block, to_block + 1, BMA_MAX_BLOCKS_CHUNK_SIZE)
    with progressbar(chunks_from, label="Processing blocks verification") as bar:
        for chunk_from in bar:
            chunk_size = get_chunk_size(from_block, to_block, chunks_from, chunk_from)
            logging.info(
                f"Processing chunk from block {chunk_from} to {chunk_from + chunk_size}"
            )
            chunk = get_chunk(client, chunk_size, chunk_from)

            for block in chunk:
                block = Block.from_signed_raw(f'{block["raw"]}{block["signature"]}\n')
                verify_block_signature(invalid_blocks_signatures, block)

    display_result(from_block, to_block, invalid_blocks_signatures)


def check_passed_blocks_range(client, from_block, to_block):
    head_number = (client(bma.blockchain.current))["number"]
    if to_block == 0:
        to_block = head_number
    if to_block > head_number:
        message_exit(
            f"Passed TO_BLOCK argument is bigger than the head block: {str(head_number)}"
        )
    if from_block > to_block:
        message_exit("TO_BLOCK should be bigger or equal to FROM_BLOCK")
    return to_block


def get_chunk_size(from_block, to_block, chunks_from, chunk_from):
    """If not last chunk, take the maximum size
    Otherwise, calculate the size for the last chunk"""
    if chunk_from != chunks_from[-1]:
        return BMA_MAX_BLOCKS_CHUNK_SIZE
    else:
        return (to_block + 1 - from_block) % BMA_MAX_BLOCKS_CHUNK_SIZE


def get_chunk(client, chunk_size, chunk_from):
    try:
        return client(bma.blockchain.blocks, chunk_size, chunk_from)
    except DuniterError as error:
        logging.error(error)


def verify_block_signature(invalid_blocks_signatures, block):
    if not block.check_signature(block.issuer):
        invalid_blocks_signatures.append(block.number)


def display_result(from_block, to_block, invalid_blocks_signatures):
    result = f"Within {from_block}-{to_block} range, "
    if invalid_blocks_signatures:
        result += "blocks with a wrong signature: "
        result += " ".join(str(n) for n in invalid_blocks_signatures)
    else:
        result += "no blocks with a wrong signature."
    print(result)
