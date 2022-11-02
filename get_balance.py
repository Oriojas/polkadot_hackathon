from substrateinterface import SubstrateInterface


class getBalance:

    def __init__(self):
        """
        this function get balance a wallet public key
        """

        try:
            self.substrate = SubstrateInterface(
                url="wss://westend-rpc.polkadot.io",
                ss58_format=42,
                type_registry_preset='westend')

            print("😀 node running")
            self.l_n = self.substrate.get_chain_head()

        except ConnectionRefusedError:
            print("⚠️ No local Substrate node running, try running 'start_local_substrate_node.sh' first")
            exit()

    def fit(self, wallet):
        """
        this function return the balance wallet
        :param wallet:
        :return:
        """

        ln = self.l_n
        result = self.substrate.query(
            module='System',
            storage_function='Account',
            params=[wallet]
        )

        balance_off = int(result.value['data']['free'] / 10 ** 8) / 10000

        print(balance_off)

        return balance_off, ln
