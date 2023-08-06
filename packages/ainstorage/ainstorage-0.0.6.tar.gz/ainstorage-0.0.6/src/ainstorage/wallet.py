from ain.utils import privateToPublic, privateToAddress

class Wallet:
    address = None
    private_key = None
    public_key = None

    def __init__(self, private_key):
        private_key_bytes = bytes.fromhex(private_key)
        public_key_bytes = privateToPublic(private_key_bytes)

        self.address = privateToAddress(private_key_bytes)
        self.private_key = private_key_bytes.hex()
        self.public_key = public_key_bytes.hex()
