from random import randint
from Bank_App.com.service.validations import (genderValidation, dateValidation, mobileNumValidation,
                                              emailValidation, passwordValidation, uniqueAccountNumber)

from Bank_App.com.service.mail_operations import mailOtpVerification
from Bank_App.com.repo.db_operations import (insert_data, fetch_data, fetch_column_data,
                                             update_last_login_by_email, update_data)

from Bank_App.com.service.user_security import hash_password_with_salt, reset_failed_attempts
from Bank_App.com.service.constants import MAX_LOGIN_ATTEMPTS


class CreateAccount:

    def accountCreation(self):

        # collecting user details
        self.fname = input("Please Enter your First Name: ")
        self.lname = input("Please Enter your Last Name: ")
        self.name = self.fname + self.lname
        self.gender = genderValidation()
        self.dob = dateValidation()
        self.mobileNo = mobileNumValidation()
        self.aadhar = input("Please Enter your 12 digit Aadhar Number: ")
        self.email = emailValidation()
        self.salt, self.password = passwordValidation()
        self.initalDeposit = int(input("Enter Initial deposit (>1000): "))
        # self.balance = self.initialDeposit()

        print()
        print("[+] OTP Verification Process initiated")
        print()

        # code to verify email through OTP and checking whether account number created is unique or not
        if mailOtpVerification(self.email):
            print("[+] OTP Verified Successfully...")
            print()
            while True:
                # generating a new random account number
                self.accountNumber = randint(100000, 999999)
                print("[+] Account Created, Your Account Number is: " + str(self.accountNumber))
                print()

                # checking whether generated account number is unique or not, if not re-generate account number
                if uniqueAccountNumber(self.accountNumber):
                    break
                else:
                    continue
        # inserting user details into database, table: users
        insert_data('users', first_name=self.fname, last_name=self.lname, email=self.email, dob=self.dob,
                    salt=self.salt, password=self.password)

        # fetching userId of the new user created
        self.userId = fetch_data('users', email=self.email)
        # print(self.userId)

        # inserting account info into database, table account for new user created
        insert_data('account', user_id=self.userId[0][0], account_number=self.accountNumber,
                    balance=self.initalDeposit, is_active=True)

        return


def login(user_mail):
    while True:

        # checking whether user_mail exist or not in users
        if user_mail in fetch_column_data('users', 'email'):
            user_password = input('Password: ')
            print()

            # fetching user data from database using user_mail
            db_data = fetch_data('users', email=user_mail)
            # print(db_data)
            # extracting user data
            failed_login_attempts = db_data[0][7]
            db_salt = db_data[0][5]
            db_password = db_data[0][6]

            if failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
                print("[-] Maximum Login Attempts Reached...!!! Account Locked..")
                reset_failed_attempts(user_mail)
                print()

                return False
                # code to reset failed_login_attempts to 0 after certain time

            else:
                # hashing user entered password with salt from database
                hashed_user_password = hash_password_with_salt(db_salt, user_password)

                # checking whether user entered password is same as database password
                if hashed_user_password == db_password:

                    # update failed_count_attempts to 0 in users
                    update_data('users', values={'failed_count_attempts': 0}, conditions={'email': user_mail})

                    # extracting last login data
                    last_login_date = db_data[0][8]
                    # if last_login_date != None:
                    print("[+] last login date and time: " + str(last_login_date))

                    # else:
                    #     return

                    # updating last_login_time in users to CURRENT TIME
                    update_last_login_by_email(user_mail)
                    # print("[+] Login Successful... Please select operation to perform below menu...")
                    print()
                    return True
                else:
                    failed_login_attempts += 1
                    update_data("users", values={"failed_count_attempts": failed_login_attempts},
                                conditions={'email': user_mail})
                    print("[-] Invalid Password!...please try again")
                    return False

        else:
            print("[-] Invalid Mail Id, Please try again!...")
            return False


def forgotPassword():
    # taking user_mail id as input
    user_mail = input("Enter Mail Id: ")
    try:
        # fetching user data row from users table based on user_mail
        db_data = fetch_data('users', email=user_mail)

        # extracting user dob from user data row fetched
        db_dob = db_data[0][4]

        # taking dob from user for further validation
        user_dob = dateValidation()

        # checking database_dob with user_dob entered
        if user_dob == str(db_dob):

            # verifying again with OTP to change password
            if mailOtpVerification(user_mail):

                # allowing user again to create new password
                updated_salt, updated_password = passwordValidation()

                # updating new password, salt into user database in users table based on user_mail
                update_data('users', values={'password': updated_password, 'salt': updated_salt},
                            conditions={'email': user_mail})

                return True
            else:
                print("[-] OTP Verification failed!, Please try again...")
                return False
        else:
            print("[-] DOB Verification failed!, Please try again...")
            return False
    except:
        print("[-] Mail Id does not exit!...")
        return False
