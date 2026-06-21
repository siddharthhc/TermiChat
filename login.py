from instagrapi import Client
from instagrapi.exceptions import (
    TwoFactorRequired
)

cl = Client()

print("=== Instagram Login ===\n")

username = input("Username: ").strip()
password = input("Password: ").strip()

try:

    # First login try
    cl.login(username, password)

    cl.dump_settings("session.json")

    print("\n[+] Login Success")
    print("[+] Session Saved")

except TwoFactorRequired:

    print("\n[!] 2FA Required")

    code = input("Enter 2FA Code: ").strip()

    try:

        # Login with verification code
        cl.login(
            username,
            password,
            verification_code=code
        )

        cl.dump_settings("session.json")

        print("\n[+] 2FA Login Success")
        print("[+] Session Saved")

    except Exception as e:

        print("\n[-] 2FA Error:", e)

except Exception as e:

    print("\n[-] Login Error:", e)
