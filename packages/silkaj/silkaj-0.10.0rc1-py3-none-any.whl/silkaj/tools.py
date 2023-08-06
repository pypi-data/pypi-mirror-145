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

from sys import exit

from silkaj.blockchain_tools import BlockchainParams
from silkaj.constants import FAILURE_EXIT_STATUS, G1_SYMBOL, GTEST_SYMBOL


class CurrencySymbol:
    __instance = None

    def __new__(cls):
        if CurrencySymbol.__instance is None:
            CurrencySymbol.__instance = object.__new__(cls)
        return CurrencySymbol.__instance

    def __init__(self):
        self.symbol = self.get_symbol()

    def get_symbol(self):
        params = BlockchainParams().params
        if params["currency"] == "g1":
            return G1_SYMBOL
        elif params["currency"] == "g1-test":
            return GTEST_SYMBOL


def message_exit(message):
    print(message)
    exit(FAILURE_EXIT_STATUS)
