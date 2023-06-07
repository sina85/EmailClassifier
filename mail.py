import base64
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def get_emails(service, search_criteria):
    """
    Retrieve email details from the Gmail account using the Gmail API based on search criteria.

    :param service: Authenticated Gmail API service instance.
    :param search_criteria: String, search criteria for fetching emails.
    :return: List of Dict, where each Dict contains details of an email.
    """
    # Request to fetch emails based on search criteria
    results = service.users().messages().list(userId='me', q=search_criteria).execute()
    messages = results.get('messages', [])

    emails = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()

        # Fetching details of the email
        payload = msg['payload']
        headers = payload['headers']

        data = {}
        for d in headers:
            if d['name'] == 'From':
                data['From'] = d['value']
            if d['name'] == 'Subject':
                data['Subject'] = d['value']

        if 'parts' in payload:
            part = payload['parts'][0]
            if part['mimeType'] == 'text/plain':
                data['Content'] = part['body']['data']
            else:
                data['Content'] = 'Non-text email content.'

        emails.append(data)
    
    return emails

def preprocess_email_content(content):
    """
    Preprocess the email content.

    :param content: String, the email content.
    :return: List of strings, preprocessed email content.
    """
    # Decoding the email content
    content = base64.urlsafe_b64decode(content).decode()

    # Converting to lower case
    content = content.lower()

    # Removing punctuations
    content = re.sub(r'[^\w\s]', '', content)

    # Tokenizing
    words = nltk.word_tokenize(content)

    # Removing stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Lemmatizing
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    return words
