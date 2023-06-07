# Email Classifier

This project aims to classify emails and provides an easy-to-use graphical user interface (GUI) for user interaction. It uses Python and Tkinter to create a tabbed interface where emails are classified into different categories.

## Features

- **Email Classification:** Emails are classified into different categories based on user-defined criteria. The default categories are 'Accepted - Moving Forward', 'Accepted - Job Offered', 'Rejected', and 'Others'.
- **Interactive GUI:** The application provides a tabbed interface where each tab represents a different email category. Each email is displayed as an item in the corresponding tab's list.
- **Email Preview:** Double clicking on an email item opens the email in a small Google Chrome instance, allowing the user to quickly view the full content of the email.

## Usage

1. Clone the repository.
2. Install the required Python libraries using pip: `pip install -r requirements.txt`.
3. Run the `main.py` script in Python: `python main.py`.

## Customization

The email classification function (`classify_email`) can be customized to fit your specific needs. By default, it classifies emails based on the content of their 'snippet'. To change the classification rules, modify this function in the `main.py` file.

## License

This project is licensed under the terms of the MIT license.

## Contribution

Contributions are always welcome. Please fork the repository and create a pull request with your changes.

