import mysql.connector

from Bank_App.com.repo.db_operations import (db_connect, insert_data,
                                             fetch_data, fetch_column_data,
                                             update_data)


# function to fetch userId based on user_email
def fetch_userID(user_mail):
    # fetching entire row based on email from users table
    db_data_users = fetch_data('users', email=user_mail)

    try:
        # fetching userId variable from entire row
        userId = db_data_users[0][0]
        return userId
    except:
        return False


# function to display balance based on user_email
def displayBalance(user_mail):
    # fetching userId based on user_mail from users table
    userId = fetch_userID(user_mail)

    if userId:
        db_data_accounts = fetch_data('account', user_id=userId)
        print("[+] Account Balance : " + str(db_data_accounts[0][3]))
        print()
        return True
    else:
        return False


# function to depositMoney based on user_email
def depositMoney(user_mail, depositAmount):
    # fetching userId based on user_mail from users table
    userId = fetch_userID(user_mail)

    if userId:
        try:
            # fetching entire row of account table based on userId
            db_data_accounts = fetch_data('account', user_id=userId)

            # extracting and updating balance variable from entire row
            balance = db_data_accounts[0][3] + depositAmount

            # updating balance variable in database, account table using userId
            update_data('account', values={'balance': balance}, conditions={'user_id': userId})
            # displayBalance(user_mail)
            return True

        except:
            return False
    else:
        return False


def withdrawlMoney(user_mail, withdrawlMoney):
    # fetching userId based on user_mail from flm_users table
    userId = fetch_userID(user_mail)

    if userId:

        # fetching entire row of account table based on userId
        db_data_accounts = fetch_data('account', user_id=userId)

        # extracting user balance from entire row data
        balance = db_data_accounts[0][3]

        # function to check whether user balance is greater than withdrawlamount
        if balance > withdrawlMoney:
            balance = balance - withdrawlMoney

            # updating user balance into database
            update_data('account', values={'balance': balance}, conditions={'user_id': userId})
            # displayBalance(user_mail)
            return True

        else:
            print("[-] Insufficient Funds...")
            print()
            return False
    else:
        return False


def transferMoney(user_mail, transferAmount):
    # fetching senderUserId based on user_mail from users table
    senderUserId = fetch_userID(user_mail)

    # fetching account information from senderUserId from account table
    senderAccountDetails = fetch_data('account', user_id=senderUserId)

    # extracting senderDetails from account table
    senderBalance = senderAccountDetails[0][3]
    senderAccountId = senderAccountDetails[0][0]
    senderAccountNumber = senderAccountDetails[0][2]

    # checking whether senderBalance is greater than amount to be transferred
    if senderBalance > transferAmount:

        # receiver accountId
        receiverAccountId = int(input("Enter Recipients Account Id: "))
        # account_ids = fetch_column_data('account', 'account_id')

        # checking whether receiver account does exist or not
        if receiverAccountId in fetch_column_data('account', 'account_id'):

            # performing update operations on sender account balance
            updateSenderBalance = senderBalance - transferAmount

            # updating sender account info into account database
            update_data('account', values={'balance': updateSenderBalance}, conditions={'user_id': senderUserId})
            displayBalance(user_mail)

            # fetching receiver account info from account tabel
            receiver_db_data = fetch_data('account', account_id=receiverAccountId)

            # extracting receiver data
            receiverUserId = receiver_db_data[0][1]
            receiverAccountNumber = receiver_db_data[0][2]

            # performing update operations on receiver account balance
            receiverBalance = receiver_db_data[0][3] + transferAmount

            # updating receiver account info into database
            update_data('account', values={'balance': receiverBalance}, conditions={'account_id': receiverAccountId})

            # inserting transaction details into transaction table ( sender side )
            insert_data('transaction', user_id=senderUserId, account_id=senderAccountId, amount=transferAmount,
                        from_account=senderAccountNumber,
                        to_account=receiverAccountNumber, trans_type='db')

            # inserting transaction details into transaction table (receiver side )
            insert_data('transaction', user_id=receiverUserId, account_id=receiverAccountId, amount=transferAmount,
                        from_account=senderAccountNumber, to_account=receiverAccountNumber, trans_type='cd')

            return True
        else:
            print("[-] Receiver Account Does not exist...")
            print()
            return False
    else:
        print("[-] Insufficient Balance...")
        print()
        return False


def transactionHistory(user_email):
    try:
        # connect to the MySQL database
        conn = db_connect()

        # create a cursor to execute sql queries
        cursor = conn.cursor()

        # query to retrieve transaction history based on user email
        query = """
                SELECT users.first_name, users.last_name, account.account_number, transaction.amount, transaction.from_account, transaction.to_account, transaction.trans_date, transaction.trans_type
                FROM users
                INNER JOIN transaction ON users.user_id = transaction.user_id
                INNER JOIN account ON transaction.account_id = account.account_id
                WHERE users.email = %s
            """

        # execute the query with the provided user_email
        cursor.execute(query, (user_email,))

        # fetch and print the transaction history
        print('Transaction History for User : ', user_email)
        print("{:<15} {:<15} {:<20} {:<15} {:<15} {:<15} {:<15} {:<10}".format("First Name", "Last Name",
                                                                               "Account Number", "Amount",
                                                                               "From Account", "To Account", "Date",
                                                                               "Trans Type"))
        for row in cursor.fetchall():
            first_name, last_name, account_number, amount, from_account, to_account, trans_date, trans_type = row
            print(
                "{:<15} {:<15} {:<20} {:<15} {:<15} {:<15} {:<15} {:<10}".format(first_name, last_name, account_number,
                                                                                 amount, from_account, to_account,
                                                                                 str(trans_date),
                                                                                 trans_type))
        print()

        # close the cursor and the database connection
        cursor.close()
        conn.close()

        return True

    except mysql.connector.Error as e:

        print('Error : ', e)
        return False
