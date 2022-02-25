import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dependencies.settings import (SERVER_SMTP, SENDER_EMAIL, SENDER_PW, 
	PORT_SMTP)

class SMTPEmail:
	
	def __init__(self):
		self.portal = smtplib.SMTP(SERVER_SMTP, PORT_SMTP)
		self.login()

	def login(self):
		self.portal.connect(SERVER_SMTP, PORT_SMTP)
		self.portal.starttls()
		self.portal.login(SENDER_EMAIL, SENDER_PW)

	def send(self, recipient, subject, body, attachment=None, filename=None):
		self.message = MIMEMultipart()
		self.draft_email(recipient, subject, body)
		
		if attachment:
			self.add_attachment(attachment, filename)
				
		self.portal.sendmail(SENDER_EMAIL, recipient, self.message.as_string())
		
	def draft_email(self, recipient, subject, body):
		self.message.add_header('from', SENDER_EMAIL)
		self.message.add_header('to', recipient)
		self.message.add_header('subject', subject)
		self.message.attach(MIMEText(body,'plain'))
	
	def add_attachment(self, attachment, filename):
		file = MIMEApplication(open(attachment,"rb").read())
		file.add_header('Content-Disposition','attachment',filename=filename)
		self.message.attach(file)

	def logout(self):
		self.portal.quit()

