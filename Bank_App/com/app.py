from Bank_App.com.service.user_service import CreateAccount, login, forgotPassword
from Bank_App.com.service.banking_service import (displayBalance, depositMoney, withdrawlMoney,
                                                  transferMoney, transactionHistory)
from Bank_App.com.service.banner_printing import bannerPrinting, exitBannerPrinting
import time

# print()
# print("[+] Welcome to People Community Bank ")

# printing banner
try:
    bannerPrinting()
except FileNotFoundError:
    print("Error!...")

# displaying choice table
while True:
    print()
    print("Enter 1 to Register")
    print("Enter 2 to Login")
    print("Enter 3 to Forgot Password")
    print("Enter 4 to Exit")
    print()

    try:
        userChoice = int(input())
    except ValueError:
        print("[-] Invalid Choice. Please Enter a Number..")
        print()
        continue

    if userChoice == 1:
        print("[+] Account Creation in process...")
        time.sleep(2)

        # Function Responsible to create a account is called
        ca = CreateAccount()
        ca.accountCreation()

        # Once Account created, CreateAccount() completes execution controller should repeat with start menu options
        # again
        continue
    elif userChoice == 2:
        # accessing existing account
        user_mail = input("Username(E-mail): ")

        # login/authentication initiated
        if not login(user_mail):
            # print("[-] Login Failed...")
            print()
            continue
        else:
            print("[+] Logged In Successful...")
            print()
            while True:
                print("[+] Please select operation to perform from below menu...")
                print()
                print("Enter 1 to Display Balance.")
                print("Enter 2 to Deposit Money.")
                print("Enter 3 to Withdraw Money.")
                print("Enter 4 to Transfer Money.")
                print("Enter 5 to Print Transaction History.")
                print("Enter 6 to Log Out.")
                print()

                try:
                    userChoice = int(input())
                except ValueError:
                    print("[-] Invalid choice. Please enter a number.")
                    print()
                    continue

                if userChoice == 1:
                    print()

                    # calling function that display balance
                    if displayBalance(user_mail):
                        pass
                    else:
                        print("[-] Problem in Displaying Balance")
                        print()

                elif userChoice == 2:
                    print()
                    try:
                        depositAmount = int(input("[+] Enter Amount to Deposit: "))
                        print()
                        if depositMoney(user_mail, depositAmount):
                            print("[+] Deposit Successful...")
                            displayBalance(user_mail)
                            continue
                        else:
                            print("[-] Deposit Unsuccessful...")
                            print()
                            continue
                    except ValueError:
                        print("[-] Enter Valid Amount!...")
                        print()
                        continue

                    # calling function that is responsible to deposit money
                    # user_mail to identify user, depositAmount to specify amount to be deposited


                elif userChoice == 3:
                    print()
                    try:
                        withdrawalAmount = int(input("[+] Enter Withdrawal Amount: "))
                        print()
                        if withdrawlMoney(user_mail, withdrawalAmount):
                            print("[+] Money withdrawal Successful...")
                            displayBalance(user_mail)
                            print()
                            continue
                        else:
                            # print("[-] Withdrawal Unsuccessful...")
                            # print()
                            continue
                    except ValueError:
                        print("[-] Enter Valid Amount...")
                        print()
                        continue


                elif userChoice == 4:
                    print()
                    try:
                        transferAmount = int(input("Enter Amount to be Transferred: "))
                        print()
                        if transferMoney(user_mail, transferAmount):
                            print("[+] Money Transfer Successful...")
                            print()
                            continue
                        else:
                            print("[-] Money Transfer Unsuccessful...")
                            print()
                            continue
                    except ValueError:
                        print("[-] Enter Valid Amount...")

                elif userChoice == 5:
                    print()
                    if transactionHistory(user_mail):
                        continue
                    else:
                        print("[-] Error in printing Transaction History...")
                        print()
                        continue

                # logout functionality
                elif userChoice == 6:
                    print("[-] Logout Successful...")
                    print()
                    break

    elif userChoice == 3:
        if forgotPassword():
            print("[+] Password Reset Successful...")
            print()
            continue
        else:
            # print("[-] Password Reset Unsuccessful...")
            print()
            continue

    elif userChoice == 4:
        print()
        # print("[+] Thank you for using People Community Bank, See you soon...")
        exitBannerPrinting()
        quit()
