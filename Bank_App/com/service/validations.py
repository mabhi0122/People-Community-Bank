import re
from random import randint
from datetime import datetime
import hashlib
from Bank_App.com.repo.db_operations import fetch_column_data


def genderValidation():
    while True:

        # taking gender value from user and converting it into lowercase
        gender = input("Please Enter your Gender [m/f/o] : ").lower()
        print()

        # checking entered gender is in specified one or not
        if gender in ['m', 'f', 'o']:
            return gender
        else:
            print("[-] Please Enter Specified Gender Types only...")
            print()
            continue


def mobileNumValidation():
    while True:

        # taking mobile number from user
        mobileNo = input("Please Enter Your Mobile Number : ")
        print()

        # regex pattern to check whether string has 10 numbers or not
        pattern = r'^\d{10}$'

        # use the re.match function to check if the number matches the pattern
        if re.match(pattern, mobileNo):
            return mobileNo
        else:
            print("[-] Please Enter Valid Mobile Number: ")
            print()
            continue


def uniqueEmail(emailId):
    # checking emailId is unique or not
    # by fetching email column from users table
    if emailId in fetch_column_data('users', 'email'):
        return False
    else:
        return True


def uniqueAccountNumber(AccountNumber):
    # checking AccountNumber is unique or not
    # by fetching account_number column in account table
    if AccountNumber in fetch_column_data('account', 'account_number'):
        return False
    else:
        return True


def emailValidation():
    while True:
        try:
            # collecting user email id
            email = input('Please Enter Your Gmail address : ')
            print()
            # isUnique = uniqueEmail(email)

            # pattern used to check whether entered email is valid or not
            pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'

            # use the re.fullmatch() function to check if the email matches the pattern
            if re.fullmatch(pattern, email):
                # Check whether entered email is unique or not
                if uniqueEmail(email):
                    return email
                else:
                    print("[-] This Email is Taken, Please Provide another Email Address: ")
                    print()
                    continue
            else:
                print("[-] Please Enter Valid Gmail Address: ")
                print()
                continue
        except Exception as e:
            print("[-] An unexpected error occurred: ", e)
            print()
            continue


def passwordValidation():
    while True:

        # update for password strength
        # salt = secretes.token_hex(16)  # 16 bytes of random data

        # generating salt randomly
        salt = randint(00000, 99999)

        # taking password from user
        password = input("Please type your Password: ")

        # taking confirm password from user
        confirmPassword = input("Please Re-type your Password: ")
        print()

        # comparing both password and confirm password, if same proceed
        if password == confirmPassword:

            # adding salt with password
            password = str(salt) + password

            # hashing password to maintain security
            password = hashlib.sha256(password.encode()).hexdigest()
            return salt, password
        else:
            print("[-] Password and Confirm Password should match try again!...")
            print()
            continue


def dateValidation():
    while True:

        # check min,max dates to avoid future dates for dob
        # collecting dob from users in specified format
        dob = input("Please Enter your Date of Birth in DD/MM/YYYY Format: ")
        print()

        # Regex pattern to validate format
        pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'

        # check if the format matches
        if re.match(pattern, dob):
            try:
                # validate if the date is logical and not in the future
                dob_date = datetime.strptime(dob, "%d/%m/%Y")
                if dob_date > datetime.now():
                    print("[-] Date of Birth cannot be in the future. Please try again!..")
                    print()
                    continue
                # Convert it to MySQL-compatible format
                dob = dob_date.strftime("%Y-%m-%d")
                return dob

            except ValueError:
                # Handle invalid dates (e.g., 31/02/2023)
                print("[-] Invalid date. Please ensure the day, month,and year are correct!.")
                print()
                continue

        else:
            print("[-] Invalid Date Of Birth, please try again!...")
            print()
            continue
