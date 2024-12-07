import hashlib
import secrets
import time
import threading
from Bank_App.com.repo.db_operations import update_data


def hash_password_with_salt(salt, password):
    # generate a random salt
    # salt= secrets.token_hex(16) # 16 bytes of random data

    # Concatenate the salt and password
    salted_password = str(salt) + password

    # hash the salted_password using SHA-256
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

    # returned the salt and hashed password as a tuple
    return hashed_password


# Example usage:
# password = "my_secure_password"
# salt, hashed_password = hash_password_with_salt(password)
#
# print("Salt:", salt)
# print("Hashed Password:", hashed_password)


def reset_failed_attempts(user_email):
    lock_time = 30  # Lock duration in seconds
    start_time = time.time()  # Record the start time

    print(f"[+] Your account is locked. You can try logging in after {lock_time} seconds.")
    while True:
        elapsed_time = time.time() - start_time
        remaining_time = max(0, int(lock_time - elapsed_time))

        print(f"[-] Please wait {remaining_time} seconds...", end="\r")
        if remaining_time <= 0:
            break
        time.sleep(1)

    # Reset the failed login attempts
    update_data('users', values={'failed_count_attempts': 0}, conditions={'email': user_email})
    print("[+] Hurray!!! Account is Unlocked, Try Logging in Now...")
    print()

