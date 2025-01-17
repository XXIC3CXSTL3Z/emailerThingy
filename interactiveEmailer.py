from emailerService import EmailSender
from tkinter import Tk
from tkinter.filedialog import askopenfilename

if __name__ == '__main__':
    sender = EmailSender()

    account = sender.choose_account()

    if account:
        to_email = input("Enter the recipient's address: ")
        subject = input("Enter the subject: ")
        body = input("Enter the body text: ")

        yn = input("Would you like to attach a file? [y/N?]: ")
        attachments = []
        if yn == "" or yn.lower() == 'n':
            pass
        elif yn.lower() == "y":
            Tk().withdraw()
            filename = askopenfilename()
            print(filename)
            attachments.append(filename)
        sender.send_email(account, to_email, subject, body, attachments)
    else:
        print("Selected account does not exist.")