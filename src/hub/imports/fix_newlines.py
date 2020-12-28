"""
    fix_newlines.py

    When importing from the old IRC, I didn't parse all the newlines to double
    them up so that they would appear as new paragraphs with markdown. Doing
    that here.
"""

from hub.apps.content.models import CONTENT_TYPES
from hub.apps.content.types.casestudies import CaseStudy
import pdb


for k, ct_class in CONTENT_TYPES.items():

    # Get the TextFields
    text_fields = []
    for f in ct_class._meta.fields:
        if f.__class__.__name__ == "TextField":
            text_fields.append(f.name)

    for ct in ct_class.objects.all():
        for field_name in text_fields:
            text = getattr(ct, field_name)
            if text:
                new_text = text.replace("\n", "\n\n")
                setattr(ct, field_name, new_text)
        ct.save()
