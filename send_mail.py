import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email_with_attachment(subject, body, to_emails, pdf_path):

    from_email = "alerta2@apotiguar.com.br"  
    password = "#Alerta2!"  

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))  

    msg['To'] = ", ".join(to_emails)

    part = MIMEBase('application', 'octet-stream')
    with open(pdf_path, 'rb') as attachment:
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_path)}')
    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.apotiguar.com.br', 587)
        server.starttls()  
        server.login(from_email, password)
        server.sendmail(from_email, to_emails, msg.as_string())
        server.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")


