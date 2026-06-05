# CipherCLI

A command-line cipher tool built in Python as a personal project to explore classical cryptography and algorithm implementation.

## Features

- **Caesar cipher** — encrypt, decrypt, and brute-force with automatic English frequency scoring
- **Vigenere cipher** — keyword-based polyalphabetic encryption and decryption
- **ROT13** — one-step classic transform (its own inverse)
- **Frequency analysis** — scores all 25 brute-force outputs against English letter distributions and ranks them, so the most likely decryption appears first
- **File mode** — encrypt or decrypt any `.txt` file directly from the terminal
- **Coloured output** — no external libraries, pure ANSI
- **Session logging** — every operation is timestamped and saved to `cipher_history.log`

## Usage

```
python cipher.py
```

Navigate the menu to select a cipher. All options are interactive — no command-line arguments needed.

## Example

```
[1] Caesar Cipher
[2] Vigenere Cipher
[3] ROT13
[4] History
[5] Clear history
[0] Exit
```

Brute-force mode ranks all 25 shifts by how closely the output matches English letter frequency — the best guess is highlighted at the top.

## Requirements

Python 3.10+, no external dependencies.

## Why I built this

I wanted to go beyond basic Caesar cipher implementations and actually apply frequency analysis as a real decryption technique. The Vigenere cipher added an interesting layer since it requires a keyword and uses polyalphabetic substitution, making it significantly harder to crack manually.
