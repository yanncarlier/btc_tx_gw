'''
Generates Taproot (P2TR) addresses using BIP86, an implementation of Segregated Witness (BIP141) with Schnorr signatures (BIP340).
BIP86 specifies the derivation path m/86'/0'/0'/0/i for Taproot addresses.
'''
from bip_utils import (
    Bip39SeedGenerator,
    Bip39MnemonicValidator,
    Bip86,
    Bip86Coins,
    Bip44Changes
)
from bip_utils.utils.mnemonic import MnemonicChecksumError

# Example BIP39 mnemonic seed phrase
mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
passphrase = ""  # Optional passphrase (default is empty string; can be changed by user)

try:
    # Validate the mnemonic phrase
    if not Bip39MnemonicValidator().IsValid(mnemonic):
        raise ValueError("Invalid mnemonic phrase provided. Please check the words and try again.")
    
    print("Mnemonic Phrase:", mnemonic)
    print("Passphrase:", passphrase if passphrase else "<empty>")

    # Generate seed from mnemonic with passphrase
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase=passphrase)

    # Display the generated seed (in hex)
    print("Seed (hex):", seed_bytes.hex())

    # Initialize BIP86 for Bitcoin mainnet and derive the default account (m/86'/0'/0')
    bip86_mst_ctx = Bip86.FromSeed(seed_bytes, Bip86Coins.BITCOIN)
    bip86_acc_ctx = bip86_mst_ctx.Purpose().Coin().Account(0)

    # Generate a set number of BIP86 addresses (Taproot, enabled by BIP341)
    num_addresses = 1  # Adjustable for more addresses
    print("Generating Taproot (P2TR) Addresses via BIP86:")

    for i in range(num_addresses):
        # Derive the external chain and address at index i
        bip86_chg_ctx = bip86_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
        bip86_addr_ctx = bip86_chg_ctx.AddressIndex(i)

        # Construct derivation path manually (BIP86: m/86'/0'/0'/0/i)
        derivation_path = f"m/86'/0'/0'/0/{i}"

             # Print the BIP32 Extended Public Key (xpub) when i == 0
        if i == 0:
            bip32_xpub = bip86_chg_ctx.PublicKey().ToExtended()
            print("BIP32 Extended Public Key (xpub):", bip32_xpub)
               
        address = bip86_addr_ctx.PublicKey().ToAddress()  # Taproot address (starts with 'bc1p')
        public_key = bip86_addr_ctx.PublicKey().RawCompressed().ToHex()  # Compressed public key in hex
        private_key = bip86_addr_ctx.PrivateKey().Raw().ToHex()  # Private key in hex
        wif = bip86_addr_ctx.PrivateKey().ToWif()  # Private key in WIF format

        # Output in a structured format
        print("{")
        print(f"derivation_path: {derivation_path}")
        print(f"address: {address}")
        print(f"public_key: {public_key}")
        print(f"private_key: {private_key}")
        print(f"wif: {wif}")
        print("},")

except MnemonicChecksumError as e:
    print(f"Error: Invalid mnemonic checksum. Details: {e}")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")