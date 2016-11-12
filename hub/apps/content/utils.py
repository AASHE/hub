import logging

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.template.loader import render_to_string

from .models import (Author,
                     CONTENT_TYPES,
                     File,
                     Image)

logger = logging.getLogger(__name__)


def send_resource_approved_email(resource, request):
    subject = ('Your Resource has been Approved - '
               'AASHE Campus Sustainability Hub')
    exception_text = 'Failed to send mail for approved resource.'
    _send_resource_email(resource=resource,
                         request=request,
                         subject=subject,
                         text_template='content/resource_approved_email.txt',
                         html_template='content/resource_approved_email.html',
                         exception_text=exception_text)


def send_resource_declined_email(resource, request):
    subject = ('Your Resource has been Declined - '
               'AASHE Campus Sustainability Hub')
    exception_text = 'Failed to send mail for declined resource.'
    _send_resource_email(resource=resource,
                         request=request,
                         subject=subject,
                         text_template='content/resource_declined_email.txt',
                         html_template='content/resource_declined_email.html',
                         exception_text=exception_text)


def _send_resource_email(resource, request, subject,
                         text_template, html_template,
                         exception_text):
    """
    Send mail about a resource to the submitter of the resource,
    from resources@aashe.org.
    """
    context = {'resource': resource,
               'request': request}
    text_content = render_to_string(text_template, context)
    html_content = render_to_string(html_template, context)
    message = EmailMultiAlternatives(subject=subject,
                                     body=text_content,
                                     from_email='resources@aashe.org',
                                     to=[resource.submitted_by.email],
                                     cc=['resources@aashe.org'])
    message.attach_alternative(html_content, 'text/html')
    try:
        message.send()
    except:
        logger.exception(exception_text)


def update_all_content_type_search_data():
    """
    Update all the search data for all the things.
    """
    for model in CONTENT_TYPES.values():
        print("Updating search data for " + str(model))
        update_search_data(model)


def update_search_data(model):
    """
    Update the search data for all the things.
    """
    for instance in model.objects.all():

        author = instance.authors.first()
        if author:
            post_save.send(Author, instance=author, created=False)

        file_ = instance.files.first()
        if file_:
            post_save.send(File, instance=file_, created=False)

        image = instance.images.first()
        if image:
            post_save.send(Image, instance=image, created=False)
