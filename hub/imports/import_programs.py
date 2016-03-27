from utils import get_rows, get_base_kwargs, get_base_m2m, sanity_check
from hub.apps.content.types.academic import AcademicProgram
from hub.apps.content.models import ContentType

import datetime

columns = [
    "Program Name",
    "Description or Abstract",
    
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
    
    "Sustainability Topic1",
    "Sustainability Topic2",
    "Sustainability Topic3",
    
    "Academic Discipline1",
    "Academic Discipline2",
    "Academic Discipline3",
    
    "Tags",
    "Program Type",
    "Year Founded",
    "Expected Completion Time",
    "distance_ed",
    "commitment",
    
    "Website1label",
    "Website1URL",
    "Website2label",
    "Website2URL",
    "Website3label",
    "Website3URL",
    "Website4label",
    "Website4URL",
    "Website5label",
    "Website5URL",
]

column_mappings = {
    'topics': "Sustainability Topic%d",
    'organizations': "Organization%d",
    'organizations_id': "Organization%did",
    'disciplines': "Academic Discipline%d",
    'files': "Upload%d",
    'links': "Website%dURL",
    'links_label': "Website%dlabel",
    'description': "Description or Abstract",
    'title': "Program Name"
}

def get_obj_kwargs():
    """
        material_type = models.CharField(choices=MATERIAL_TYPE_CHOICES)
        course_name = models.CharField(max_length=500, blank=True, null=True)
        course_level = models.CharField(
            blank=True, null=True, choices=LEVEL_CHOICES)
    """
    kwargs = {}
    
    # get Program Type
    _name = row[columns.index("Program Type")].value
    from hub.apps.metadata.models import ProgramType
    if _name:
        kwargs["program_type"] = ProgramType.objects.get(name=_name)
        
    # get Year Founded
    _year = row[columns.index("Year Founded")].value
    if _year:
        kwargs['founded'] = _year
    
    # completion time
    _completion = row[columns.index("Expected Completion Time")].value
    if _completion:
        if len(_completion) >= 128:
            import pdb; pdb.set_trace()
        kwargs['completion'] = _completion
        
    # distance education
    _distance = row[columns.index("distance_ed")].value
    if _distance:
        for d in AcademicProgram.DISTANCE_CHOICES:
            if _distance.lower() == d[1].lower():
                kwargs['distance'] = d[0]
        if _distance and 'distance' not in kwargs.keys():
            print "distance not found: %s" % _type
            assert False
        
    # commitment
    _commitment = row[columns.index("commitment")].value
    if _commitment:
        for c in AcademicProgram.COMMITMENT_CHOICES:
            if _commitment.lower() == c[1].lower():
                kwargs['commitment'] = c[0]
        if _commitment and 'commitment' not in kwargs.keys():
            print "commitment not found: %s" % _type
            assert False
    
    return kwargs

# run the sanity check first
rows = get_rows('hub/imports/fixtures/academic_programs.xlsx', 'Sheet1')
skip_index_list = sanity_check(rows, columns, column_mappings)
print "SKIP"
print skip_index_list
    
rows = get_rows('hub/imports/fixtures/academic_programs.xlsx', 'Sheet1')

count = 0
for row in rows:
    
    count += 1
    if count == 1 or count in skip_index_list:
        continue
    print count
    if row[0].value == None:
        break

    kwargs = get_base_kwargs(
        columns, column_mappings, row,
        default_permission=ContentType.PERMISSION_CHOICES.open,
        published_date=datetime.date(year=2016, month=2, day=25))
    kwargs.update(get_obj_kwargs())
    program = AcademicProgram.objects.create(**kwargs)
    get_base_m2m(program, columns, column_mappings, row)
