import smtplib
from email.mime.text import MIMEText

from dotenv import dotenv_values

config = dotenv_values(".env")


def send_email(new_apartments) -> None:
    body = "Siemka!\n\nPopatrz, ktoś przed chwilą dodał nowe mieszkanki:\n\n"

    for apartment in new_apartments:
        body += (
            f'Dodano: {apartment["created"]},\n'
            f'Cena: {apartment["price"]}\n'
            f'{apartment["url"]}\n\n'
        )
    body += f"Pozdrawiam,\nTwój slejw szukający mieszkanek"

    SUBJECT = "Uwaga nowe mieszkanki!!!"
    msg = body
    TO = config['RECIPIENT_MAIL']
    FROM = config['SENDER_MAIL']

    msg = MIMEText(msg)
    msg["Subject"] = SUBJECT
    msg["To"] = TO
    msg["From"] = FROM
    try:
        smtpObj = smtplib.SMTP("smtp-mail.outlook.com", 587)
    except Exception as e:
        print(e)
        smtpObj = smtplib.SMTP_SSL("smtp-mail.outlook.com", 465)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(FROM, config['MAIL_PASSWORD'])
    smtpObj.sendmail(FROM, TO, msg.as_string())
    print("Email has been sent!")
    smtpObj.quit()
