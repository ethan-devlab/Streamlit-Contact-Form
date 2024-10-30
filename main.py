# coding=utf-8

"""
Author: Ethan Chan / JC Work
Version: 1.0
First Release: 2024-10-30
Last Update: 2024-10-30 14:24:13
"""

from datetime import datetime as dt
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError

sender, password = st.secrets["Email"]["email"], st.secrets["Email"]["password"]
receiver = sender
port = 587

if "disable" not in st.session_state or st.session_state.disable is False:
    st.session_state.disable = True

if dt.now().strftime("%Y-%m-%d") >= "2024-11-14":
    st.session_state.disable = False
else:
    st.session_state.disable = True

st.set_page_config(page_title="Contact Us")
st.title("Contact Us")
st.subheader("We are group 2! If you have any questions, kindly fill in the form to contact us!")

form = st.form("contact_form")
form.markdown("<p style='font-size: 12pt'><span style='color: red;'>*</span>Required Fields</p>", unsafe_allow_html=True)
form.markdown("<p style='font-size: 12pt; color: #fc3535'>Kind Reminder: Only <b>English</b> is acceptable in all fields.</p>", unsafe_allow_html=True)
name = form.text_input("**Your Name***")
email = form.text_input("**Your Email***")
subject = form.text_input("**Subject**")
message = form.text_area("**Message***")
submit = form.form_submit_button("Submit", disabled=st.session_state.disable)
if dt.now().strftime("%Y-%m-%d") < "2024-11-14":
    form.markdown("<p style='font-size: 12pt'>Submit button will be available on 2024-11-14.</p>", unsafe_allow_html=True)

mimetext = f"""
You received an email from {name}, email: {email}

Here is the original content:
{message}

"""

def check(email):
    try:
        valid = validate_email(email)
        email = valid.normalized
        return True
    except EmailNotValidError as e:
        st.error(e)
        return False

def send():
    try:
        server = smtplib.SMTP("smtp.gmail.com", port)
        server.ehlo()
        server.starttls()
        server.login(user=sender, password=password)
        msg = MIMEText(mimetext)
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        form.success("Your submit has been recorded!")

    except Exception as e:
        form.error(e)


if submit:
    print("Starting sending email")
    if name and email and message:
        if check(email):
            send()
    else:
        form.error("\\* fields are required")


st.markdown(f"<div style='position: relative; bottom: 0; width: 100%; color: lightblue;'><p>© 2021 - 2024 Ethan Chan. All Rights Reserved.<p></div>", unsafe_allow_html=True)