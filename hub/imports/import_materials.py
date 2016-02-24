from utils import get_rows, get_base_kwargs, get_base_m2m
from hub.apps.content.types.courses import Material

columns = [
    "Title",
    "Description",
    "Org1_name",
    "Org1_ID",
    "Sust_Topic_1",
    "Sust_Topic_2",
    "Acad_Disc_1",
    "Acad_Disc_2",
    "Tags",
    "Type of Material (Assignment or Exercise, Syllabus, Course Presentation)",
    "Course Name",
    "Course level",
    "Author1Name",
    "Author1Title",
    "Author1Org",
    "Author1OrgID",
    "Upload1",
    "Link",
]

column_mappings = {
    'topics': "SustainabilityTopic%d",
    'organizations': "Org%d_name",
    'organizations_id': "Org%d_ID",
    'disciplines': "Acad_Disc_%d",
    'files': "Upload%d",
    'links': "Link",
}

def get_obj_kwargs():
    """
        material_type = models.CharField(choices=MATERIAL_TYPE_CHOICES)
        course_name = models.CharField(max_length=500, blank=True, null=True)
        course_level = models.CharField(
            blank=True, null=True, choices=LEVEL_CHOICES)
    """
    kwargs = {}
    
    # get the material type
    _type = row[columns.index("Type of Material (Assignment or Exercise, Syllabus, Course Presentation)")].value
    for t in Material.MATERIAL_TYPE_CHOICES:
        if _type == t[1]:
            kwargs['material_type'] = t[0]
    if _type and 'material_type' not in kwargs.keys():
        print "material_type not found: %s" % _type
        assert False
    
    # get the conference name
    name = row[columns.index("Course Name")].value
    if name:
        kwargs['course_name'] = name
    
    # get the course_level
    level = row[columns.index("Course level")].value
    for t in Material.LEVEL_CHOICES:
        if level == t[1]:
            kwargs['course_level'] = t[0]
    if level and 'course_level' not in kwargs.keys():
        print "course_level not found: %s" % level
        assert False
    
    return kwargs
    
rows = get_rows('hub/imports/fixtures/materials.xlsx', 'Sheet1')

count = 0
for row in rows:
    
    count += 1
    if count == 1: 
        continue
    print count
    if row[0].value == None:
        break

    kwargs = get_base_kwargs(columns, column_mappings, row)
    kwargs.update(get_obj_kwargs())
    material = Material.objects.create(**kwargs)
    get_base_m2m(material, columns, column_mappings, row)