#!/usr/bin/env python
# coding=utf-8

from send_gmail import get_credentials_gmail_api, create_mail, send_mail

from googleapiclient.discovery import build
from time import sleep
import pandas as pd
from datetime import datetime


def get_df_fb_loan_status():
    # Get Current Datetime
    current_datetime = datetime.now()
    print(current_datetime)

    # This function, you have to create it yourself
    df_need_to_pay = pd.DataFrame()
    
    return df_need_to_pay


def get_templated_reminder_payment(firstname, user_id):
    subject_mail_reminder_payment = "Bitch better have my money! ⏰"
    html_template_reminder_payment = """\
    <html>
      <head></head>
      <body>
        <p>Hey {firstname}! 👋</p>
        <p>Gentle reminder that today is payday, so please don't forget to pay me. 😳</p>
        <p>Check your payment details in your <strong><a href="https://www.mywebsite.com/mydebt?id={user_id}">personal calculator</a></strong>.</p>
        <p>If you already paid, just ignore that mail</p>
        <p>Saludos,<br>
        El Equipo de Vech
        </p>
      </body>
    </html>
    """
    html_templated_reminder_payment = html_template_reminder_payment. \
        format(firstname=firstname, user_id=user_id)
    return html_templated_reminder_payment, subject_mail_reminder_payment


if __name__ == '__main__':
    # Get Gmail credentials
    gmail_creds = get_credentials_gmail_api()
    service = build('gmail', 'v1', credentials=gmail_creds)

    # Get The Users that need to Pay today
    df_need_to_pay = get_df_fb_loan_status()
    print("There are {} Users who need to pay today 💸".format(len(df_need_to_pay)))

    # Loop
    list_user_id = []
    for index, row in df_need_to_pay.iterrows():
        # Get parameters
        user_id = row['user_id']
        recipient_email = row['email']
        firstname = row['firstname']
        print(user_id, firstname, recipient_email)

        # Reminder Payment: Template and Body
        html_templated_reminder_payment, subject_reminder_payment = \
            get_templated_reminder_payment(firstname, user_id)

        body_mail_reminder_payment = \
            create_mail(sender_mail="soporte@vech.com.mx", recipient_mail=recipient_email,
                        subject_mail=subject_reminder_payment, html_text=html_templated_reminder_payment)

        # Reminder Payment: Send mail
        response_dict = send_mail(service, user_id="soporte@vech.com.mx", body_mail=body_mail_reminder_payment)
        print(response_dict)

        # Append Prospect Id
        list_user_id.append(user_id)

        # Wait to avoid Limit Rate Gmail API
        sleep(1/4)
