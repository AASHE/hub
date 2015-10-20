from django.db import models
from model_utils import Choices

from ..models import ContentType
from .strings import AFFIRMATION


class Material(ContentType):
    MATERIAL_TYPE_CHOICES = Choices(
        ('assignment', 'Assignment or Exercise'),
        ('syllabus', 'Syllabus'),
        ('course', 'Course Presentation'),
    )
    LEVEL_CHOICES = Choices(
        ('introductory', 'Introductory'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    document = models.FileField(help_text="The following files formats are "
        "acceptable: JPEG, PNG, TIFF...", blank=True, null=True)
    material_type = models.CharField(max_length=50, blank=True, null=True,
        choices=MATERIAL_TYPE_CHOICES)
    course_name = models.CharField(max_length=500, blank=True, null=True)
    course_level = models.CharField(max_length=50, blank=True, null=True,
        choices=LEVEL_CHOICES)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Course Material'
        verbose_name_plural = 'Course Materials'
