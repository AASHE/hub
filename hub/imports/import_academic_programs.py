from utils import get_rows, get_base_kwargs, get_base_m2m, sanity_check
from hub.apps.content.types.academic import AcademicProgram
from hub.apps.metadata.models import ProgramType

from datetime import datetime

columns = [
    "Program Name",
    "Description",
    "Organization1",
    "Organization1 ID",
    "Organization2",
    "Organization2 ID",
    "Topic1",
    "Topic2",
    "Acad Discipline1",
    "Acad Discipline2",
    "Acad Discipline3",
    "Tag(s): (comma separated)",
    "Year Founded (200x)",
    "Program Type",
    "Learning Outcomes",
    "Expected completion time",
    "Approx # students completing program annually",
    "Distance Ed.",
    "Commitment",
    "Link URL",
]

column_mappings = {
    'title': "Program Name",
    'description': "Description",
    'organizations_id': "Organization%d ID",
    'topics': "Topic%d",
    'disciplines': "Acad Discipline%d",
    'keywords': "Tag(s): (comma separated)",
    'outcomes': "Learning Outcomes",
    'completion': "Expected completion time",
    'num_students': "Approx # students completing program annually",
    'distance': "Distance Ed.",
    'commitment': "Commitment",
    'website_url': "Link URL",
}

def get_obj_kwargs():
    """

    """
    kwargs = {}
    date = row[columns.index("Year Founded (200x)")].value
    if date:
        kwargs['date_created'] = date.date()

    # get the program type
    prog_type = row[columns.index("Program Type")].value
    try:
        pt = ProgramType.objects.get(name=prog_type)
    except:
        print "Creating ProgramType: %s" % prog_type
        pt = ProgramType.objects.create(name=prog_type)
    kwargs['prog_type'] = pt

    return kwargs

rows = get_rows('hub/imports/fixtures/STARSAcademicProgramsNotInHub.xlsx', 'To Add')

# run the sanity check first
skip_index_list = sanity_check(rows, columns, column_mappings)

print "importing academic programs"

rows = get_rows('hub/imports/fixtures/STARSAcademicProgramsNotInHub.xlsx', 'To Add')
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

    count += 1
    if count == 1 or count in skip_index_list:
        continue
    # if count > 11:
    #     break
    print count

    kwargs = get_base_kwargs(columns, column_mappings, row)
    kwargs.update(get_obj_kwargs())
    acadmic_program = AcademicProgram.objects.create(**kwargs)
    get_base_m2m(
        acadmic_program, columns, column_mappings, row,
        bucket_prefix='/uploads/')
    acadmic_program.published = datetime.date()
    acadmic_program.save()
