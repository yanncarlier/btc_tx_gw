'''
Generates Native SegWit (P2WPKH) Addresses.
BIP44 (Legacy P2PKH, among others) uses 44'.
'''
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicValidator
from bip_utils.utils.mnemonic import MnemonicChecksumError

# Example BIP39 mnemonic seed phrase
mnemonic = "caution blush hill vintage park empower coin mystery earth unaware control fault"
passphrase = ""  # Optional passphrase (default is empty string; can be changed by user)

try:
    # Initialize Mnemonic object for English wordlist
    # mnemo = Mnemonic("english")

    # Validate the mnemonic phrase
    if not Bip39MnemonicValidator().IsValid(mnemonic):
        raise ValueError("Invalid mnemonic phrase provided. Please check the words and try again.")
    
    print("Mnemonic Phrase:", mnemonic)
    print("Passphrase:", passphrase if passphrase else "<empty>")

    # Generate seed from mnemonic with passphrase
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase=passphrase)

    # Display the generated seed (in hex)
    print("Seed (hex):", seed_bytes.hex())

    # Initialize BIP44 for Bitcoin mainnet and derive the default account (m/44'/0'/0')
    print("Generating Native SegWit (P2WPKH) Addresses:")

    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)

    # Generate a set number of addresses
    num_addresses = 1  # Number of addresses to generate
    for i in range(num_addresses):
        # Derive the external chain and address at index i
        bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
        bip44_addr_ctx = bip44_chg_ctx.AddressIndex(i)

        # Construct the derivation path manually (m/44'/0'/0'/0/i)
        derivation_path = f"m/44'/0'/0'/0/{i}"

        # Extract required information
        address = bip44_addr_ctx.PublicKey().ToAddress()  # Bitcoin address
        public_key = bip44_addr_ctx.PublicKey().RawCompressed().ToHex()  # Public key in hex
        private_key = bip44_addr_ctx.PrivateKey().ToWif()  # Private key in WIF format

        # Print the output in the specified order
        print("{")
        print(f"derivation_path: {derivation_path}")
        print(f"address: {address}")
        print(f"public_key: {public_key}")
        print(f"private_key: {private_key}")
        print("},")

except MnemonicChecksumError as e:
    print(f"Error: Invalid mnemonic checksum. Details: {e}")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")