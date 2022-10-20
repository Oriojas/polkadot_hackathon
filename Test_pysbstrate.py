# Python Substrate Interface Library
#
# Copyright 2018-2020 Stichting Polkascan (Polkascan Foundation).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from substrateinterface import SubstrateInterface

# # Enable for debugging purposes
# import logging
# logging.basicConfig(level=logging.DEBUG)


substrate = SubstrateInterface(
    url="wss://westend-rpc.polkadot.io",
    ss58_format=42,
    type_registry_preset='westend'
)

# Set block_hash to None for chaintip
block_hash = "0x4e85a21e7a1fe7cfcfaa4b5592830c2cd4cfeae4c9d965751b9b607f352145cd"

# Retrieve extrinsics in block
result = substrate.get_block(block_hash=block_hash)

for extrinsic in result['extrinsics']:

    if 'address' in extrinsic.value:
        signed_by_address = extrinsic.value['address']
    else:
        signed_by_address = None

    print('\nPallet: {}\nCall: {}\nSigned by: {}'.format(
        extrinsic.value["call"]["call_module"],
        extrinsic.value["call"]["call_function"],
        signed_by_address
    ))

    # Loop through call params
    for param in extrinsic.value["call"]['call_args']:

        if param['type'] == 'Balance':
            param['value'] = '{} {}'.format(param['value'] / 10 ** substrate.token_decimals, substrate.token_symbol)

        print("Param '{}': {}".format(param['name'], param['value']))