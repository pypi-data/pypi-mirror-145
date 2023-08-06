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

from duniterpy.api.bma import wot

from silkaj.network_tools import ClientInstance


def identity_of(pubkey_uid):
    """
    Only works for members
    Not able to get corresponding uid from a non-member identity
    Able to know if an identity is member or not
    """
    client = ClientInstance().client
    try:
        return client(wot.identity_of, pubkey_uid)
    except ValueError as e:
        pass


def is_member(pubkey_uid):
    """
    Check identity is member
    If member, return corresponding identity, else: False
    """
    try:
        return identity_of(pubkey_uid)
    except:
        return False


def wot_lookup(identifier):
    """
    :identifier: identity or pubkey in part or whole
    Return received and sent certifications lists of matching identities
    if one identity found
    """
    client = ClientInstance().client
    return (client(wot.lookup, identifier))["results"]


def identities_from_pubkeys(pubkeys, uids):
    """
    Make list of pubkeys unique, and remove empty strings
    Request identities
    """
    if not uids:
        return list()

    uniq_pubkeys = list(filter(None, set(pubkeys)))
    identities = list()
    for pubkey in uniq_pubkeys:
        try:
            identities.append(identity_of(pubkey))
        except Exception as e:
            pass
    return identities
