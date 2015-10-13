from django.db import models

from ..models import ContentType
from ...metadata.models import ProgramType, InstitutionalOffice

AFFIRMATION = """By checking this box, you are granting AASHE an irrevocable,
royalty-free, non-exclusive and perpetual license to use the submitted documents
in publications, newsletters, resources or promotional materials, and you are
hereby representing and warranting that you own all the rights to the submitted
image, or have obtained all necessary licenses and/or permissions to use the
submitted image, and that AASHE's use of such image will not infringe the rights
of any third party, including but not limited to intellectual property rights,
or any other rights protected by law (such as the right to privacy or right of
publicity).""".replace('\n', ' ')


class CaseStudy(ContentType):
    program_type = models.ForeignKey(ProgramType, blank=True, null=True, verbose_name='Program Type')
    overview = models.TextField('Project overview', blank=True, null=True)
    background = models.TextField('Background', blank=True, null=True)
    goals = models.TextField('Project Goals', blank=True, null=True)
    implementation = models.TextField('Project Implementation', blank=True, null=True)
    timeline = models.TextField('Project Timeline', blank=True, null=True)
    financing = models.TextField('Financing', blank=True, null=True)
    results = models.TextField('Project Results (or results to date)', blank=True, null=True)
    lessons_learned = models.TextField('Lessons learned', blank=True, null=True)
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    @property
    def class_content_type(self):
        return self.CONTENT_TYPES.casestudy
