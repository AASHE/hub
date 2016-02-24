from utils import get_rows, get_base_kwargs, get_base_m2m
from hub.apps.content.types.centers import CenterAndInstitute

columns = [
    "Center Name",
    "Description",
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
    "SustainabilityTopic_1",
    "SustainabilityTopic_2",
    "SustainabilityTopic_3",
    "AcadDiscipline_1",
    "AcadDiscipline_2",
    "AcadDiscipline_3",
    "Tags",
    "Year Founded",
    "Links",
]

column_mappings = {
    'title': "Center Name",
    'topics': "SustainabilityTopic%d",
    'organizations_id': "Organization%d_id",
    'disciplines': "AcadDiscipline_%d",
    'links': "Links",
}

def get_obj_kwargs():
    """
        [not included] num_paid = models.PositiveIntegerField(blank=True, null=True)
        founded = models.PositiveIntegerField(blank=True, null=True)
        [not_included] budget = models.PositiveIntegerField(blank=True, null=True)
    """
    kwargs = {}
    # get the conference name
    year = row[columns.index("Year Founded")].value
    if year:
        kwargs['founded'] = year
    return kwargs
    
rows = get_rows('hub/imports/fixtures/centers.xlsx', 'Sheet1')

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
    center = CenterAndInstitute.objects.create(**kwargs)
    get_base_m2m(center, columns, column_mappings, row)