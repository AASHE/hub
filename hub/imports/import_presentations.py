from utils import get_rows, get_base_kwargs, get_base_m2m, sanity_check
from hub.apps.content.types.presentations import Presentation

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
]

column_mappings = {
    'title': "Presentation Title",
    'description': "Description or Abstract",
    'organizations_id': "Organization%d_id",
    'author_name': "Author%d_Name",
    'author_title': "Author%d_Title",
    'author_org': "Author%d_Org",
    'author_org_id': "Author%d_OrgID",
    'disciplines': "AcademicDiscipline%d",
    'institutions': "OfficeDepartment%d",
}

"""
# get rows
rows = get_rows(workbook_path, sheet_name)

for row in rows:
    # common base fields
    kwargs = get_base_kwargs(columns, column_mappings)
    
    # fields specific to this child model type
    kwargs.update(get_object_specficic_kwargs(columns, column_mappings))
    
    # create object
    ObjectKass.object.create(**kwargs)
    
    # apply many-to-many relationships
    get_base_m2m(parent, columns, patterns)
"""

def get_obj_kwargs():
    """
        date = models.DateField('Presentation Date')
        conf_name = models.CharField(max_length=100, choices=CONF_NAME_CHOICES)
        presentation_type = models.CharField(max_length=100, blank=True, null=True,
            choices=PRESENTATION_CHOICES)
    """
    kwargs = {}
    date = row[columns.index("PresentationDate")].value
    if date:
        kwargs['date'] = date.date()
    
    # get the conference name
    conf = row[columns.index("ConferenceName")].value
    for t in Presentation.CONF_NAME_CHOICES:
        if conf == t[1]:
            kwargs['conf_name'] = t[0]
            break
            
    if conf and 'conf_name' not in kwargs.keys():
        print "conference not found: %s" % conf
        assert False
    
    # get the material type
    _type = row[columns.index("PresType")].value
    for t in Presentation.PRESENTATION_CHOICES:
        if _type == t[1]:
            kwargs['presentation_type'] = t[0]
    if _type and 'presentation_type' not in kwargs.keys():
        print "presentationtype not found: %s" % _type
        assert False
        
    return kwargs
    
rows = get_rows('hub/imports/fixtures/ConferencePresentations.xlsx', 'data')

# run the sanity check first
skip_index_list = sanity_check(rows, columns, column_mappings)

print "importing presentations"

rows = get_rows('hub/imports/fixtures/ConferencePresentations.xlsx', 'data')
count = 0
for row in rows:

    count += 1
    if count == 1 or count in skip_index_list:
        continue
    print count

    kwargs = get_base_kwargs(columns, column_mappings, row)
    kwargs.update(get_obj_kwargs())
    presentation = Presentation.objects.create(**kwargs)
    get_base_m2m(presentation, columns, column_mappings, row)