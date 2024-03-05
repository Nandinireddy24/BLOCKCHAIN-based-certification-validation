class Block:
    def __init__(self, index, previous_hash, transactions, timestamp, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Your hash calculation logic here
        pass
