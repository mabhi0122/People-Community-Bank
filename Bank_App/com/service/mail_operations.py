import smtplib
from email.message import EmailMessage
from random import randint
from Bank_App.com.service.constants import sender_mail, mail_pass


# function that generates random number
def otp_gen():
    otp = randint(100000, 999999)
    return otp


# function that sends mail and verifies OTP
def mailOtpVerification(email):
    try:
        # senderMail = send_mail
        # password = mail_pass

        # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # server.login(sender_mail, mail_pass)

        # Generate otp
        otp = otp_gen()

        # # send mail
        # subject = 'OTP Verification'
        # message = f"""
        # Subject: OTP Verification
        #
        # Welcome to People Community Bank, Trust Above All.
        # Your OTP is: {otp}
        # """
        # server.sendmail(sender_mail, email, message)
        # print("An OTP has been sent to : " + email)
        # server.quit()
        # print()

        # Create EmailMessage object
        msg = EmailMessage()
        msg['Subject'] = 'OTP Verification'
        msg['From'] = sender_mail
        msg['To'] = email
        msg.set_content(f"Welcome to People Community Bank, Trust Above All.\nYour OTP is: {otp}")

        # Add HTML alternative
        msg.add_alternative(f"""
                <!DOCTYPE html>
                <html>
                    <body>
                        <h4>Welcome to <span style="color:SlateGray;">People Community Bank</span>. Trust Above All.</h4>
                        <h4>Your OTP is: <span style="color:SlateGray;">{otp}</span></h4>
                    </body>
                </html>
                """, subtype='html')

        # Send email using SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_mail, mail_pass)
            smtp.send_message(msg)
        print(f"An OTP has been sent to: {email}")

        # Prompt user for OTP
        try:
            user_otp = int(input("Please Enter OTP to continue : "))
        except ValueError:
            print("Invalid OTP! Must be a number...")
            print()
            return False

        # Verify OTP
        if user_otp == otp:
            print("OTP Verified Successfully...")
            return True
        else:
            print("Invalid OTP. Please try again!...")
            return False

    except smtplib.SMTPException:
        # ERROR - SMTP error occurred: (535, 'Authentication failed')
        print("Unable to send OTP at the moment. Please try again later!...")
        return False

    except Exception:
        # if Sender email or password is not configured.
        print("An unexpected error occurred. Please try again later!...")


# email = input("Enter email: ")
# mailOtpVerification(email)
