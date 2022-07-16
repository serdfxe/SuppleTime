import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from SuppleTime.pr.app.config import EMAIL_PASS, EMAIL_ADDRES



class Email():
    _addres = EMAIL_ADDRES
    _password = EMAIL_PASS


    def auth():
        smtp = smtplib.SMTP("smtp.timeweb.ru")
        print(smtp.login(Email._addres, Email._password, 'portable'))
        return smtp

    
    def send(email: str, body: str, sub: str, is_html=False):
        smtp = smtplib.SMTP("smtp.timeweb.ru")
        smtp.starttls() 
        print(f'addres = {Email._addres} password = {Email._password}')
        print(smtp.login(Email._addres.encode('utf-8').decode('ascii'), Email._password.encode('utf-8').decode('ascii')))
       
        msg = MIMEMultipart()
        message = body
        msg['From'] = Email._addres
        msg['To'] = email
        msg['Subject'] = sub
        msg.attach(MIMEText(message, ('plain', 'html')[is_html]))
        
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())
        
        smtp.quit()
