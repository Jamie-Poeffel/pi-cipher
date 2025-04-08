# Pi Cipher v2.0

<p align="center">
  <img src="logo.svg" width="200" alt="Pi Cipher Logo">
</p>

Quantum Ready Verschlüsselungstool mit Dummy-Daten, Redundanz, kryptosicherer Zufall und Integritätsprüfung.

## Features

- Quantum-Safe Startoffset (128 Bit)
- Kombinierte mathematische Konstanten (Pi, e, Phi)
- Zufällige Gruppenreihenfolge & Dummy-Padding
- Redundanz + Fehlerkorrektur
- Optionaler Integritätscheck
- Open Source & PyPI ready

## Installation

```bash
git clone https://github.com/dein-user/pi_cipher.git
cd pi_cipher
pip install .
```

## Nutzung

### CLI

```bash
pi-cipher encrypt "HELLO WORLD"
pi-cipher decrypt "deine_verschlüsselte_nachricht"
```

### Als Python Library

```python
from pi_cipher import encrypt, decrypt

encrypted = encrypt("HELLO WORLD")
print(encrypted)

decrypted = decrypt(encrypted)
print(decrypted)
```

## Lizenz

MIT License
