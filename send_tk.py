import os
from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

SEED = os.environ["SEED"]


class sendTk:
    """
    this class connect and send tokens to blockchain
    """

    def __init__(self):
        """
        this function connect to blockchain westend
        """

        try:
            self.substrate = SubstrateInterface(
                url="wss://westend-rpc.polkadot.io",
                ss58_format=42,
                type_registry_preset='westend'
            )

            print("😀 last node running")

        except ConnectionRefusedError:
            print("⚠️ No local Substrate node running, try running 'start_local_substrate_node.sh' first")
            exit()

        print(f'🏃‍ Last node: {self.substrate.get_chain_head()}')

    def send(self, wallet_to_send, amount):
        """
        this function send tokens to blockchain wallet
        :param wallet_to_send: a wallet to send tokens
        :param amount: amount in WND
        :return: transfer: is True if transaction OK, else False
        """

        keypair = Keypair.create_from_uri(SEED)

        call = self.substrate.compose_call(
            call_module='Balances',
            call_function='transfer',
            call_params={
                'dest': wallet_to_send,
                'value': amount * 10 ** 12
            }
        )

        try:
            extrinsic = self.substrate.create_signed_extrinsic(call=call, keypair=keypair)
            receipt = self.substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
            print(f"🤑 Extrinsic {receipt.extrinsic_hash} sent and included in block {receipt.block_hash}")
            transfer = True

        except SubstrateRequestException as e:
            print(f"😬 Failed to send: {format(e)}")
            transfer = False

        return transfer
