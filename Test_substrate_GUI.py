from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

# conexion local con un no de kusama
try:
    substrate = SubstrateInterface(
        # url="wss://kusama-rpc.polkadot.io/",
        url="http://127.0.0.1:9933/",
        ss58_format=2,
        type_registry_preset='kusama'
    )

    print("😀 local Substrate node running")

except ConnectionRefusedError:
    print("⚠️ No local Substrate node running, try running 'start_local_substrate_node.sh' first")
    exit()

print(f'🏃‍ Last node: {substrate.get_chain_head()}')

keypair_a = Keypair.create_from_uri('//Alice')
keypair_b = Keypair.create_from_uri('//Bob')

print(f'Alice: {keypair_a}')
print(f'Bob: {keypair_b}')

tk_value = 3

# para dar algo de tokens a la cuenta de Bob
balance_call = substrate.compose_call(
    call_module='Balances',
    call_function='transfer',
    call_params={
        'dest': keypair_b.ss58_address,
        'value': tk_value * 10**15
    }
)

print(f"Bob's balance: {balance_call.value.get('call_args').get('value')}")

# llamada para confirmar el balance
call = substrate.compose_call(
    call_module='Utility',
    call_function='batch',
    call_params={
        'calls': [balance_call, balance_call]
    }
)

# Get payment info
#payment_info = substrate.get_payment_info(call=call, keypair=keypair_b)

#print("Payment info: ", payment_info)

extrinsic = substrate.create_signed_extrinsic(
    call=call,
    keypair=keypair_b,
    era={'period': 64}
)

#print(extrinsic)

try:
    receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)

    print('Extrinsic "{}" included in block "{}"'.format(
        receipt.extrinsic_hash, receipt.block_hash
    ))

    if receipt.is_success:

        print('✅ Success, triggered events:')
        for event in receipt.triggered_events:
            print(f'* {event.value}')

    else:
        print('⚠️ Extrinsic Failed: ', receipt.error_message)


except SubstrateRequestException as e:
    print("Failed to send: {}".format(e))
