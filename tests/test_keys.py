# This file is part of Maker Keeper Framework.
#
# Copyright (C) 2017-2018 reverendus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pkg_resources
from web3 import Web3, HTTPProvider

from pymaker import Address, Wad, eth_transfer
from pymaker.keys import register_key
from pymaker.token import DSToken


def test_local_accounts():
    # given
    # [that address is not recognized by ganache, this way we can be sure it's the local account being used for signing]
    web3 = Web3(HTTPProvider("http://localhost:8555"))
    web3.eth.defaultAccount = Address('0x13314e21cd6d343ceb857073f3f6d9368919d1ef').address

    # and
    keyfile_path = pkg_resources.resource_filename(__name__, "accounts/4_0x13314e21cd6d343ceb857073f3f6d9368919d1ef.json")
    passfile_path = pkg_resources.resource_filename(__name__, "accounts/pass")
    register_key(web3, keyfile_path, passfile_path)

    # and
    # [as ganache does not know this address, we need to send some ETH to it first]
    eth_transfer(web3, Address(web3.eth.defaultAccount), Wad.from_number(100)) \
        .transact(from_address=Address(web3.eth.accounts[0]))

    # when
    # [we deploy some test contract and mint some tokens]
    token = DSToken.deploy(web3, 'XYZ')
    token.mint(Wad.from_number(150000)).transact()

    # then
    # [these operations were successful]
    assert token.balance_of(Address(web3.eth.defaultAccount)) == Wad.from_number(150000)
