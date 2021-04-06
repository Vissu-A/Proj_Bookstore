# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.result import AsyncResult

from django.core.mail import send_mail, EmailMessage
from django.conf import settings

@shared_task
def Account_Activate_Send_Mail(email, fname, act_link):
    '''
    This is function will send account activation link to the registered user's email.
    '''

    email_subject = 'Activate your account'
    email_body = 'Hi '+fname+'.\n'+'Please click on this link to activate your account'+'\n'+act_link

    email = EmailMessage(
        email_subject,
        email_body,
        'djangoclient97@gmail.com',
        [email,]
    )

    email.send(fail_silently=False)

@shared_task
def Reset_Password_Send_Mail(email, fname, act_link):
    '''
    This is function will send password reset link to the registered user's email.
    '''

    email_subject = 'Password Reset'
    email_body = 'Hi '+fname+'.\n'+'Please click on this link to reset your password'+'\n'+act_link

    email = EmailMessage(
        email_subject,
        email_body,
        'djangoclient97@gmail.com',
        [email,]
    )

    email.send(fail_silently=False)