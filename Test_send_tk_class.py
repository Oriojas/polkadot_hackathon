from send_tk import sendTk

w_to_send = '5D2fBKHgezt6pKKuXFo8Xse3sT9hZK5PtkJEyacozZJnVXZ3'
amount = 0.1

tx = sendTk().send(wallet_to_send=w_to_send, amount=amount)

print(f'Tx is: {tx}')
