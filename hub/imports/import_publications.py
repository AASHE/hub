"""
    import_publications.py
    
    Imports publication objects from the old IRC export files
    
    Questions:
        - status is published, right?
"""

from openpyxl import load_workbook
from datetime import datetime

from hub.apps.content.models import Publication, Author, File, Website
from hub.apps.metadata.models import (
    Organization, SustainabilityTopic, AcademicDiscipline, InstitutionalOffice)
from utils import create_file_from_url

from django.contrib.auth.models import User
from django.utils.text import slugify

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

user = User.objects.get(email='monika.urbanski@aashe.org')

wb = load_workbook('hub/imports/fixtures/Publications.xlsx', read_only=True)
ws = wb['Sheet1'] # ws is now an IterableWorksheet

columns = [
    "Title",
    "Description",
    "Organization1",
    "Organization1id",
    "Organization2",
    "Organization2id",
    "Organization3",
    "Organization3id",
    "Organization4",
    "Organization4id",
    "Organization5",
    "Organization5id",
    "Organization6",
    "Organization6id",
    "SustainabilityTopic1",
    "SustainabilityTopic2",
    "SustainabilityTopic3",
    "AcademicDisc1",
    "AcademicDisc2",
    "AcademicDisc3",
    "OfficeDept1",
    "OfficeDept2",
    "Tags",
    "Publication Release Date",
    "Publisher",
    "Periodical/Publication Name",
    "Type of Material",
    "Author1Name",
    "Author1Title",
    "Author1Org",
    "Author1OrgID",
    "Author2Name",
    "Author2Title",
    "Author2Org",
    "Author2OrgID",
    "Author3Name",
    "Author3Title",
    "Author3Org",
    "Author3OrgID",
    "Author4Name",
    "Author4Title",
    "Author4Org",
    "Author4OrgID",
    "Author5Name",
    "Author5Title",
    "Author5Org",
    "Author5OrgID",
    "Author6Name",
    "Author6Title",
    "Author6Org",
    "Author6OrgID",
    "File1",
    "File2",
    "Link1",
]

"""
    Publication fields
    
    Base Fields
    
    content_type = models.CharField(max_length=40)
    status = models.CharField(default=STATUS_CHOICES.new)
    permission = models.CharField(default=PERMISSION_CHOICES.member)
    published = models.DateTimeField(blank=True,null=True,)
    submitted_by = models.ForeignKeysettings.AUTH_USER_MODEL, blank=True, null=True)
    title = models.CharField(max_length=500)  # label set by self.title_label
    slug = models.CharField(max_length=500, editable=False)
    description = models.TextField('Description', blank=True, null=True)
    organizations = models.ManyToManyField('metadata.Organization',blank=True,)
    topics = models.ManyToManyField('metadata.SustainabilityTopic',)
    disciplines = models.ManyToManyField('metadata.AcademicDiscipline',blank=True)
    institutions = models.ManyToManyField('metadata.InstitutionalOffice',blank=True,)
    keywords = tagulous.models.TagField(blank=True,)
    notes = models.TextField('Notes', blank=True, null=True, default='',
                             help_text="Internal notes.")
                             
    Publication Fields
    
    release_date = models.DateField('Publication release date', blank=True, null=True,)
    publisher = models.CharField('Publisher', max_length=200, blank=True, null=True,)
    periodical_name = models.CharField(max_length=200, blank=True, null=True,)
    _type = models.CharField(max_length=40, choices=TYPE_CHOICES, null=True,)
    
"""

count = 0

for row in ws.rows:

    count += 1
    print "Count: %d" % count
    if count == 1:
        continue
    
    release_date=row[columns.index("Publication Release Date")].value
    # print type(release_date)
    # import pdb; pdb.set_trace()
    # break
    # if release_date:
    #     datetime.strptime(release_date, DATE_FORMAT)
    
    pub = Publication.objects.create(
        status=Publication.STATUS_CHOICES.published,
        published=datetime.now().date(),
        submitted_by=user,
        title=row[columns.index("Title")].value,
        slug=slugify(row[columns.index("Title")].value),
        description=row[columns.index("Description")].value,
        
        release_date=release_date.date(),
        publisher=row[columns.index("Publisher")].value,
        periodical_name=row[columns.index("Periodical/Publication Name")].value,
        _type=row[columns.index("Type of Material")].value,
    )

    # match organizations
    for i in range(1, 7):
        key = "Organization%d" % i
        org_name = row[columns.index(key)].value
        org_id = row[columns.index("%sid" % key)].value
        if org_id and org_id != 20096:
            print "%s: %d" % (org_name, org_id)
            org = Organization.objects.get(pk=org_id)
            if org.org_name.lower() != org_name.lower():
                print "ORG NAME WRONG!!!"
                print org.org_name
                print org_name
                assert False
            pub.organizations.add(org)
    
    # match topics
    print "adding topics"
    for i in range(1, 4):
        key = "SustainabilityTopic%d" % i
        topic_name = row[columns.index(key)].value
        if topic_name:
            topic = SustainabilityTopic.objects.get(name=topic_name)
            pub.topics.add(topic)
            print topic
            
    # match disciplines
    print "adding disciplines"
    for i in range(1, 4):
        key = "AcademicDisc%d" % i
        disc_name = row[columns.index(key)].value
        if disc_name:
            disc = AcademicDiscipline.objects.get(name=disc_name)
            pub.disciplines.add(disc)
            print disc
    
    # match institution offices
    print "Adding institution offices"
    for i in range(1, 3):
        key = "OfficeDept%d" % i
        office_name = row[columns.index(key)].value
        if office_name:
            try:
                office = InstitutionalOffice.objects.get(name=office_name)
            except InstitutionalOffice.DoesNotExist:
                office = InstitutionalOffice.objects.create(name=office_name)
                print "creating office: %s" % office
            pub.institutions.add(office)
    
    # set keywords
    print "adding tags"
    tags = row[columns.index("Tags")].value
    if tags:
        for tag in tags.split(','):
            print tag
            pub.keywords.add(tag)
            
    # authors
    print "adding authors"
    for i in range(1, 7):
        name = row[columns.index("Author%dName" % i)].value
        title = row[columns.index("Author%dTitle" % i)].value
        org_name = row[columns.index("Author%dOrg" % i)].value
        org_id = row[columns.index("Author%dOrgID" % i)].value
        if name:
            author = Author(ct=pub, name=name, title=title)
            # confirm org exists
            if org_id and org_id != 20096:
                org = Organization.objects.get(pk=org_id)
                if org.org_name.lower() != org_name.lower():
                    print "ORG NAME WRONG!!!"
                    print org.org_name
                    print org_name
                    assert False
                author.organization = org
            author.save()
            print author
    
    # files
    for i in range(1, 3):
        key = "File%d" % i
        url = row[columns.index(key)].value
        if url:
            create_file_from_url(pub, url)
    
    # links
    url = row[columns.index("Link1")].value
    if url:
        Website.objects.create(ct=pub, url=url)
        
    pub.save()
