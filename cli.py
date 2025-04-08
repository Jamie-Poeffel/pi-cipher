import argparse
from pi_cipher import cipher

def main():
    parser = argparse.ArgumentParser(description="Pi Cipher Verschlüsselungstool")
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Modus: encrypt oder decrypt")
    parser.add_argument("message", help="Die Nachricht, die ver- oder entschlüsselt werden soll")

    args = parser.parse_args()

    if args.mode == "encrypt":
        encrypted = cipher.encrypt(args.message)
        print("Verschlüsselte Nachricht:", encrypted)
    else:
        decrypted = cipher.decrypt(args.message)
        print("Entschlüsselte Nachricht:", decrypted)

if __name__ == "__main__":
    main()
