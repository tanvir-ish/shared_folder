#!/usr/bin/python3
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

SMTP_SERVER='vps30780.inmotionhosting.com'
SMTP_PORT= 465
SENDER_EMAIL='info@jobxprss.com'
SENDER_PASSWORD='v&RzdlGm.8lK'
SECURED = True

#SENDER_EMAIL='no-reply@jobxprss.com'
#SENDER_PASSWORD='L?D0Y{M.N+6T'


logging.basicConfig(filename=f'email.log',
                    format='%(levelname)s [%(asctime)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

console = logging.StreamHandler()
console.setFormatter(logging.Formatter('%(message)s'))
logging.getLogger().addHandler(console)

def send_email(to, subject, body):
    server = None
    try:
        if SECURED:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        server.ehlo()  # Can be omitted
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        html = """
        <html>
            <head></head>
            <body>
        """  \
            + body.replace('\r\n', '<br />\r\n') + \
        """
            </body>
        </html>
        """

        msg.attach(MIMEText(html, 'html'))

        server.sendmail(
            from_addr=SENDER_EMAIL,
            to_addrs=to,
            msg = msg.as_string())
    except Exception as ex:
        logging.exception(ex)
        raise
    finally:
        if server != None:
            server.quit()


if __name__ == '__main__':
    df = pd.read_csv("mail_list.csv")
    for idx, row in df.iterrows():
        try:
            logging.info(f"Sending email to {row['Email']}")
            send_email(row['Email'], row['Subject'], row['Message'])
            logging.info("Ok")
        except Exception as ex:
            logging.error("Failed")
            logging.exception(ex)


