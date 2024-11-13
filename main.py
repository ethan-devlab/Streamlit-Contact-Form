# coding=utf-8

"""
Author: Ethan Chan / JC Work
Version: 2.1.1
First Release: 2024-10-30
Last Update: 2024-11-14 00:43:34
"""

from datetime import datetime as dt
import pytz
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError, EmailUndeliverableError

sender, password = st.secrets["Email"]["email"], st.secrets["Email"]["password"]
receiver = sender
port = 587
date = st.secrets["General"]["available_date"]
today = dt.now(pytz.timezone("Asia/Taipei")).strftime("%Y-%m-%d")
if "disable" not in st.session_state or st.session_state.disable is False:
    st.session_state.disable = True

if today >= date:
    st.session_state.disable = False
else:
    st.session_state.disable = True

st.set_page_config(page_title="Contact Us")
st.title("Contact Us")
st.subheader("We are group 2! If you have any questions, kindly fill in the form to contact us!")

form = st.form("contact_form")
form.markdown("<p style='font-size: 13pt;color: lightblue'><strong>Privacy Policy</strong>: By filling in the form below, you acknowledge "
              "and consent to the collection of your personal information. We may collect your name, ID and email. "
              "We respect your privacy and are committed to protecting your personal information.</p>",
              unsafe_allow_html=True)
confirm_box = form.checkbox("***By ticking this box I agree to the privacy policy stated above**")
form.markdown("<p style='font-size: 12pt'><span style='color: red;'>*</span>Required Fields</p>",
              unsafe_allow_html=True)
# form.markdown(
#     "<p style='font-size: 12pt; color: #fc3535'>Kind Reminder: Only <b>English</b> is acceptable in all fields.</p>",
#     unsafe_allow_html=True)
name = form.text_input("**Your Name***")
ID = form.text_input("**Your ID***")
email = form.text_input("**Your Email***")
subject = form.text_input("**Subject**")
message = form.text_area("**Message***")
copy_checkbox = form.checkbox("**Send me a copy of my responses**")
submit = form.form_submit_button("Submit", disabled=st.session_state.disable, icon=":material/send:")
if today < date:
    form.markdown("<p style='font-size: 12pt'>Submit button will be available on 2024-11-14.</p>",
                  unsafe_allow_html=True)

# For self-sending
mimetext_ss = f"""
<p>You received an email from <b>{name}</b>, Student/Teacher ID: <b>{ID}</b>,</p>
<p>email: {email}</p>
<br>
<p>Here is the original content:</p>
<p>{message}</p>

"""

# Copy for real sender
mimetext_cp = f"""
<p>Hi <b>{name}</b>, Student/Teacher ID: <b>{ID}</b>,</p>
<p>Thank you for contacting us! We will reply to you ASAP.</p>
<p>Here is the original content:</p>
<p>{message}</p>
<br>
<p>Please note that this is a copy of your response.</p>
<br>
<p>---------</p>
<p>Best regards,</p>
<p><b>Group 2</b></p>
"""


def check(email):
    try:
        valid = validate_email(email, check_deliverability=True)
        email = valid.normalized
        return True, email
    except (EmailNotValidError or EmailUndeliverableError) as e:
        form.error(e)
        return False, email


def send(normalized_email):
    try:
        server = smtplib.SMTP("smtp.gmail.com", port)
        server.ehlo()
        server.starttls()
        server.login(user=sender, password=password)
        msg = MIMEMultipart('alternative')
        msg.set_charset('utf-8')
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject
        html = MIMEText(mimetext_ss, 'html', 'UTF-8')
        msg.attach(html)
        if copy_checkbox:
            copy = MIMEMultipart('alternative')
            copy.set_charset('utf-8')
            copy['From'] = sender
            copy['To'] = normalized_email
            copy['Subject'] = subject
            copy_html = MIMEText(mimetext_cp, 'html', 'UTF-8')
            copy.attach(copy_html)
            server.sendmail(sender, normalized_email, copy.as_string())
        server.sendmail(sender, [receiver, st.secrets["Email"]["bcc"]], msg.as_string())
        server.quit()
        if copy_checkbox:
            form.success("Your response has been recorded! Please check your mailbox for a copy of your response and further information.")
        else:
            form.success("Your response has been recorded!")
        print("Email sent")
    except Exception as e:
        form.error(e)


if submit:
    print("Starting sending email")
    if name and email and message and ID and confirm_box:
        valid, normalized_email = check(email)
        if valid:
            send(normalized_email)
    else:
        form.error("\\* fields are required")

st.markdown(
    f"<div style='position: relative; bottom: 0; width: 100%; color: lightblue;'><p>© 2021 - 2024 Ethan Chan. All Rights Reserved.<p></div>",
    unsafe_allow_html=True)
