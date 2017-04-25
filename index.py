#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

import requests
import sys
import json
import datetime
import sendgrid
import os
from sendgrid.helpers.mail import *

def enviaEmail(body):

	sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
	from_email = Email('rodrigo.prates@mercadobackoffice.com')
	subject = 'Fechamento de items Done do projeto de Features - ' + str(datetime.datetime.now())
	to_email = Email('express.features@mercadobackoffice.com')
	content = Content('text/html', body.encode('utf-8'))
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())


def mainProcess(shouldDelete):

	cards = api('https://api.github.com/projects/columns/882651/cards')
	issues = json.loads(cards.content)
	if len(issues) > 0:
		print 'Total de issues em Done:', len(issues)
		mailBody = u'<h2>Total de issues em Done: ' + str(len(issues)) + '</h2><p><b>Cards arquivados:</b></p><ul>'

		for issue in issues:
			oneIssue = json.loads(api(issue['content_url']).content)
			msg = u'' + str(oneIssue['number']) + ' - '
			msg += oneIssue['title']
			msg += u' (' + str(oneIssue['user']['login']) + ' ' + str(oneIssue['state']) + ')'
			print msg
			mailBody += u'<li style="margin: 4px 0;">'
			mailBody += u'<a href="' + str(oneIssue['html_url']) + '" target="_blank" style="color: black; text-decoration: none">'
			mailBody += u'<span style="color: #3367d6">' + str(oneIssue['number']) + '</span> - '
			mailBody += oneIssue['title']
			mailBody += u'(<i>by: ' + str(oneIssue['user']['login']) + '</i>)'
			mailBody += u'<span style="color: black">' + str(oneIssue['state']) + '</span></a></li>'

		mailBody += '</ul><p>E-mail enviado em ' + str(datetime.datetime.now()) + ' por kpl-project-archiver Python</p>'

		enviaEmail(mailBody)
	else:
		print 'Nao ha issues a processar'


def api(url):

	headers = {
        'Authorization' : 'token '+ os.environ.get('SENDGRID_API_KEY')
        'Accept'        : 'application/vnd.github.inertia-preview+json'
    }
	r = requests.get(url, headers=headers)
	return r


def main():
	deleteCards = raw_input("Remover cards que estao em Done (Y/N)? ")
	if deleteCards=="Y":
		deleteCards = True
	else:
		deleteCards = False

	mainProcess(deleteCards)

if __name__ == "__main__":
    main()
