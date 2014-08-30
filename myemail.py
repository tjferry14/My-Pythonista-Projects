import console
import smtplib
import time
import ui

email_provider = raw_input('Gmail, AOL, Yahoo! or Comcast? ').title() 
login = (console.login_alert('Login', 'Enter your login credentials.', '', '', 'Submit'))
email_user = login[0]
email_pwd = login[1]

def send_action(sender):
	global sendto, subj, assignment
	sendto = v['tofield'].text
	subj = v['subjectfield'].text	
	assignment = v['message'].text
	main()
	
def cancel_action(sender):
	smtpserver.close()
	ui.close_all()

def main():	
	global sendto, subj, assignment		
	header = 'To: ' + sendto + '\\n' + 'From: ' + email_user + '\\n' + 'Subject: ' + subj +'\\n'
	msg = header + assignment + '\\n'
	smtpserver.sendmail(email_user, sendto, msg)
	sent_time = time.strftime("%A, %B %d, %Y at %I:%M:%S %p.", time.localtime())
	console.hud_alert('Your message has been sent successfully on ' + sent_time, 'success', 2.1)
	v['tofield'].text = ''
	v['subjectfield'].text = ''
	v['message'].text = ''

v = ui.load_view('myemail')

send = ui.ButtonItem()
send.title = 'Send'
send.action = send_action
v.right_button_items = [send]

fromfield = v['fromfield']
fromfield.text = email_user
fromfield.scroll_enabled = False
v['tofield'].clear_button_mode = 'while_editing'
v['subjectfield'].clear_button_mode = 'while_editing'

if email_provider in ('Gmail', 'Google'):
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
if email_provider in ('Aol', 'AOL'):
	smtpserver = smtplib.SMTP("smtp.aol.com",587)
if email_provider in ('Yahoo', 'Yahoo!'):
	smtpserver = smtplib.SMTP("smtp.mail.yahoo.com",587)
if email_provider in ('Comcast'): 
	smtpserver = smtplib.SMTP("smtp.comcast.net",587)

smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(email_user, email_pwd)

v.present('sheet')
