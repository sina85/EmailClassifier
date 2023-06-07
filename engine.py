import openai
from mail import *
import tkinter as tk
from tkinter import ttk
import json
import base64
import webbrowser
import tkinter as tk
from tkinter import ttk

def decode_content(encoded_content):
    try:
        # Decode the base64 encoded string
        decoded_bytes = base64.urlsafe_b64decode(encoded_content)
        
        # Convert bytes to string
        decoded_str = decoded_bytes.decode('utf-8')
        
        return decoded_str
    except UnicodeDecodeError:
        try:
            # Try decoding with 'latin-1' if 'utf-8' fails
            decoded_str = decoded_bytes.decode('latin-1')
            return decoded_str
        except Exception as e:
            print(f"Error decoding content with latin-1: {e}")
            return ""
    except Exception as e:
        print(f"Error decoding content: {e}")
        return ""

EMAILS_FILE = 'emails.json'  # The file where we'll store the emails

def load_emails_from_file():
    try:
        with open(EMAILS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_emails_to_file(emails):
    with open(EMAILS_FILE, 'w') as f:
        json.dump(emails, f)

def show_email(encoded_content):
    #decoded_content = decode_content(encoded_content)

    # Create a new Tkinter window
    window = tk.Toplevel()
    window.title('Email Content')

    # Create a scrollbar
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side='right', fill='y')

    # Create a Text widget in this window
    text = tk.Text(window, wrap='word', yscrollcommand=scrollbar.set)
    text.insert('1.0', encoded_content)
    text.pack(fill='both', expand=True)

    # Configure the scrollbar
    scrollbar.config(command=text.yview)

def count_tokens(text):
  tokens = re.findall(r"\w+", text)
  return len(tokens)

def create_gmail_thread_url(thread_id):
    base_url = "https://mail.google.com/mail/u/0/#inbox/"
    return base_url + thread_id

def open_in_gmail(event, thread_id):
    # Function to open the Gmail thread in the default web browser
    url = create_gmail_thread_url(thread_id)
    webbrowser.open(url, new=1)  # 'new=1' means open in a new window

def create_gui(emails):
    # Create the root window
    root = tk.Tk()
    root.title("Email Classification")

    # Create a tabbed notebook
    notebook = ttk.Notebook(root)

    # Create a tab for each category
    tabs = {
        'Accepted - Moving Forward': ttk.Frame(notebook),
        'Accepted - Job Offered': ttk.Frame(notebook),
        'Rejected': ttk.Frame(notebook),
        'Others': ttk.Frame(notebook),
    }

    # Add each tab to the notebook
    for category, tab in tabs.items():
        notebook.add(tab, text=category)

    # Create a treeview for each tab
    for category, tab in tabs.items():
        treeview = ttk.Treeview(tab, columns=('From', 'Subject'), show='headings')
        treeview.heading('From', text='From')
        treeview.heading('Subject', text='Subject')
        treeview.pack(fill='both', expand=True)
        tabs[category] = treeview

    # Populate each treeview with the appropriate emails
    for email in emails:
        classification = classify_email(email.messages[0].snippet)
        treeview = tabs.get(classification, tabs['Others'])
        item_id = treeview.insert('', 'end', values=(email.messages[0].recipient, email.messages[0].subject))
        
        # Bind the double-click event to the treeview to open the email in Gmail
        treeview.tag_bind(item_id, '<Double-1>', lambda e, thread_id=email.messages[0].threadId: open_in_gmail(e, thread_id))

    # Pack the notebook into the root window and run the Tkinter event loop
    notebook.pack(fill='both', expand=True)
    root.mainloop()

def classify_email(email_content):
    """
    Classify the email as either moving forward in the application process, accepted for the job, or rejected
    using the OpenAI API.

    :param service: Authenticated OpenAI API service instance.
    :param email: Dict, contains details of an email.
    :return: String, classification result.
    """

    openai.api_key = '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'

    if not email_content:
        return 'Others'
    
    prompt = ("Your task is to classify the emails into three categories: 'Accepted - Moving Forward', "
              "'Accepted - Job Offered', and 'Rejected'. If an email indicates that the applicant has moved forward "
              "in the application process, classify it as 'Accepted - Moving Forward'. If an email clearly states "
              "that the applicant has been offered the job, classify it as 'Accepted - Job Offered'. If the email "
              "conveys that the applicant has been rejected or the application will not be moving forward, classify "
              "it as 'Rejected'. You will only reply the identified class, no explanation needed!")

    if count_tokens(prompt + email_content) > 3500:
        return 'Others'

    
    messages = [
        {"role": "system", "content" : "You are a classifier with expertise in employment application emails"},
        {"role": "user", "content": prompt + ' '.join(email_content)},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    result = response['choices'][0]['message']['content'].strip()

    return result

