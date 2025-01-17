import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import re
import mimetypes

class EmailSender:
    # PLEASE FOR THE LOVE OF GOD MAKE A '.ENV' FILE BEFORE TRYING TO RUN THESE
    def __init__(self):
        load_dotenv()
        self.accounts = self.load_accounts()


    def load_accounts(self):
        accounts = {}
        pattern = r"EMAIL_USER_([A-Z]+)_(\d+)"

        for key, email in os.environ.items():
            match = re.match(pattern, key)
            if match:
                provider = match.group(1)
                index = match.group(2)

                password_key = f"EMAIL_PASS_{provider}_{index}"
                password = os.getenv(password_key)

                if password:
                    account_name = f"{provider}_{index}"
                    accounts[account_name] = {
                        "email": email,
                        "password": password,
                        "smtp_server": self.get_smtp_server(provider),
                        "port": 465
                    }

        return accounts

    def get_smtp_server(self, provider):
        smtp_servers = {
            "GMAIL": "smtp.gmail.com",
            "YAHOO": "smtp.mail.yahoo.com",
        }
        return smtp_servers.get(provider, "smtp.mail.yahoo.com")

    def list_accounts(self):
        print("Available Email Accounts:")
        for account_name, account_info in self.accounts.items():
            print(f"{account_name}: {account_info['email']}")

    def choose_account(self):
        self.list_accounts()
        account_name = input("Enter the account name you want to use (e.g., GMAIL_1): ")

        return self.accounts.get(account_name)

    def send_email(self, account, to_email, subject, body, attachments=None):
        em = EmailMessage()
        em['From'] = account["email"]
        em['To'] = to_email
        em['Subject'] = subject
        em.set_content(body)

        if attachments:
            for attachment_path in attachments:
                try:
                    with open(attachment_path, 'rb') as f:
                        mime_type, _ = mimetypes.guess_type(attachment_path)
                        mime_type = mime_type or 'application/octet-stream'
                        main_type, sub_type = mime_type.split('/', 1)

                        em.add_attachment(
                            f.read(),
                            maintype=main_type,
                            subtype=sub_type,
                            filename=os.path.basename(attachment_path)
                        )
                except Exception as e:
                    print(f"Failed to attach file {attachment_path}: {e}")

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL(account["smtp_server"], account["port"], context=context) as smtp:
                smtp.login(account["email"], account["password"])
                smtp.sendmail(account["email"], to_email, em.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

