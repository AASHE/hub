import logging

from django.core.mail import send_mail
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)

NEW_SUBMITTED_RESOURCE_EMAIL_TEMPLATE = 'new_submitted_resource_email.txt'


def send_new_submitted_resource_email(resource, request):
    content = render_to_string(NEW_SUBMITTED_RESOURCE_EMAIL_TEMPLATE,
                               {'resource': resource,
                                'request': request})
    try:
        send_mail(subject='New Submitted Resource for Review',
                  message=content,
                  from_email='resources@aashe.org',
                  recipient_list=['resources@aashe.org'])
    except:
        logger.exception('Failed to send mail for new submitted resource.')
