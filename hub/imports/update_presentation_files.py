"""
Because the 3rd and 4th files were not uploaded during the original import
we need to have this one-off script to add those.
"""

# from import_presentations import columns
from utils import get_rows
from datetime import datetime

from hub.apps.content.types.presentations import Presentation
from hub.apps.content.models import File

columns = [
    "Presentation Title",
    "Description or Abstract",
    "Organization1",
    "Organization1_id",
    "Organization2",
    "Organization2_id",
    "Organization3",
    "Organization3_id",
    "Organization4",
    "Organization4_id",
    "Organization5",
    "Organization5_id",
    "Organization6",
    "Organization6_id",
    "SustainabilityTopic1",
    "SustainabilityTopic2",
    "SustainabilityTopic3",
    "AcademicDiscipline1",
    "AcademicDiscipline2",
    "AcademicDiscipline3",
    "OfficeDepartment1",
    "OfficeDepartment2",
    "Tags",
    "PresentationDate",
    "ConferenceName",
    "PresType",
    "Author1_Name",
    "Author1_Title",
    "Author1_Org",
    "Author1_OrgID",
    "Author2_Name",
    "Author2_Title",
    "Author2_Org",
    "Author2_OrgID",
    "Author3_Name",
    "Author3_Title",
    "Author3_Org",
    "Author3_OrgID",
    "Author4_Name",
    "Author4_Title",
    "Author4_Org",
    "Author4_OrgID",
    "Author5_Name",
    "Author5_Title",
    "Author5_Org",
    "Author5_OrgID",
    "Author6_Name",
    "Author6_Title",
    "Author6_Org",
    "Author6_OrgID",
    "Image1",
    "File1",
    "File2",
    "File3",
    "File4",
]

rows = get_rows('hub/imports/fixtures/2016Presentations.xlsx', '2016')
published = datetime(month=11, day=18, year=2016)
bucket_prefix = '/uploads/aashe2016/'


def add_files(presentation):
    file_key = "File%d"
    for i in range(3, 5):
        key = file_key % i
        filename = row[columns.index(key)].value
        if filename:
            url = "https://hub-media.aashe.org%s%s" % (
                bucket_prefix, filename)
            print presentation.title
            print "adding %s" % url
            file = File.objects.create(
                ct=presentation, label=filename, item=url, affirmation=True)

dupes = []
missing = []
count = 0
for row in rows:

    """
    openpyxl returns incomplete rows, so I extend them here.
    """
    if len(row) < len(columns):
        class MockVal:
            def __init__(self, value):
                self.value = value
        new_row = []
        new_row.extend(row)
        for i in range(len(columns) - len(row)):
            new_row.append(MockVal(None))
        row = new_row

    if count > 0:
        try:
            p = Presentation.objects.get(
                title=row[0].value,
                published=published)  # description=row[1].value)
            add_files(p)
        except Presentation.MultipleObjectsReturned:
            if row[0].value not in dupes:
                dupes.append(row[0].value)
        except Presentation.DoesNotExist:
            missing.append(row[0].value)
    count += 1

print "Dupes: %d" % len(dupes)
for dupe in dupes:
    print dupe

print "Missing: %d" % len(missing)
for m in missing:
    print m
