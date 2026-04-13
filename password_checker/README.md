# 🔐 Password Strength Analyzer

A command-line tool that rates password strength using entropy analysis and checks whether it has appeared in real-world data breaches — **without ever sending your password over the internet**.

## Features

- 📊 **Entropy-based strength scoring** (bits of randomness, not cheap rules)
- 🕵️ **Breach detection** via the HaveIBeenPwned API using k-anonymity
- 🎲 **Secure password suggestions** using Python's `secrets` module
- 🖥️ **Simple CLI** — works from any terminal

## How the breach check stays private

Your password never leaves your machine. The tool:
1. Computes the SHA-1 hash of your password locally
2. Sends only the **first 5 characters** of that hash to the API
3. Receives a list of all breached hashes starting with those 5 chars
4. Compares locally to see if yours is in the list

This is called **k-anonymity** — the API has no way to know which password you were actually checking.

## Usage

```bash
pip install -r requirements.txt
python password_analyzer.py
```

Or pass the password directly:

```bash
python password_analyzer.py mySecretPass123
```

## Example Output

```
🔐 Password Analysis
────────────────────────────────────────
Length      : 14
Entropy     : 82.3 bits
Strength    : Strong 🟢
Breach check: ✅ Not found in known breaches
```

## Built with
- Python 3.9+
- `requests`, `hashlib`, `secrets`


## Author
Adithyakiran
adithyakiranhere
