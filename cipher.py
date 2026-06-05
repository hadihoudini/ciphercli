import string
import sys
import os
from datetime import datetime

LOG = "cipher_history.log"

FREQ = {
    'e':12.70,'t':9.06,'a':8.17,'o':7.51,'i':6.97,'n':6.75,'s':6.33,
    'h':6.09,'r':5.99,'d':4.25,'l':4.03,'c':2.78,'u':2.76,'m':2.41,
    'w':2.36,'f':2.23,'g':2.02,'y':1.97,'p':1.93,'b':1.49,'v':0.98,
    'k':0.77,'j':0.15,'x':0.15,'q':0.10,'z':0.07
}

R = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
BOLD = "\033[1m"
MAG = "\033[95m"

def col(text, c):
    return f"{c}{text}{R}"

def log_action(action, detail):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a") as f:
        f.write(f"[{ts}] {action}: {detail}\n")

def freq_score(text):
    text = text.lower()
    total = sum(1 for c in text if c.isalpha())
    if total == 0:
        return 0.0
    score = sum(FREQ.get(c, 0) for c in text)
    return score / total

def show_freq(text):
    text = text.lower()
    total = sum(1 for c in text if c.isalpha())
    if total == 0:
        print(col("  No letters to analyse.", RED))
        return
    counts = {}
    for c in text:
        if c.isalpha():
            counts[c] = counts.get(c, 0) + 1
    print(col("\n  Frequency Analysis", CYAN))
    print("  " + "-"*48)
    print(f"  {'Letter':<8}{'Count':<8}{'% in text':<14}{'English avg'}")
    print("  " + "-"*48)
    for letter, count in sorted(counts.items(), key=lambda x: -x[1]):
        pct = (count / total) * 100
        eng = FREQ.get(letter, 0.0)
        bar = col("█" * int(pct), GREEN) + col("░" * (15 - int(pct)), DIM)
        print(f"  {letter.upper():<8}{count:<8}{pct:<6.2f}%  {bar}  (eng: {eng:.2f}%)")

def caesar_enc(text, shift):
    out = []
    for ch in text:
        if ch in string.ascii_lowercase:
            out.append(string.ascii_lowercase[(ord(ch) - 97 + shift) % 26])
        elif ch in string.ascii_uppercase:
            out.append(string.ascii_uppercase[(ord(ch) - 65 + shift) % 26])
        else:
            out.append(ch)
    return "".join(out)

def caesar_dec(text, shift):
    return caesar_enc(text, -shift)

def brute_force(ctext):
    results = []
    for shift in range(1, 26):
        plain = caesar_dec(ctext, shift)
        results.append((shift, plain, freq_score(plain)))
    return sorted(results, key=lambda x: -x[2])

def vigenere(text, key, mode):
    key = key.lower()
    out = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[ki % len(key)]) - 97
            if mode == "dec":
                shift = -shift
            if ch.islower():
                out.append(string.ascii_lowercase[(ord(ch) - 97 + shift) % 26])
            else:
                out.append(string.ascii_uppercase[(ord(ch) - 65 + shift) % 26])
            ki += 1
        else:
            out.append(ch)
    return "".join(out)

def rot13(text):
    return caesar_enc(text, 13)

def read_file(path):
    if not os.path.isfile(path):
        print(col(f"  File not found: {path}", RED))
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(col(f"  Saved: {path}", GREEN))

def maybe_save(content, default):
    if input(col("\n  Save to file? (y/n): ", DIM)).strip().lower() == "y":
        name = input(col(f"  Filename [{default}]: ", DIM)).strip() or default
        write_file(name, content)

def get_shift():
    while True:
        try:
            s = int(input(col("  Shift (1-25): ", YELLOW)))
            if 1 <= s <= 25:
                return s
            print(col("  Must be 1-25.", RED))
        except ValueError:
            print(col("  Numbers only.", RED))

def get_key():
    while True:
        k = input(col("  Keyword (letters only, min 2): ", YELLOW)).strip()
        if k.isalpha() and len(k) >= 2:
            return k
        print(col("  Letters only, at least 2 characters.", RED))

def banner():
    print(col("""
  ╔══════════════════════════════════════════════╗
  ║       CipherCLI v2.0 — by Abdul Hadi        ║
  ║  Caesar · Vigenere · ROT13 · Freq Analysis  ║
  ╚══════════════════════════════════════════════╝
""", CYAN))

def caesar_menu():
    print(col("\n  ── Caesar Cipher ──", CYAN))
    print("  [1] Encrypt\n  [2] Decrypt\n  [3] Brute-force\n  [4] Frequency analysis\n  [5] File mode\n  [0] Back")
    choice = input(col("\n  Select: ", YELLOW)).strip()
    if choice == "1":
        text = input(col("  Text: ", YELLOW))
        shift = get_shift()
        out = caesar_enc(text, shift)
        print(col(f"\n  Encrypted: {out}", GREEN))
        log_action("Caesar enc", f"shift={shift} in='{text}' out='{out}'")
        maybe_save(f"Original : {text}\nShift    : {shift}\nEncrypted: {out}\n", "caesar_enc.txt")
    elif choice == "2":
        text = input(col("  Ciphertext: ", YELLOW))
        shift = get_shift()
        out = caesar_dec(text, shift)
        print(col(f"\n  Decrypted: {out}", GREEN))
        log_action("Caesar dec", f"shift={shift} in='{text}' out='{out}'")
        maybe_save(f"Ciphertext: {text}\nShift     : {shift}\nDecrypted : {out}\n", "caesar_dec.txt")
    elif choice == "3":
        text = input(col("  Ciphertext: ", YELLOW))
        results = brute_force(text)
        print(col("\n  Results ranked by English likelihood:\n", CYAN))
        print(f"  {'Rank':<6}{'Shift':<8}{'Score':<10}Plaintext")
        print("  " + "-"*60)
        lines = []
        for rank, (shift, plain, score) in enumerate(results, 1):
            line = f"  #{rank:<5}{shift:<8}{score:<10.2f}{plain}"
            print(col(line, GREEN) if rank == 1 else line)
            lines.append(f"Rank {rank} | Shift {shift} | Score {score:.2f} | {plain}")
        log_action("Caesar brute", f"in='{text}' best_shift={results[0][0]}")
        maybe_save("\n".join(lines), "brute_results.txt")
    elif choice == "4":
        text = input(col("  Text: ", YELLOW))
        show_freq(text)
    elif choice == "5":
        print(col("  [e] Encrypt  [d] Decrypt", DIM))
        mode = input(col("  Mode: ", YELLOW)).strip().lower()
        path = input(col("  File path: ", YELLOW)).strip()
        text = read_file(path)
        if text is None:
            return
        shift = get_shift()
        out = caesar_enc(text, shift) if mode == "e" else caesar_dec(text, shift)
        write_file(os.path.splitext(path)[0] + ("_enc.txt" if mode == "e" else "_dec.txt"), out)

def vigenere_menu():
    print(col("\n  ── Vigenere Cipher ──", MAG))
    print("  [1] Encrypt\n  [2] Decrypt\n  [0] Back")
    choice = input(col("\n  Select: ", YELLOW)).strip()
    if choice == "1":
        text = input(col("  Text: ", YELLOW))
        key = get_key()
        out = vigenere(text, key, "enc")
        print(col(f"\n  Encrypted: {out}", GREEN))
        print(col(f"  Keyword  : {key}", DIM))
        log_action("Vigenere enc", f"key='{key}' in='{text}' out='{out}'")
        maybe_save(f"Original : {text}\nKeyword  : {key}\nEncrypted: {out}\n", "vigenere_enc.txt")
    elif choice == "2":
        text = input(col("  Ciphertext: ", YELLOW))
        key = get_key()
        out = vigenere(text, key, "dec")
        print(col(f"\n  Decrypted: {out}", GREEN))
        log_action("Vigenere dec", f"key='{key}' in='{text}' out='{out}'")
        maybe_save(f"Ciphertext: {text}\nKeyword   : {key}\nDecrypted : {out}\n", "vigenere_dec.txt")

def main():
    banner()
    while True:
        print(col("  Main Menu", BOLD))
        print(f"  {col('[1]', CYAN)} Caesar Cipher")
        print(f"  {col('[2]', MAG)} Vigenere Cipher")
        print(f"  {col('[3]', YELLOW)} ROT13")
        print(f"  {col('[4]', DIM)} History")
        print(f"  {col('[5]', RED)} Clear history")
        print(f"  {col('[0]', DIM)} Exit\n")
        choice = input(col("  Select: ", YELLOW)).strip()
        if choice == "1":
            caesar_menu()
        elif choice == "2":
            vigenere_menu()
        elif choice == "3":
            text = input(col("\n  Text: ", YELLOW))
            out = rot13(text)
            print(col(f"\n  Result: {out}", GREEN))
            log_action("ROT13", f"in='{text}' out='{out}'")
            maybe_save(f"Input : {text}\nROT13 : {out}\n", "rot13.txt")
        elif choice == "4":
            if not os.path.isfile(LOG):
                print(col("  No history yet.", DIM))
            else:
                print(col(f"\n  Last 20 entries:\n", CYAN))
                with open(LOG) as f:
                    for line in f.readlines()[-20:]:
                        print(col("  " + line.rstrip(), DIM))
                print()
        elif choice == "5":
            if input(col("  Clear history? (y/n): ", RED)).strip().lower() == "y":
                open(LOG, "w").close()
                print(col("  Cleared.", GREEN))
        elif choice == "0":
            print(col("\n  Bye.\n", CYAN))
            sys.exit(0)
        else:
            print(col("  Invalid.\n", RED))

if __name__ == "__main__":
    main()
