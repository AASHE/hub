import logging

from django.core.mail import send_mail
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


def send_resource_submitted_email(resource, submitter, request):
    content = render_to_string('submit/resource_submitted_email.txt',
                               {'resource': resource,
                                'request': request})
    try:
        send_mail(subject='Resource Submitted for Review',
                  message=content,
                  from_email='resources@aashe.org',
                  recipient_list=['resources@aashe.org', submitter])
    except:
        logger.exception('Failed to send mail for resource submitted.')
