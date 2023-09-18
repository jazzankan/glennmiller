from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText


def send_email(subject, body, sender, recipient, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    connection = smtplib.SMTP("smtp.websupport.se", port=587)
    connection.starttls()
    connection.login(user=sender, password=password)
    connection.sendmail(sender, recipient, msg.as_string())
    connection.quit()


response = requests.get("https://www.glennmillercafe.se/konserter")
glenn_page = response.text

soup = BeautifulSoup(glenn_page, "html.parser")
calender = ["Januari", "Februari", "Mars", "April", "Maj", "Juni", "Juli", "Augusti", "September", "Oktober", "November", "December"]
p_hits = soup.select("div.before-konsert p")
p_with_month = []
for p in p_hits:
    for month in calender:
        if month in str(p).title():
            p_text = p.getText()
            p_text = p_text.split()[0]
            p_with_month.append(p_text)

latest_month = p_with_month[-1].title()

# Email variables. Placed here because latest_month is now defined.
subject = "Glenn Miller"
body = f"Ny månad för Glenn Miller café: {latest_month} !"
sender = "anders@webbsallad.se"
recipient = "shasfn@gmail.com"
password = "ZxPr57y5wZQCiJA"

with open("latest_saved.txt") as f:
    saved_file = f.read()
    if latest_month != saved_file:
        # send_email(subject, body, sender, recipient, password)
        pass

with open("latest_saved.txt", "w") as f:
    f.write(latest_month)

