import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

MAX_LOGIN_ATTEMPTS = 3

# Access environment variables

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_DATABASE')

sender_mail = os.getenv('SENDMAIL')
mail_pass = os.getenv('PASSWORD')

welcome_banner_path = 'C:\\Users\\mabhi\\OneDrive\\Desktop\\BankPDB\\Bank_App\\com\\Welcome banner.txt'
exit_banner_path = 'C:\\Users\\mabhi\\OneDrive\\Desktop\\BankPDB\\Bank_App\\com\\Exit banner.txt'
