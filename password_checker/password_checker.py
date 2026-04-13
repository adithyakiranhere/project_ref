import hashlib
import math
import re
import secrets
import string
import sys
import requests


def calculate_entropy(password: str) -> float:
    """Calculate password entropy in bits. Higher = stronger."""
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[0-9]", password):
        pool += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        pool += 32
    if pool == 0:
        return 0.0
    return len(password) * math.log2(pool)


def strength_label(entropy: float) -> str:
    if entropy < 28:
        return "Very Weak 🔴"
    elif entropy < 36:
        return "Weak 🟠"
    elif entropy < 60:
        return "Reasonable 🟡"
    elif entropy < 128:
        return "Strong 🟢"
    return "Very Strong 🔵"


def check_pwned(password: str) -> int:
    """
    Check HaveIBeenPwned using k-anonymity.
    We only send the first 5 chars of the SHA-1 hash — never the password.
    Returns how many times the password has been seen in breaches.
    """
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)
    return 0


def suggest_strong_password(length: int = 16) -> str:
    """Generate a cryptographically secure random password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def analyze(password: str) -> None:
    print("\n🔐 Password Analysis")
    print("─" * 40)

    entropy = calculate_entropy(password)
    print(f"Length      : {len(password)}")
    print(f"Entropy     : {entropy:.1f} bits")
    print(f"Strength    : {strength_label(entropy)}")

    try:
        breaches = check_pwned(password)
        if breaches:
            print(f"Breach check: ❌ Found in {breaches:,} known breaches!")
        else:
            print("Breach check: ✅ Not found in known breaches")
    except requests.RequestException as e:
        print(f"Breach check: ⚠️  Could not reach API ({e})")

    if entropy < 60 or (breaches if "breaches" in dir() else 0) > 0:
        print(f"\n💡 Suggested strong password: {suggest_strong_password()}")
    print()


def main() -> None:
    if len(sys.argv) > 1:
        password = " ".join(sys.argv[1:])
    else:
        password = input("Enter a password to analyze: ").strip()
    if not password:
        print("No password provided.")
        return
    analyze(password)


if __name__ == "__main__":
    main()
