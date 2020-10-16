from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors
from googleapiclient.discovery import build

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

import pickle
import os.path


# Get Credentials locally
def get_credentials_gmail_api(path_creds="config/gmail_credentials.json"):
    scopes = ['https://www.googleapis.com/auth/gmail.send']  # ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token_gmail.pickle'):
        with open('token_gmail.pickle', 'rb') as token:
            print("Read old creds")
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Get credentials
            flow = InstalledAppFlow.from_client_secrets_file(path_creds, scopes)
            creds = flow.run_local_server(port=8000, prompt='consent')
        # Save the credentials for the next run
        with open('token_gmail.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def create_mail(sender_mail, recipient_mail, subject_mail, html_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEMultipart('alternative')
    message['from'] = sender_mail
    message['to'] = recipient_mail
    message['subject'] = subject_mail

    mime_test_html = MIMEText(html_text, 'html')
    message.attach(mime_test_html)

    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body_mail = {'raw': raw}
    return body_mail


def send_mail(service, user_id, body_mail):
    """Send an email message.
    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    message: Message to be sent.
    Returns:
    Sent Message.
    """
    try:
        response_dict = (service.users().messages().send(userId=user_id, body=body_mail).execute())
        print('Mail sent')
        # print('Message Id: {}'.format(response_dict['id']))
        return response_dict
    except errors.HttpError as error:
        print('An error occurred: {}'.format(error))
        return "mail send"


def get_templated_mail(firstname):
    subject_mail_mail = "You Can't Miss It! 😺"
    html_template_mail = """\
        <html>
          <head></head>
          <body>
            <img src="https://www.vech.com.mx/static/images/vech_banner.png">
            <p>Hey {firstname}!</p>
            <p>
                ¿You earn at least $50 USD every week with Uber, Uber Eats, DiDi, DiDi Food, Rappi, or Cornershop? <br><br>
                <strong>Vech guarantees you a loan TODAY of $25 USD!</strong><br>
            </p>
            <p style="text-align:center; font-size:large;">
                <strong><a href="https://ingresos-garantizados.vech.com.mx" target="_blank" class="button">I want my 
                Income Promise</a><strong>
            </p>
            <br>
          </body>
        </html>     
    """
    html_templated_mail = html_template_mail.format(firstname=firstname)
    return html_templated_mail, subject_mail_mail


if __name__ == '__main__':
    # Get Gmail credentials
    gmail_creds = get_credentials_gmail_api()
    service_gmail = build('gmail', 'v1', credentials=gmail_creds)

    recipient_email = 'pierre@gmail.com'
    first_name = 'Pierre'
    print(recipient_email, first_name)

    # Template and body
    html_templated_adhoc, subject_adhoc = get_templated_mail(first_name)
    # print(html_templated_adhoc)

    body_mail_adhoc = \
        create_mail(sender_mail="soporte@vech.com.mx", recipient_mail=recipient_email,
                    subject_mail=subject_adhoc, html_text=html_templated_adhoc)

    # Send mail
    response_dict = send_mail(service_gmail, user_id="soporte@vech.com.mx", body_mail=body_mail_adhoc)
    print(response_dict)
