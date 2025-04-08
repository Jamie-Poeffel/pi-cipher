import argparse
from pi_cipher import encrypt, decrypt

def main():
    parser = argparse.ArgumentParser(description="Pi Cipher v3.0 - Quantum Ready Kryptotool")
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Modus: encrypt oder decrypt")
    parser.add_argument("message", help="Nachricht zum Ver- oder Entschlüsseln")

    args = parser.parse_args()

    if args.mode == "encrypt":
        print("Verschlüsselte Nachricht:\n", encrypt(args.message))
    elif args.mode == "decrypt":
        print("Entschlüsselte Nachricht:\n", decrypt(args.message))

if __name__ == "__main__":
    main()