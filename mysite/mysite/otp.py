# import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# Streamlit app title
# st.title("Data Fetching App")

# Get user input
# password = st.text_input("Password:")
# recipient_email = st.text_input("Recipient Email:")
# send_date = st.date_input("Select Date")
# # body = "The data for asked date is: "
# subject = "DATA"
# body = "formatted_date4"

# Gmail credentials (replace with your own)
sender_email = "k63814776@gmail.com"
sender_password = "bnyc enyb ekxt cwii"




from datetime import datetime,date
# import numpy as np

# from mysite.tasks import add

# Function to send email
def send_email(formated_data):
    try:
        # Create the MIME object
        # formatted_date = send_date.strftime("%Y-%m-%d")
        # formated_data = "otp"

        # Concatenate the date with the existing body
        # body = f"{body} {formatted_date}"
        # print(body) 
        body = formated_data
        
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = "yashrajdwivedi26@gmail.com"
        message['Subject'] = "subject"
        message.attach(MIMEText(f"List of ladles not completing turnaround are \n {body}", 'plain'))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            # Login to the sender's email account
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, "yashrajdwivedi26@gmail.com", message.as_string())

        # st.success("Email sent successfully!")
       

    except Exception as e:
       print(e)
# Button to send email
# send_email()