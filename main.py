import nltk
from mail import *
from engine import *
from tkinter import messagebox
from mail import get_emails
from Authenticate import get_service
import ezgmail

def main():

    email_list = []

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

    ezgmail.init()

    load_from_file = messagebox.askyesno('Load Emails', 'Would you like to load emails from file?')

    if load_from_file:
        email_list = load_emails_from_file()
        if email_list is None:
            messagebox.showerror('Error', 'Failed to load emails from file.')
            return
    else:
        #emails = get_emails(service, 'in:inbox')
        emails = ezgmail.search('in:inbox', 250)

        for i in range(200):
            temp = {}
            temp['class'] = classify_email(emails[i].messages[0].snippet)
            temp['body'] = emails[i].messages[0].snippet
            temp['from'] = emails[i].messages[0].recipient
            temp['time'] = emails[i].messages[0].timestamp.isoformat()
            temp['subject'] = emails[i].messages[0].subject
            temp['ThreadId'] = emails[i].messages[0].threadId
            email_list.append(temp)

        # Save the emails to file
        save_emails_to_file(email_list)
    
    
    create_gui(email_list)

if __name__ == '__main__':
    main()

