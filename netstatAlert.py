#!/usr/bin/env python3

__author__		= "Rodrigo Contarino"

import os
import subprocess
import config as cfg


from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler

ntOutput = 'netstat.log'

def saveNetstatResult(ntOutput):
	cmd = ("netstat -suna | grep error > " + ntOutput)
	os.system(cmd)

def sendMail(sender, toAddress, subject, message):
	# create message object instance
	msg = MIMEMultipart()

	# setup the parameters of the message
	msg['From'] = sender
	msg['To'] = ", ".join(toAddress)
	msg['Subject'] = subject

	# add in the message body
	msg.attach(MIMEText(message, 'plain'))

	#create server
	server = SMTP(host=cfg.smtp['host'],port=cfg.smtp['port'])

	# send the message via the server.
	server.sendmail(sender, toAddress, msg.as_string())

	server.quit()

#print ("successfully sent email to %s:" % (msg['To']))

def checkNetstatOutput():
	result = subprocess.run(['cat', 'netstat.log'], stdout=subprocess.PIPE)
	result.stdout
	return (result.stdout.decode('utf-8'))

def monitor():
	with open(ntOutput, "r") as file:
		for line in file:
			if "0" not in line: sendMail(cfg.mail['from'],cfg.mail['to'],cfg.mail['subject'],checkNetstatOutput())
	file.close()

def removeFile(file):
	try:
		return os.remove(file)
	except OSError:
		pass

def submain():
	saveNetstatResult(ntOutput)
	monitor()
	removeFile(ntOutput)


def main():
	scheduler = BlockingScheduler()
	scheduler.add_job(submain, 'interval', hours=1)
	scheduler.start()

main()
