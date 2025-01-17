from dotenv import load_dotenv
import os

load_dotenv()


def add_account_to_env(provider, email, password):
    """
    Add an email account to the .env file with auto-indexed variables.
    Args:
        provider (str): The provider name (e.g., 'GMAIL', 'YAHOO')
        email (str): The email address to add
        password (str): The password for the email account
    """
    index = 1
    while os.getenv(f"EMAIL_USER_{provider}_{index}"):
        index += 1

    new_lines = [
        f"EMAIL_USER_{provider}_{index}={email}\n",
        f"EMAIL_PASS_{provider}_{index}={password}\n"
    ]

    with open(".env", "a") as env_file:
        env_file.writelines(new_lines)

    print(f"Added {provider} account {email} with index {index} to .env")


# Example usage
provider = input("Enter email provider (e.g., GMAIL, YAHOO): ").upper()
email = input("Enter the email address: ")
password = input("Enter the password: ")
add_account_to_env(provider, email, password)
