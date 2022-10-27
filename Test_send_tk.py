import os
from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

substrate = SubstrateInterface(
    url="wss://westend-rpc.polkadot.io",
    ss58_format=42,
    type_registry_preset='westend'
)

SEED = os.environ["SEED"]

keypair = Keypair.create_from_uri(SEED)

call = substrate.compose_call(
    call_module='Balances',
    call_function='transfer',
    call_params={
        'dest': '5D2fBKHgezt6pKKuXFo8Xse3sT9hZK5PtkJEyacozZJnVXZ3',
        'value': 0.1 * 10 ** 12
    }
)

extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)

try:
    receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
    print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

except SubstrateRequestException as e:
    print("Failed to send: {}".format(e))
